from rest_framework import serializers
from django.utils import timezone
from planificacion.models.plan_trimestral_model import PlanTrimestral


class PlanTrimestralListSerializer(serializers.ModelSerializer):

    ficha_codigo = serializers.CharField(
        source='ficha.codigo_ficha', read_only=True
    )
    programa_nombre = serializers.CharField(
        source='ficha.version.programa.nombre', read_only=True
    )
    total_horas_planificadas = serializers.IntegerField(read_only=True)
    total_horas_ejecutadas = serializers.DecimalField(
        max_digits=6, decimal_places=1, read_only=True
    )
    porcentaje_avance = serializers.FloatField(read_only=True)
    aprobado_por_nombre = serializers.CharField(
        source='aprobado_por.nombre', read_only=True, default=None
    )

    class Meta:
        model = PlanTrimestral
        fields = [
            'id', 'ficha', 'ficha_codigo', 'programa_nombre',
            'trimestre', 'fecha_inicio', 'fecha_fin',
            'aprobado', 'aprobado_por_nombre', 'fecha_aprobacion',
            'total_horas_planificadas', 'total_horas_ejecutadas',
            'porcentaje_avance',
        ]


class PlanTrimestralDetailSerializer(serializers.ModelSerializer):

    ficha_codigo = serializers.CharField(
        source='ficha.codigo_ficha', read_only=True
    )
    programa_nombre = serializers.CharField(
        source='ficha.version.programa.nombre', read_only=True
    )
    total_horas_planificadas = serializers.IntegerField(read_only=True)
    total_horas_ejecutadas = serializers.DecimalField(
        max_digits=6, decimal_places=1, read_only=True
    )
    porcentaje_avance = serializers.FloatField(read_only=True)
    aprobado_por_nombre = serializers.CharField(
        source='aprobado_por.nombre', read_only=True, default=None
    )
    items = serializers.SerializerMethodField()

    class Meta:
        model = PlanTrimestral
        fields = [
            'id', 'ficha', 'ficha_codigo', 'programa_nombre',
            'trimestre', 'fecha_inicio', 'fecha_fin',
            'aprobado', 'aprobado_por', 'aprobado_por_nombre',
            'fecha_aprobacion',
            'total_horas_planificadas', 'total_horas_ejecutadas',
            'porcentaje_avance',
            'items',
            'created_at', 'updated_at',
        ]

    def get_items(self, obj):
        from planificacion.serializers.item_plan_serializer import (
            ItemPlanListSerializer,
        )
        return ItemPlanListSerializer(
            obj.items.select_related(
                'competencia', 'docente__user'
            ).all(), many=True
        ).data


class PlanTrimestralCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanTrimestral
        fields = [
            'ficha', 'trimestre', 'fecha_inicio', 'fecha_fin',
        ]

    def validate(self, data):
        ficha = data.get('ficha')
        trimestre = data.get('trimestre')

        if PlanTrimestral.objects.filter(
            ficha=ficha, trimestre=trimestre
        ).exists():
            raise serializers.ValidationError(
                f'Ya existe un plan para la ficha '
                f'{ficha.codigo_ficha} en el trimestre {trimestre}.'
            )

        trimestres_max = getattr(
            ficha.version.programa, 'trimestres_totales', None
        )
        if trimestres_max and trimestre > trimestres_max:
            raise serializers.ValidationError({
                'trimestre': (
                    f'El programa solo tiene {trimestres_max} trimestres.'
                )
            })

        if data.get('fecha_fin') and data['fecha_fin'] <= data['fecha_inicio']:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la de inicio.'
            })
        return data


class PlanTrimestralUpdateSerializer(serializers.ModelSerializer):
    """No permite cambiar ficha ni trimestre."""

    class Meta:
        model = PlanTrimestral
        fields = ['fecha_inicio', 'fecha_fin']

    def validate(self, data):
        fecha_inicio = data.get(
            'fecha_inicio',
            self.instance.fecha_inicio if self.instance else None,
        )
        fecha_fin = data.get('fecha_fin')
        if fecha_fin and fecha_inicio and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la de inicio.'
            })
        return data


class PlanTrimestralAprobarSerializer(serializers.ModelSerializer):
    """Aprueba o desaprueba un plan."""

    class Meta:
        model = PlanTrimestral
        fields = ['aprobado']

    def validate_aprobado(self, value):
        if value and not self.instance.items.exists():
            raise serializers.ValidationError(
                'No se puede aprobar un plan sin items.'
            )
        return value

    def update(self, instance, validated_data):
        from django.utils import timezone
        request = self.context.get('request')
        instance.aprobado = validated_data['aprobado']
        if instance.aprobado:
            instance.aprobado_por = request.user if request else None
            instance.fecha_aprobacion = timezone.now()
        else:
            instance.aprobado_por = None
            instance.fecha_aprobacion = None
        instance.save(update_fields=[
            'aprobado', 'aprobado_por', 'fecha_aprobacion'
        ])
        return instance