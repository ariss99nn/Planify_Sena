from rest_framework import serializers


class BaseDocenteSerializer(serializers.ModelSerializer):

    def validate_horas_max_semanales(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Las horas semanales deben ser mayores a 0."
            )
        if value > 40:
            raise serializers.ValidationError(
                "Las horas semanales no pueden superar 40."
            )
        return value