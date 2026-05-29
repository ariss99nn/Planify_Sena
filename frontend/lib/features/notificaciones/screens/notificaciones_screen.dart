import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/ws_mensaje_model.dart';
import '../services/notificaciones_notifier.dart';

class NotificacionesScreen extends StatelessWidget {
  const NotificacionesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final notifier = context.watch<NotificacionesNotifier>();
    final mensajes = notifier.mensajes
        .where((m) =>
            m.tipo == TipoWsMensaje.alerta_nueva ||
            m.tipo == TipoWsMensaje.conflicto_horario)
        .toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notificaciones'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 14),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 7,
                  height: 7,
                  decoration: BoxDecoration(
                    color: notifier.conectado
                        ? const Color(0xFF69F0AE)
                        : Colors.grey.shade400,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 5),
                Text(
                  notifier.conectado ? 'En vivo' : 'Desconectado',
                  style: const TextStyle(fontSize: 12, color: Colors.white70),
                ),
              ],
            ),
          ),
        ],
      ),
      body: mensajes.isEmpty
          ? const _EmptyView()
          : ListView.separated(
              padding: const EdgeInsets.all(12),
              itemCount: mensajes.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (_, i) => _NotifTile(msg: mensajes[i]),
            ),
    );
  }
}

class _NotifTile extends StatelessWidget {
  final WsMensaje msg;
  const _NotifTile({required this.msg});

  @override
  Widget build(BuildContext context) {
    final esConflicto = msg.tipo == TipoWsMensaje.conflicto_horario ||
        msg.tipoAlerta == 'CONFLICTO';
    final esSistema = msg.tipoAlerta == 'SISTEMA';

    final (icon, color, bgColor, label) = switch (true) {
      _ when esConflicto => (
          Icons.warning_amber_rounded,
          const Color(0xFFA32D2D),
          const Color(0xFFFCEBEB),
          'Conflicto de horario',
        ),
      _ when esSistema => (
          Icons.settings_outlined,
          const Color(0xFF854F0B),
          const Color(0xFFFAEEDA),
          'Sistema',
        ),
      _ => (
          Icons.notifications_outlined,
          const Color(0xFF185FA5),
          const Color(0xFFE6F1FB),
          'Alerta nueva',
        ),
    };

    final fecha = msg.fecha != null ? DateTime.tryParse(msg.fecha!) : null;
    final fechaStr = fecha != null
        ? '${fecha.day}/${fecha.month} '
          '${fecha.hour.toString().padLeft(2, '0')}:'
          '${fecha.minute.toString().padLeft(2, '0')}'
        : '';

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: Colors.grey.shade200, width: 0.5),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(color: bgColor, shape: BoxShape.circle),
            child: Icon(icon, size: 18, color: color),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      label,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: color,
                      ),
                    ),
                    const Spacer(),
                    Text(
                      fechaStr,
                      style: TextStyle(fontSize: 11, color: Colors.grey.shade400),
                    ),
                  ],
                ),
                const SizedBox(height: 3),
                Text(
                  msg.descripcion ?? '',
                  style: const TextStyle(fontSize: 13, height: 1.4),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyView extends StatelessWidget {
  const _EmptyView();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.notifications_none_rounded,
              size: 56, color: Colors.grey.shade300),
          const SizedBox(height: 12),
          Text(
            'Sin notificaciones',
            style: TextStyle(fontSize: 14, color: Colors.grey.shade500),
          ),
        ],
      ),
    );
  }
}