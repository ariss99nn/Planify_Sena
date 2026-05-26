from rest_framework import serializers
from bhorario.models.bloque_horario_model import BloqueHorario


class BloqueHorarioCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloqueHorario
        fields = [
            'dia_semana', 'hora_inicio', 'hora_fin',
            'jornada', 'aula', 'docente', 'ficha',
        ]

    def validate(self, data):
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({
                'hora_fin': 'La hora de fin debe ser mayor a la hora de inicio.'
            })

        dia = data.get('dia_semana')
        docente = data.get('docente')
        aula = data.get('aula')

        if docente and hora_inicio and hora_fin:
            conflicto = BloqueHorario.objects.filter(
                dia_semana=dia,
                docente=docente,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            )
            if conflicto.exists():
                raise serializers.ValidationError(
                    'El docente ya tiene un bloque asignado en ese horario.'
                )

        if aula and hora_inicio and hora_fin:
            conflicto = BloqueHorario.objects.filter(
                dia_semana=dia,
                aula=aula,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            )
            if conflicto.exists():
                raise serializers.ValidationError(
                    'El aula ya tiene un bloque asignado en ese horario.'
                )

        return data