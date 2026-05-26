from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import AulaCreateSerializer, AulaDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class AulaCreateView(AulaBaseView):
    """POST /api/aulas/create/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = AulaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aula = serializer.save()
        return Response(
            AulaDetailSerializer(aula).data,
            status=status.HTTP_201_CREATED,
        )