from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import VersionCreateSerializer, VersionDetailSerializer
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class VersionCreateView(ProgramaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = VersionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version = serializer.save()
        return Response(
            VersionDetailSerializer(version).data,
            status=status.HTTP_201_CREATED,
        )