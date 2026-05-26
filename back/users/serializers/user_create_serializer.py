from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from users.models.user import User
from users.models.email_verification import EmailVerification
from users.services.token_service import generate_numeric_code
from users.services.email_service import send_verification_email
from users.services.role_service import sync_user_group


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'nombre',
            'apellido',
            'email',
            'rol',
            'password',
            'password2',
            'imagen',
        )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email.")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User(**validated_data, is_active=False, email_verificado=False)
        user.set_password(password)
        user.save()

        sync_user_group(user)

        EmailVerification.invalidate_previous_codes(user)

        code = generate_numeric_code()
        EmailVerification.objects.create(
            user=user,
            code=code,
            expires_at=EmailVerification.get_expiration_time(),
        )

        transaction.on_commit(lambda: send_verification_email(user.email, code))

        return user