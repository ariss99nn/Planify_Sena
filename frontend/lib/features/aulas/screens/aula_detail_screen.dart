import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/theme.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/aula_provider.dart';
import '../models/aula.dart';
import 'aula_form_screen.dart';

// Colores de estado precalculados (mismo patrón que aula_list_screen)
const _kActivaBg    = Color(0xFFE8F5E9);
const _kActivaFg    = Color(0xFF2E7D32);
const _kActivaBorder= Color(0xFF81C784);
const _kMantBg      = Color(0xFFFFF3E0);
const _kMantFg      = Color(0xFFE65100);
const _kMantBorder  = Color(0xFFFFB74D);
const _kInacBg      = Color(0xFFFFEBEE);
const _kInacFg      = Color(0xFFC62828);
const _kInacBorder  = Color(0xFFEF9A9A);

class AulaDetailScreen extends StatefulWidget {
  final int aulaId;
  const AulaDetailScreen({super.key, required this.aulaId});

  @override
  State<AulaDetailScreen> createState() => _AulaDetailScreenState();
}

class _AulaDetailScreenState extends State<AulaDetailScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AulaProvider>().fetchAula(widget.aulaId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AulaProvider>();
    final rol = context.watch<AuthProvider>().user?.rol ?? '';
    final canWrite        = rol == 'COORDINADOR' || rol == 'ADMINISTRATIVO';
    final canChangeEstado = canWrite || rol == 'DOCENTE';

    return Scaffold(
      appBar: AppBar(
        title: Text(provider.selected?.codigoAula ?? 'Detalle'),
        actions: [
          if (canWrite && provider.selected != null)
            IconButton(
              icon: const Icon(Icons.edit_outlined),
              tooltip: 'Editar',
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => AulaFormScreen(aula: provider.selected),
                ),
              ).then((_) => context.read<AulaProvider>().fetchAula(widget.aulaId)),
            ),
        ],
      ),
      body: switch (provider.detailStatus) {
        AulaStatus.loading || AulaStatus.idle => const Center(
            child: CircularProgressIndicator(),
          ),
        AulaStatus.error => Center(
            child: Text(provider.detailError ?? 'Error'),
          ),
        AulaStatus.success => _AulaDetailBody(
            aula: provider.selected!,
            canChangeEstado: canChangeEstado,
          ),
      },
    );
  }
}

// ── Cuerpo del detalle ────────────────────────────────────────────────────────

class _AulaDetailBody extends StatelessWidget {
  final Aula aula;
  final bool canChangeEstado;
  const _AulaDetailBody({required this.aula, required this.canChangeEstado});

  static const _estadosOpciones = [
    ('ACT',  'Activa'),
    ('MANT', 'Mantenimiento'),
    ('INAC', 'Inactiva'),
  ];

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Imagen
          if (aula.imagenUrl != null)
            ClipRRect(
              borderRadius: BorderRadius.circular(14),
              child: Image.network(
                aula.imagenUrl!,
                height: 180,
                width: double.infinity,
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => const SizedBox.shrink(),
              ),
            ),
          if (aula.imagenUrl != null) const SizedBox(height: 16),

