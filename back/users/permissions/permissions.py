from rest_framework.permissions import BasePermission
from users.models.user import User


# ---------------------------------------------------------------------------
# Base por rol
# ---------------------------------------------------------------------------

class HasRole(BasePermission):
    allowed_roles: tuple = ()                              # ✅ tupla inmutable, no lista

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.rol in self.allowed_roles


class IsEstudiante(HasRole):
    allowed_roles = (User.Rol.ESTUDIANTE,)


class IsDocente(HasRole):
    allowed_roles = (User.Rol.DOCENTE,)


class IsCoordinador(HasRole):
    allowed_roles = (User.Rol.COORDINADOR,)


class IsAdministrativo(HasRole):
    allowed_roles = (User.Rol.ADMINISTRATIVO,)


class IsManager(HasRole):
    """COORDINADOR + ADMINISTRATIVO — gestión completa del sistema."""
    allowed_roles = (User.Rol.COORDINADOR, User.Rol.ADMINISTRATIVO)


class IsStaffLike(HasRole):
    """Docentes, coordinadores y administrativos — excluye estudiantes."""
    allowed_roles = (
        User.Rol.DOCENTE,
        User.Rol.COORDINADOR,
        User.Rol.ADMINISTRATIVO,
    )

class IsManagerOrDocente(BasePermission):
    """
    Permiso personalizado para permitir solo a managers y docentes
    """
    def has_permission(self, request, view):
        # Implementa tu lógica aquí
        user = request.user
        return user.is_authenticated and (
            user.rol == 'manager' or user.rol == 'docente'
        )
# ---------------------------------------------------------------------------
# Gestión de usuarios
# ---------------------------------------------------------------------------

class CanManageUser(IsManager):
    """
    Controla quién puede editar, desactivar o gestionar a otro usuario.

    Reglas:
    - Solo COORDINADOR y ADMINISTRATIVO tienen acceso (hereda IsManager).
    - Nadie puede gestionarse a sí mismo por esta vía (para eso existe /auth/profile/).
    """

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return False
        return request.user.rol in self.allowed_roles      # ✅ reutiliza allowed_roles de IsManager



