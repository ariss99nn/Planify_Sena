from rest_framework.permissions import BasePermission
from users.models.user import User

class CanManageFicha(BasePermission):
    """
    COORDINADOR / ADMINISTRATIVO: puede gestionar cualquier ficha.
    DOCENTE: solo puede ver/actualizar fichas donde es jefe_grupo.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.rol in (User.Rol.COORDINADOR, User.Rol.ADMINISTRATIVO):  # ✅ corregido: era Rol.ADMIN
            return True
        if user.rol == User.Rol.DOCENTE:
            return obj.jefe_grupo and obj.jefe_grupo.user == user
        return False