from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bhorario.serializers import BloqueHorarioCreateSerializer, BloqueHorarioDetailSerializer
from users.permissions import IsManager
from bhorario.views.base import BhorarioBaseView
from bhorario.services.bloque_service import BloqueHorarioService

class BloqueHorarioCreateView(BhorarioBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = BloqueHorarioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            bloque = BloqueHorarioService.crear_bloque(
                serializer.validated_data
            )
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
        return Response(
            BloqueHorarioDetailSerializer(bloque).data,
            status=status.HTTP_201_CREATED,
        )

# class BloqueHorarioCreateView(BhorarioBaseView):
#     permission_classes = [IsAuthenticated, IsManager]

#     def post(self, request):
#         serializer = BloqueHorarioCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         bloque = serializer.save()
#         return Response(
#             BloqueHorarioDetailSerializer(bloque).data,
#             status=status.HTTP_201_CREATED,
#         )