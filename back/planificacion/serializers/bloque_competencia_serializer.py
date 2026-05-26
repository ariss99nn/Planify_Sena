from rest_framework import serializers
from planificacion.models.bloque_competencia_model import BloqueCompetencia


class BloqueCompetenciaListSerializer(serializers.ModelSerializer):

    competencia_codigo = serializers.CharField(
        source='item_plan.competencia.codigo', read_only=True
    )
    competencia_nombre = serializers.CharField(
        source='item_plan.competencia.nombre', read_only=True
    )
    bloque_dia = serializers.CharField(
        source='bloque.get_dia_semana_display', read_only=True
    )
    bloque_hora_inicio = serializers.TimeField(
        source='bloque.hora_inicio', read_only=True
    )
    bloque_hora_fin = serializers.TimeField(
        source='bloque.hora_fin', read_only=True
    )
    horas_restantes_item = serializers.IntegerField(
        source='item_plan.horas_restantes', read_only=True
    )

    class Meta:
        model = BloqueCompetencia
        fields = [
            'id', 'bloque', 'item_plan',
            'competencia_codigo', 'competencia_nombre',
            'bloque_dia', 'bloque_hora_inicio', 'bloque_hora_fin',
            'horas_ejecutadas', 'horas_restantes_item',
            'observaciones',
        ]


class BloqueCompetenciaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloqueCompetencia
        fields = ['bloque', 'item_plan', 'horas_ejecutadas', 'observaciones']

    def validate(self, data):
        bloque = data.get('bloque')
        item_plan = data.get('item_plan')

        if hasattr(bloque, 'competencia_asignada'):
            raise serializers.ValidationError(
                'Este bloque ya tiene una competencia asignada.'
            )

        if not item_plan.plan.aprobado:
            raise serializers.ValidationError(
                'Solo se pueden vincular bloques a planes aprobados.'
            )

        # Validar que el bloque pertenezca a la misma ficha del plan
        if bloque.ficha_id != item_plan.plan.ficha_id:
            raise serializers.ValidationError(
                'El bloque debe pertenecer a la misma ficha del plan.'
            )

        return data