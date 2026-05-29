import 'package:flutter/material.dart';
import '../../../core/theme/theme.dart';

class AlertaFilterChips extends StatelessWidget {
  final String? filtroEstado;
  final String? filtroTipo;
  final ValueChanged<String?> onEstadoChanged;
  final ValueChanged<String?> onTipoChanged;

  const AlertaFilterChips({
    super.key,
    this.filtroEstado,
    this.filtroTipo,
    required this.onEstadoChanged,
    required this.onTipoChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        child: Row(
          children: [
            _Chip(
              label: 'Todas',
              selected: filtroEstado == null && filtroTipo == null,
              onTap: () {
                onEstadoChanged(null);
                onTipoChanged(null);
              },
            ),
            _Chip(
              label: 'Pendientes',
              selected: filtroEstado == 'PENDIENTE',
              onTap: () => onEstadoChanged(
                filtroEstado == 'PENDIENTE' ? null : 'PENDIENTE',
              ),
            ),
            _Chip(
              label: 'Conflictos',
              selected: filtroTipo == 'CONFLICTO',
              onTap: () => onTipoChanged(
                filtroTipo == 'CONFLICTO' ? null : 'CONFLICTO',
              ),
            ),
            _Chip(
              label: 'Leídas',
              selected: filtroEstado == 'LEIDA',
              onTap: () => onEstadoChanged(
                filtroEstado == 'LEIDA' ? null : 'LEIDA',
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Chip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _Chip({required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(right: 6),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: selected ? AppTheme.greenSoft : Colors.white,
          border: Border.all(
            color: selected ? AppTheme.greenPrimary : Colors.grey.shade300,
            width: 0.5,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w500,
            color: selected ? AppTheme.greenPrimary : Colors.grey.shade600,
          ),
        ),
      ),
    );
  }
}