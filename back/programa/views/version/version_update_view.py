from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import VersionUpdateSerializer, VersionDetailSerializer
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class VersionUpdateView(ProgramaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        version, error = self.get_version_or_404(pk)
        if error:
            return error
        serializer = VersionUpdateSerializer(
            version, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(VersionDetailSerializer(version).data)