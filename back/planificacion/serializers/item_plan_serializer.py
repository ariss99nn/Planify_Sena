from rest_framework import serializers
from planificacion.models.item_plan_model import ItemPlan


class ItemPlanListSerializer(serializers.ModelSerializer):

    competencia_codigo = serializers.CharField(
        source='competencia.codigo', read_only=True
    )
    competencia_nombre = serializers.CharField(
        source='competencia.nombre', read_only=True
    )
    competencia_tipo = serializers.CharField(
        source='competencia.tipo', read_only=True
    )
    docente_nombre = serializers.CharField(
        source='docente.user.nombre', read_only=True, default=None
    )
    horas_ejecutadas = serializers.DecimalField(
        max_digits=5, decimal_places=1, read_only=True
    )
    horas_restantes = serializers.IntegerField(read_only=True)
    porcentaje_avance = serializers.FloatField(read_only=True)

    class Meta:
        model = ItemPlan
        fields = [
            'id', 'plan', 'competencia', 'competencia_codigo',
            'competencia_nombre', 'competencia_tipo',
            'docente', 'docente_nombre',
            'horas_asignadas', 'horas_ejecutadas',
            'horas_restantes', 'porcentaje_avance',
            'orden', 'completado',
        ]


class ItemPlanCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPlan
        fields = [
            'plan', 'competencia', 'docente',
            'horas_asignadas', 'orden',
        ]

    def validate(self, data):
        plan = data.get('plan')
        competencia = data.get('competencia')

        if plan and plan.aprobado:
            raise serializers.ValidationError(
                'No se pueden agregar items a un plan ya aprobado.'
            )

        if ItemPlan.objects.filter(
            plan=plan, competencia=competencia
        ).exists():
            raise serializers.ValidationError(
                'Esta competencia ya está en el plan.'
            )

        # Validar que horas no superen las de la asignatura
        if competencia and competencia.asignatura_id:
            horas_max = competencia.asignatura.total_horas
            if data.get('horas_asignadas', 0) > horas_max:
                raise serializers.ValidationError({
                    'horas_asignadas': (
                        f'No puede superar {horas_max} horas '
                        f'de la asignatura.'
                    )
                })
        return data


class ItemPlanUpdateSerializer(serializers.ModelSerializer):
    """No permite cambiar plan ni competencia."""

    class Meta:
        model = ItemPlan
        fields = ['docente', 'horas_asignadas', 'orden', 'completado']

    def validate(self, data):
        if self.instance and self.instance.plan.aprobado:
            raise serializers.ValidationError(
                'No se puede editar un item de un plan aprobado.'
            )
        return data