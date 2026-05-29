import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/ws_mensaje_model.dart';

/// Gestiona la conexión WebSocket a ws://host/ws/alertas/?token=<access>
///
/// Reconexión automática en 5 s si la conexión cae.
/// Ping cada 30 s para keepalive (el consumer responde con pong).
class WsAlertasService {
  final String token;
  final String baseWsUrl;

  WsAlertasService({
    required this.token,
    this.baseWsUrl = 'ws://192.168.10.27:8000',
  });

  WebSocketChannel? _channel;
  final _controller = StreamController<WsMensaje>.broadcast();
  Timer? _pingTimer;
  bool _disposed = false;

  Stream<WsMensaje> get mensajes => _controller.stream;

  void connect() {
    if (_disposed) return;
    final uri = Uri.parse('$baseWsUrl/ws/alertas/?token=$token');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
      (raw) {
        if (_disposed) return;
        try {
          final json = jsonDecode(raw as String) as Map<String, dynamic>;
          _controller.add(WsMensaje.fromJson(json));
        } catch (_) {}
      },
      onError: (e) {
        if (!_disposed) _controller.addError(e);
      },
      onDone: () {
        _pingTimer?.cancel();
        if (!_disposed) {
          Future.delayed(const Duration(seconds: 5), () {
            if (!_disposed) connect();
          });
        }
      },
      cancelOnError: false,
    );

    _pingTimer?.cancel();
    _pingTimer = Timer.periodic(const Duration(seconds: 30), (_) {
      _send({'tipo': 'ping'});
    });
  }

  void _send(Map<String, dynamic> data) {
    try {
      _channel?.sink.add(jsonEncode(data));
    } catch (_) {}
  }

  void dispose() {
    _disposed = true;
    _pingTimer?.cancel();
    _channel?.sink.close();
    _controller.close();
  }
}