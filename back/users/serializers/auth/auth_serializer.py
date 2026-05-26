from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models.user import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Buscamos el usuario directamente para poder distinguir entre
        # credenciales malas, cuenta no verificada y cuenta desactivada.
        # No usamos authenticate() porque ModelBackend retorna None cuando
        # is_active=False, impidiendo mostrar el mensaje correcto al usuario.
        try:
            user = User.objects.get(email__iexact=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Credenciales inválidas.", "code": "invalid_credentials"}
            )

        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                {"detail": "Credenciales inválidas.", "code": "invalid_credentials"}
            )

        if not user.email_verificado:
            raise serializers.ValidationError(
                {"detail": "Debes verificar tu correo antes de iniciar sesión.", "code": "not_verified"}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Esta cuenta ha sido desactivada. Contacta al administrador.", "code": "inactive"}
            )

        data['user'] = user
        return data

    def get_tokens(self, user=None):
        target = user or self.validated_data['user']
        refresh = RefreshToken.for_user(target)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Token inválido o ya expirado.")