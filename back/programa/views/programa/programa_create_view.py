from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import ProgramaCreateSerializer, ProgramaDetailSerializer
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class ProgramaCreateView(ProgramaBaseView):
    """POST /api/programas/create/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = ProgramaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        programa = serializer.save()
        return Response(
            ProgramaDetailSerializer(programa).data,
            status=status.HTTP_201_CREATED,
        )