          // Encabezado + badge de estado
          Row(
            children: [
              Expanded(
                child: Text(
                  aula.codigoAula,
                  style: const TextStyle(
                      fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
              if (canChangeEstado)
                GestureDetector(
                  onTap: () => _showEstadoSheet(context),
                  child: _EstadoBadge(
                      estado: aula.estado, display: aula.estadoDisplay),
                )
              else
                _EstadoBadge(estado: aula.estado, display: aula.estadoDisplay),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            aula.bloque.nombre,
            style: TextStyle(fontSize: 15, color: cs.onSurfaceVariant),
          ),
          const SizedBox(height: 20),
          const Divider(),
          const SizedBox(height: 12),

          _InfoGrid(aula: aula),
          const SizedBox(height: 20),

          // Descripción
          if (aula.descripcion.isNotEmpty) ...[
            const Text('Descripción',
                style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
            const SizedBox(height: 6),
            Text(aula.descripcion,
                style: TextStyle(color: cs.onSurfaceVariant)),
            const SizedBox(height: 20),
          ],

          // Equipamiento
          const Text('Equipamiento',
              style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
          const SizedBox(height: 10),
          if (aula.equipamiento.isEmpty)
            Text('Sin equipamiento asignado',
                style: TextStyle(color: cs.onSurfaceVariant))
          else
            ...aula.equipamiento.map(
              (e) => Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(6),
                      decoration: BoxDecoration(
                        color: AppTheme.greenSoft,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(Icons.devices_other,
                          size: 18, color: AppTheme.greenPrimary),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                        child: Text(e.nombre,
                            style: const TextStyle(fontSize: 14))),
                    Text('x${e.cantidad}',
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    const SizedBox(width: 10),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: cs.surfaceContainerHighest,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(e.estadoDisplay,
                          style: TextStyle(
                              fontSize: 11, color: cs.onSurfaceVariant)),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  void _showEstadoSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Cambiar estado',
                style:
                    TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
            const SizedBox(height: 16),
            ..._estadosOpciones.map(
              (op) => ListTile(
                contentPadding: EdgeInsets.zero,
                leading: Icon(
                  aula.estado == op.$1
                      ? Icons.radio_button_checked
                      : Icons.radio_button_unchecked,
                  color: AppTheme.greenPrimary,
                  size: 20,
                ),
                title: Text(op.$2),
                selected: aula.estado == op.$1,
                selectedColor: AppTheme.greenPrimary,
                onTap: () {
                  Navigator.pop(ctx);
                  context
                      .read<AulaProvider>()
                      .updateEstado(aula.id, op.$1);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Badge de estado ───────────────────────────────────────────────────────────

class _EstadoBadge extends StatelessWidget {
  final String estado;
  final String display;
  const _EstadoBadge({required this.estado, required this.display});

  ({Color bg, Color fg, Color border}) _colors() => switch (estado) {
        'ACT'  => (bg: _kActivaBg, fg: _kActivaFg, border: _kActivaBorder),
        'MANT' => (bg: _kMantBg,   fg: _kMantFg,   border: _kMantBorder),
        'INAC' => (bg: _kInacBg,   fg: _kInacFg,   border: _kInacBorder),
        _      => (
            bg: const Color(0xFFF5F5F5),
            fg: const Color(0xFF616161),
            border: const Color(0xFFBDBDBD),
          ),
      };

  @override
  Widget build(BuildContext context) {
    final c = _colors();
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: c.bg,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: c.border),
      ),
      child: Text(
        display,
        style: TextStyle(
            color: c.fg, fontWeight: FontWeight.w600, fontSize: 13),
      ),
    );
  }
}

// ── Info grid ─────────────────────────────────────────────────────────────────

class _InfoGrid extends StatelessWidget {
  final Aula aula;
  const _InfoGrid({required this.aula});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    final items = [
      (Icons.category_outlined,  'Tipo',              aula.tipoAulaDisplay),
      (Icons.people_outline,     'Capacidad',         '${aula.capacidad} personas'),
      (Icons.business_outlined,  'Bloque',            aula.bloque.nombre),
      (Icons.layers_outlined,    'Pisos del bloque',  '${aula.bloque.piso}'),
    ];

    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 10,
      crossAxisSpacing: 10,
      childAspectRatio: 2.8,
      children: items.map((item) {
        return Container(
          padding:
              const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: BoxDecoration(
            // surfaceContainerLow en lugar de Colors.grey.shade50
            color: cs.surfaceContainerLow,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: cs.outlineVariant),
          ),
          child: Row(
            children: [
              Icon(item.$1, size: 18, color: AppTheme.greenPrimary),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(item.$2,
                        style: TextStyle(
                            fontSize: 10, color: cs.onSurfaceVariant)),
                    Text(item.$3,
                        style: const TextStyle(
                            fontSize: 13, fontWeight: FontWeight.w600),
                        overflow: TextOverflow.ellipsis),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}