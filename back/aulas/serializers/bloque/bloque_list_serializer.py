from rest_framework import serializers
from aulas.models.bloque import Bloque


class BloqueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bloque
        fields = ['id', 'nombre', 'piso', 'capacidad_maxima']