from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import BloqueCreateSerializer, BloqueDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class BloqueCreateView(AulaBaseView):
    """POST /api/aulas/bloques/create/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = BloqueCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bloque = serializer.save()
        return Response(
            BloqueDetailSerializer(bloque).data,
            status=status.HTTP_201_CREATED,
        )