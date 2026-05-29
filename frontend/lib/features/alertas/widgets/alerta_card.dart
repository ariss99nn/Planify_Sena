import 'package:flutter/material.dart';
import '../../../core/theme/theme.dart';
import '../models/alerta_model.dart';

class AlertaCard extends StatelessWidget {
  final AlertaModel alerta;
  final VoidCallback? onTap;

  const AlertaCard({super.key, required this.alerta, this.onTap});

  @override
  Widget build(BuildContext context) {
    final isUnread = !alerta.isLeida;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border(
            left: isUnread
                ? const BorderSide(color: AppTheme.greenPrimary, width: 3)
                : BorderSide.none,
            top: BorderSide(color: Colors.grey.shade200, width: 0.5),
            right: BorderSide(color: Colors.grey.shade200, width: 0.5),
            bottom: BorderSide(color: Colors.grey.shade200, width: 0.5),
          ),
        ),
        child: Padding(
          padding: EdgeInsets.fromLTRB(isUnread ? 10 : 12, 12, 12, 12),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _IconBubble(tipo: alerta.tipo),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          alerta.tipoDisplay,
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: _tipoColor(alerta.tipo),
                          ),
                        ),
                        const Spacer(),
                        Text(
                          _formatTime(alerta.fechaCreacion),
                          style: TextStyle(
                            fontSize: 11,
                            color: Colors.grey.shade400,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 3),
                    Text(
                      alerta.descripcion,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 13, height: 1.4),
                    ),
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        _EstadoBadge(estado: alerta.estado, display: alerta.estadoDisplay),
                        const Spacer(),
                        if (alerta.destinatarioNombre != null)
                          Row(
                            children: [
                              Icon(Icons.person_outline,
                                  size: 11, color: Colors.grey.shade400),
                              const SizedBox(width: 2),
                              Text(
                                alerta.destinatarioNombre!,
                                style: TextStyle(
                                    fontSize: 11, color: Colors.grey.shade400),
                              ),
                            ],
                          ),
                      ],
                    ),
                  ],
                ),
              ),
              if (isUnread) ...[
                const SizedBox(width: 6),
                Container(
                  width: 7,
                  height: 7,
                  margin: const EdgeInsets.only(top: 4),
                  decoration: const BoxDecoration(
                    color: AppTheme.greenPrimary,
                    shape: BoxShape.circle,
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  String _formatTime(DateTime dt) {
    final now = DateTime.now();
    if (dt.year == now.year && dt.month == now.month && dt.day == now.day) {
      return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    }
    return '${dt.day}/${dt.month}';
  }

  Color _tipoColor(TipoAlerta tipo) => switch (tipo) {
    TipoAlerta.CONFLICTO      => const Color(0xFFA32D2D),
    TipoAlerta.DISPONIBILIDAD => const Color(0xFF185FA5),
    TipoAlerta.SISTEMA        => const Color(0xFF854F0B),
  };
}

class _IconBubble extends StatelessWidget {
  final TipoAlerta tipo;
  const _IconBubble({required this.tipo});

  @override
  Widget build(BuildContext context) {
    final (icon, bg, fg) = switch (tipo) {
      TipoAlerta.CONFLICTO      => (Icons.warning_amber_rounded,
                                    const Color(0xFFFCEBEB), const Color(0xFFA32D2D)),
      TipoAlerta.DISPONIBILIDAD => (Icons.calendar_today_outlined,
                                    const Color(0xFFE6F1FB), const Color(0xFF185FA5)),
      TipoAlerta.SISTEMA        => (Icons.settings_outlined,
                                    const Color(0xFFFAEEDA), const Color(0xFF854F0B)),
    };
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(color: bg, shape: BoxShape.circle),
      child: Icon(icon, size: 18, color: fg),
    );
  }
}

class _EstadoBadge extends StatelessWidget {
  final EstadoAlerta estado;
  final String display;
  const _EstadoBadge({required this.estado, required this.display});

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = switch (estado) {
      EstadoAlerta.PENDIENTE => (const Color(0xFFFAEEDA), const Color(0xFF854F0B)),
      EstadoAlerta.ENVIADA   => (const Color(0xFFE6F1FB), const Color(0xFF185FA5)),
      EstadoAlerta.LEIDA     => (const Color(0xFFF1EFE8), const Color(0xFF5F5E5A)),
    };
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(12)),
      child: Text(display, style: TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: fg)),
    );
  }
}