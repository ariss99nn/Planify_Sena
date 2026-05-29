import 'package:flutter/material.dart';
import '../models/ws_mensaje_model.dart';

/// SnackBar flotante que muestra una alerta WS en la pantalla actual.
///
/// Llamar desde un listener en el widget raíz que tenga Scaffold:
///
///   @override
///   void didChangeDependencies() {
///     super.didChangeDependencies();
///     context.read<NotificacionesNotifier>().addListener(_onNotif);
///   }
///
///   void _onNotif() {
///     final msg = context.read<NotificacionesNotifier>().ultimoMensaje;
///     if (msg != null && mounted) AlertaToast.show(context, msg);
///   }
class AlertaToast {
  static void show(BuildContext context, WsMensaje msg) {
    final key = msg.tipoAlerta ?? msg.tipo.name;
    final (icon, color, label) = switch (key) {
      'CONFLICTO' || 'conflicto_horario' =>
        (Icons.warning_amber_rounded, const Color(0xFFA32D2D), 'Conflicto de horario'),
      'DISPONIBILIDAD' =>
        (Icons.calendar_today_outlined, const Color(0xFF185FA5), 'Disponibilidad'),
      'SISTEMA' =>
        (Icons.settings_outlined, const Color(0xFF854F0B), 'Sistema'),
      _ =>
        (Icons.notifications_outlined, const Color(0xFF2E7D32), 'Notificación'),
    };

    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          behavior: SnackBarBehavior.floating,
          margin: const EdgeInsets.all(12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          backgroundColor: Colors.white,
          elevation: 6,
          duration: const Duration(seconds: 4),
          content: Row(
            children: [
              Container(
                width: 34,
                height: 34,
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, size: 18, color: color),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: color,
                      ),
                    ),
                    if (msg.descripcion != null)
                      Text(
                        msg.descripcion!,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFF1B5E20),
                          height: 1.3,
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
  }
}