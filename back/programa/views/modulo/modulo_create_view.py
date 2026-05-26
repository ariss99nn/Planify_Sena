from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import ModuloCreateSerializer, ModuloDetailSerializer
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class ModuloCreateView(ProgramaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = ModuloCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modulo = serializer.save()
        return Response(
            ModuloDetailSerializer(modulo).data,
            status=status.HTTP_201_CREATED,
        )