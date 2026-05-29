// ─────────────────────────────────────────────────────────────────────────────
// EJEMPLO DE INTEGRACIÓN — no es un archivo de producción, es guía de uso.
// ─────────────────────────────────────────────────────────────────────────────
//
// 1. Dependencias en pubspec.yaml:
//    provider: ^6.1.2
//    web_socket_channel: ^3.0.1
//
// 2. En el login callback, después de guardar los tokens:
//
//   final notifier = NotificacionesNotifier(token: accessToken);
//   // Pasar al árbol con un provider global:
//
// main.dart (estructura mínima):
// ─────────────────────────────────────────────────────────────────────────────
//
//   void main() async {
//     WidgetsFlutterBinding.ensureInitialized();
//     final access = await TokenStorage.getAccessToken();
//     runApp(
//       ChangeNotifierProvider(
//         create: (_) => NotificacionesNotifier(token: access ?? ''),
//         child: const MyApp(),
//       ),
//     );
//   }
//
// ─────────────────────────────────────────────────────────────────────────────
// HomeScreen (con toast en tiempo real):
// ─────────────────────────────────────────────────────────────────────────────
//
//   class HomeScreen extends StatefulWidget { ... }
//
//   class _HomeScreenState extends State<HomeScreen> {
//     late final NotificacionesNotifier _notif;
//
//     @override
//     void didChangeDependencies() {
//       super.didChangeDependencies();
//       _notif = context.read<NotificacionesNotifier>();
//       _notif.addListener(_onNuevaNotif);
//     }
//
//     void _onNuevaNotif() {
//       final msg = _notif.ultimoMensaje;
//       if (msg != null && mounted &&
//           (msg.tipo == TipoWsMensaje.alerta_nueva ||
//            msg.tipo == TipoWsMensaje.conflicto_horario)) {
//         AlertaToast.show(context, msg);
//       }
//     }
//
//     @override
//     void dispose() {
//       _notif.removeListener(_onNuevaNotif);
//       super.dispose();
//     }
//
//     @override
//     Widget build(BuildContext context) {
//       return Scaffold(
//         appBar: AppBar(
//           title: const Text('CHRONOSIA'),
//           actions: const [NotificacionBadge()],  // ← badge automático
//         ),
//         body: ...,
//       );
//     }
//   }
//
// ─────────────────────────────────────────────────────────────────────────────
// Autenticación WebSocket en Django Channels:
// ─────────────────────────────────────────────────────────────────────────────
//
// El consumer recibe el token via query string (?token=...).
// Para validarlo, usar TokenAuthMiddleware en asgi.py:
//
//   # asgi.py
//   from channels.routing import ProtocolTypeRouter, URLRouter
//   from notificaciones.routing import websocket_urlpatterns
//   from notificaciones.middleware import TokenAuthMiddleware
//
//   application = ProtocolTypeRouter({
//     'http': django_asgi_app,
//     'websocket': TokenAuthMiddleware(
//       URLRouter(websocket_urlpatterns)
//     ),
//   })
//
// # notificaciones/middleware.py
//   from urllib.parse import parse_qs
//   from channels.db import database_sync_to_async
//   from rest_framework_simplejwt.tokens import AccessToken
//   from django.contrib.auth.models import AnonymousUser
//   from users.models.user import User
//
//   class TokenAuthMiddleware:
//     def __init__(self, inner):
//       self.inner = inner
//
//     async def __call__(self, scope, receive, send):
//       qs = parse_qs(scope['query_string'].decode())
//       token_str = qs.get('token', [None])[0]
//       scope['user'] = await self._get_user(token_str)
//       return await self.inner(scope, receive, send)
//
//     @database_sync_to_async
//     def _get_user(self, token_str):
//       if not token_str:
//         return AnonymousUser()
//       try:
//         data = AccessToken(token_str)
//         return User.objects.get(pk=data['user_id'])
//       except Exception:
//         return AnonymousUser()