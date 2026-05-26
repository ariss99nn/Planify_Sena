from rest_framework import serializers
from ficha.models.ficha_model import Ficha
from bhorario.models.bloque_horario_model import BloqueHorario


MODULOS_DISPONIBLES = [
    'fichas', 'estudiantes', 'docentes',
    'aulas', 'bloques_horario', 'competencias',
]


class ExportacionRequestSerializer(serializers.Serializer):
    modulo = serializers.ChoiceField(choices=[(m, m) for m in MODULOS_DISPONIBLES])
    formato = serializers.ChoiceField(choices=[('csv', 'CSV'), ('excel', 'Excel')])
    filtros = serializers.DictField(required=False, default=dict)