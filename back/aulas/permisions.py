from rest_framework.permissions import BasePermission
from users.models.user import User


class IsManagerOrDocente(BasePermission):
    """
    Permite acceso a COORDINADOR, ADMIN y DOCENTE.
    Extraído de AulaEstadoView para que la lógica de autorización
    viva en permissions.py y no dentro del método de la vista.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.rol in {
                User.Rol.COORDINADOR,
                User.Rol.ADMIN,
                User.Rol.DOCENTE,
            }
        )


class CanManageBloque(BasePermission):
    """
    COORDINADOR / ADMINISTRATIVO: puede gestionar cualquier bloque.
    DOCENTE: solo puede gestionar bloques donde es el docente asignado.

    ADVERTENCIA: la rama DOCENTE asume que el objeto pasado tiene un campo
    'docente' con un FK a un perfil que a su vez tiene FK a User.
    El modelo Bloque actual NO tiene ese campo — esta permisión probablemente
    está pensada para Aula u otro modelo. Revisar antes de usar.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.rol in (User.Rol.COORDINADOR, User.Rol.ADMINISTRATIVO):
            return True
        if user.rol == User.Rol.DOCENTE:
            # TODO: confirmar que el modelo del objeto tiene campo 'docente'
            return hasattr(obj, 'docente') and obj.docente and obj.docente.user == user
        return False