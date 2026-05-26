from users.views.auth import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfileView,
    EmailChangeRequestView,
    EmailChangeConfirmView,
)
from users.views.user import (
    UserListCreateView,
    UserRetrieveUpdateView,
    UserDesactivateView,
)

__all__ = [
    # auth
    'RegisterView',
    'VerifyEmailView',
    'LoginView',
    'LogoutView',
    'PasswordResetRequestView',
    'PasswordResetConfirmView',
    # perfil propio
    'ProfileView',
    'EmailChangeRequestView',
    'EmailChangeConfirmView',
    # gestión de usuarios
    'UserListCreateView',
    'UserRetrieveUpdateView',
    'UserDesactivateView',
]