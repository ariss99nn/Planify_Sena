import 'dart:async';
import 'package:flutter/foundation.dart';
import '../models/ws_mensaje_model.dart';
import 'ws_alertas_service.dart';

/// ChangeNotifier que expone las notificaciones recibidas por WebSocket.
///
/// Ejemplo de setup en main.dart / login callback:
///
///   ChangeNotifierProvider(
///     create: (_) => NotificacionesNotifier(token: accessToken),
///   )
///
/// Para mostrar el toast en pantallas que ya tienen Scaffold:
///
///   context.read<NotificacionesNotifier>().addListener(() {
///     final msgs = context.read<NotificacionesNotifier>().mensajes;
///     if (msgs.isNotEmpty) AlertaToast.show(context, msgs.first);
///   });
class NotificacionesNotifier extends ChangeNotifier {
  final WsAlertasService _svc;
  StreamSubscription<WsMensaje>? _sub;

  final List<WsMensaje> _mensajes = [];
  int _noLeidas = 0;
  String? _ultimoError;
  bool _conectado = false;

  List<WsMensaje> get mensajes    => List.unmodifiable(_mensajes);
  int             get noLeidas    => _noLeidas;
  String?         get ultimoError => _ultimoError;
  bool            get conectado   => _conectado;

  /// El último mensaje recibido de tipo alerta — útil para disparar toasts.
  WsMensaje? get ultimoMensaje => _mensajes.isNotEmpty ? _mensajes.first : null;

  NotificacionesNotifier({required String token, String? baseWsUrl})
      : _svc = WsAlertasService(
          token: token,
          baseWsUrl: baseWsUrl ?? 'ws://192.168.10.27:8000',
        ) {
    _init();
  }

  void _init() {
    _svc.connect();
    _sub = _svc.mensajes.listen(
      _onMensaje,
      onError: (e) {
        _ultimoError = e.toString();
        _conectado   = false;
        notifyListeners();
      },
    );
  }

  void _onMensaje(WsMensaje msg) {
    switch (msg.tipo) {
      case TipoWsMensaje.conexion:
        _conectado   = true;
        _ultimoError = null;
      case TipoWsMensaje.alerta_nueva:
      case TipoWsMensaje.conflicto_horario:
        _mensajes.insert(0, msg);
        _noLeidas++;
      case TipoWsMensaje.pong:
        break;
      case TipoWsMensaje.desconocido:
        break;
    }
    notifyListeners();
  }

  void marcarTodasLeidas() {
    _noLeidas = 0;
    notifyListeners();
  }

  @override
  void dispose() {
    _sub?.cancel();
    _svc.dispose();
    super.dispose();
  }
}