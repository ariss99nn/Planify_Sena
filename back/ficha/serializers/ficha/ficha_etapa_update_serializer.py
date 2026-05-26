from rest_framework import serializers
from ficha.models.ficha_model import Ficha


class FichaEtapaUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer exclusivo para cambiar la etapa de una ficha.
    Inyecta _cambiado_por en la instancia para que la señal
    pre_save pueda registrar quién hizo el cambio en HistorialEtapa.
    """

    class Meta:
        model = Ficha
        fields = ['etapa', 'trimestre']

    def validate_etapa(self, value):
        if value not in [choice[0] for choice in Ficha.Etapa.choices]:
            raise serializers.ValidationError('Etapa inválida.')
        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.instance._cambiado_por = request.user
        return super().save(**kwargs)