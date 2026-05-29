import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/notificaciones_notifier.dart';
import '../screens/notificaciones_screen.dart';

/// Ícono de campana con badge rojo del contador de no leídas.
///
/// Colocar en el AppBar de cualquier pantalla:
///   actions: [const NotificacionBadge()],
///
/// Requiere NotificacionesNotifier en el árbol de providers.
class NotificacionBadge extends StatelessWidget {
  const NotificacionBadge({super.key});

  @override
  Widget build(BuildContext context) {
    final noLeidas = context.select<NotificacionesNotifier, int>(
      (n) => n.noLeidas,
    );

    return Stack(
      clipBehavior: Clip.none,
      children: [
        IconButton(
          icon: const Icon(Icons.notifications_outlined, color: Colors.white),
          tooltip: 'Notificaciones',
          onPressed: () {
            context.read<NotificacionesNotifier>().marcarTodasLeidas();
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ChangeNotifierProvider.value(
                  value: context.read<NotificacionesNotifier>(),
                  child: const NotificacionesScreen(),
                ),
              ),
            );
          },
        ),
        if (noLeidas > 0)
          Positioned(
            top: 6,
            right: 6,
            child: IgnorePointer(
              child: Container(
                width: 16,
                height: 16,
                decoration: const BoxDecoration(
                  color: Color(0xFFE53935),
                  shape: BoxShape.circle,
                ),
                alignment: Alignment.center,
                child: Text(
                  noLeidas > 9 ? '9+' : '$noLeidas',
                  style: const TextStyle(
                    fontSize: 9,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }
}