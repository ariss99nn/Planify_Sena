from rest_framework import serializers
from bhorario.models.bloque_horario_model import BloqueHorario


class BloqueHorarioUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloqueHorario
        fields = [
            'dia_semana', 'hora_inicio', 'hora_fin',
            'jornada', 'aula', 'docente', 'ficha',
        ]

    def validate(self, data):
        hora_inicio = data.get(
            'hora_inicio',
            self.instance.hora_inicio if self.instance else None,
        )
        hora_fin = data.get(
            'hora_fin',
            self.instance.hora_fin if self.instance else None,
        )
        dia = data.get(
            'dia_semana',
            self.instance.dia_semana if self.instance else None,
        )
        docente = data.get(
            'docente',
            self.instance.docente if self.instance else None,
        )
        aula = data.get(
            'aula',
            self.instance.aula if self.instance else None,
        )

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({
                'hora_fin': 'La hora de fin debe ser mayor a la hora de inicio.'
            })

        if docente and hora_inicio and hora_fin:
            conflicto = BloqueHorario.objects.filter(
                dia_semana=dia,
                docente=docente,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exclude(pk=self.instance.pk)
            if conflicto.exists():
                raise serializers.ValidationError(
                    'El docente ya tiene un bloque en ese horario.'
                )

        if aula and hora_inicio and hora_fin:
            conflicto = BloqueHorario.objects.filter(
                dia_semana=dia,
                aula=aula,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exclude(pk=self.instance.pk)
            if conflicto.exists():
                raise serializers.ValidationError(
                    'El aula ya tiene un bloque en ese horario.'
                )

        return data