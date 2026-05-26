from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from aulas.serializers import AulaEstadoSerializer, AulaDetailSerializer
from users.permissions import IsManager, IsDocente
from aulas.views.base_view import AulaBaseView

# CORRECCIÓN: lógica de autorización extraída a permission_classes.
# Ya no hay import diferido ni chequeo manual de roles dentro del método.
# IsManagerOrDocente debería vivir en users/permissions.py junto a los demás.
from users.permissions import IsManagerOrDocente


class AulaEstadoView(AulaBaseView):
    """
    PATCH /api/aulas/{id}/estado/
    IsManager (COORDINADOR / ADMIN): puede cambiar a cualquier estado.
    IsDocente: puede cambiar estado en el momento (situación operativa).
    """
    permission_classes = [IsAuthenticated, IsManagerOrDocente]

    def patch(self, request, pk):
        aula, error = self.get_aula_or_404(pk)
        if error:
            return error

        serializer = AulaEstadoSerializer(aula, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # CORRECCIÓN: serializer.instance es el objeto actualizado en memoria.
        # Usar 'aula' devolvería el estado previo al save (objeto stale).
        return Response(AulaDetailSerializer(serializer.instance).data)