import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/theme.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/aula_provider.dart';
import '../models/aula.dart';
import 'aula_detail_screen.dart';
import 'aula_form_screen.dart';

// Colores de estado precalculados — evita withOpacity() en runtime
// y es consistente con el patrón de AppTheme.greenSoftFill
const _kActivaBg    = Color(0xFFE8F5E9); // green.shade50
const _kActivaFg    = Color(0xFF2E7D32); // green.shade800
const _kMantBg      = Color(0xFFFFF3E0); // orange.shade50
const _kMantFg      = Color(0xFFE65100); // orange.shade900
const _kInacBg      = Color(0xFFFFEBEE); // red.shade50
const _kInacFg      = Color(0xFFC62828); // red.shade800

class AulaListScreen extends StatefulWidget {
  const AulaListScreen({super.key});

  @override
  State<AulaListScreen> createState() => _AulaListScreenState();
}

class _AulaListScreenState extends State<AulaListScreen> {
  final _searchCtrl = TextEditingController();
  String? _estadoFiltro;
  String? _tipoFiltro;

  static const _estados = [
    ('ACT',  'Activa'),
    ('MANT', 'Mantenimiento'),
    ('INAC', 'Inactiva'),
  ];
  static const _tipos = [
    ('LAB', 'Laboratorio'),
    ('TEO', 'Teórica'),
    ('SIS', 'Sistemas'),
    ('OTR', 'Otro'),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AulaProvider>().fetchAulas();
    });
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  void _applyFiltros() {
    context.read<AulaProvider>().setFiltros(
          search: _searchCtrl.text.trim(),
          estado: _estadoFiltro,
          tipo: _tipoFiltro,
        );
  }

  void _clearFiltros() {
    _searchCtrl.clear();
    setState(() {
      _estadoFiltro = null;
      _tipoFiltro = null;
    });
    context.read<AulaProvider>().clearFiltros();
  }

  @override
  Widget build(BuildContext context) {
    final rol = context.watch<AuthProvider>().user?.rol ?? '';
    final canWrite = rol == 'COORDINADOR' || rol == 'ADMINISTRATIVO';

    return Scaffold(
      appBar: AppBar(
        title: const Text('Aulas'),
        // AppBar usa appBarTheme del theme global — no hace falta repetir colores
        actions: [
          if (canWrite)
            IconButton(
              icon: const Icon(Icons.add),
              tooltip: 'Nueva aula',
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AulaFormScreen()),
              ).then((_) => context.read<AulaProvider>().fetchAulas()),
            ),
        ],
      ),
      body: Column(
        children: [
          _FiltrosBar(
            searchCtrl: _searchCtrl,
            estadoFiltro: _estadoFiltro,
            tipoFiltro: _tipoFiltro,
            estados: _estados,
            tipos: _tipos,
            onEstadoChanged: (v) => setState(() => _estadoFiltro = v),
            onTipoChanged:   (v) => setState(() => _tipoFiltro = v),
            onApply: _applyFiltros,
            onClear: _clearFiltros,
          ),
          Expanded(child: _AulaListBody(canWrite: canWrite)),
        ],
      ),
    );
  }
}

// ── Barra de filtros ──────────────────────────────────────────────────────────

class _FiltrosBar extends StatelessWidget {
  final TextEditingController searchCtrl;
  final String? estadoFiltro;
  final String? tipoFiltro;
  final List<(String, String)> estados;
  final List<(String, String)> tipos;
  final ValueChanged<String?> onEstadoChanged;
  final ValueChanged<String?> onTipoChanged;
  final VoidCallback onApply;
  final VoidCallback onClear;

  const _FiltrosBar({
    required this.searchCtrl,
    required this.estadoFiltro,
    required this.tipoFiltro,
    required this.estados,
    required this.tipos,
    required this.onEstadoChanged,
    required this.onTipoChanged,
    required this.onApply,
    required this.onClear,
  });

  @override
  Widget build(BuildContext context) {
    // surface del colorScheme en lugar de Colors.grey.shade50 hardcodeado
    final surface = Theme.of(context).colorScheme.surface;

    return Container(
      color: surface,
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
      child: Column(
        children: [
          TextField(
            controller: searchCtrl,
            decoration: const InputDecoration(
              hintText: 'Buscar por código, bloque o descripción…',
              prefixIcon: Icon(Icons.search),
              // border, filled y fillColor vienen del inputDecorationTheme global
            ),
            onSubmitted: (_) => onApply(),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _DropdownFiltro<String>(
                  hint: 'Estado',
                  value: estadoFiltro,
                  items: estados.map((e) => (e.$1, e.$2)).toList(),
                  onChanged: onEstadoChanged,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _DropdownFiltro<String>(
                  hint: 'Tipo',
                  value: tipoFiltro,
                  items: tipos.map((e) => (e.$1, e.$2)).toList(),
                  onChanged: onTipoChanged,
                ),
              ),
              const SizedBox(width: 8),
              FilledButton(
                onPressed: onApply,
                style: FilledButton.styleFrom(
                  backgroundColor: AppTheme.greenPrimary,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                ),
                child: const Text('Filtrar'),
              ),
              const SizedBox(width: 4),
              IconButton(
                icon: const Icon(Icons.clear),
                tooltip: 'Limpiar filtros',
                onPressed: onClear,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _DropdownFiltro<T> extends StatelessWidget {
  final String hint;
  final T? value;
  final List<(T, String)> items;
  final ValueChanged<T?> onChanged;

  const _DropdownFiltro({
    required this.hint,
    required this.value,
    required this.items,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<T>(
      value: value,
      hint: Text(hint, style: const TextStyle(fontSize: 13)),
      isDense: true,
      // decoration hereda inputDecorationTheme; solo ajustamos padding
      decoration: const InputDecoration(
        contentPadding: EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      ),
      items: [
        DropdownMenuItem<T>(
          value: null,
          child: Text('Todos', style: TextStyle(fontSize: 13)),
        ),
        ...items.map((e) => DropdownMenuItem<T>(
              value: e.$1,
              child: Text(e.$2, style: const TextStyle(fontSize: 13)),
            )),
      ],
      onChanged: onChanged,
    );
  }
}

// ── Cuerpo ────────────────────────────────────────────────────────────────────

class _AulaListBody extends StatelessWidget {
  final bool canWrite;
  const _AulaListBody({required this.canWrite});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AulaProvider>();
    final colorScheme = Theme.of(context).colorScheme;

    return switch (provider.listStatus) {
      AulaStatus.loading || AulaStatus.idle => Center(
          child: CircularProgressIndicator(color: AppTheme.greenPrimary),
        ),
      AulaStatus.error => Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.error_outline, size: 48, color: colorScheme.error),
              const SizedBox(height: 12),
              Text(provider.listError ?? 'Error desconocido'),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: () => context.read<AulaProvider>().fetchAulas(),
                child: const Text('Reintentar'),
              ),
            ],
          ),
        ),
      AulaStatus.success when provider.aulas.isEmpty => Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.meeting_room_outlined,
                  size: 64, color: colorScheme.outlineVariant),
              const SizedBox(height: 12),
              Text('No hay aulas',
                  style: TextStyle(color: colorScheme.onSurfaceVariant)),
            ],
          ),
        ),
      _ => RefreshIndicator(
          color: AppTheme.greenPrimary,
          onRefresh: () => context.read<AulaProvider>().fetchAulas(),
          child: ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: provider.aulas.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (ctx, i) =>
                _AulaCard(aula: provider.aulas[i], canWrite: canWrite),
          ),
        ),
    };
  }
}

// ── Card ──────────────────────────────────────────────────────────────────────

class _AulaCard extends StatelessWidget {
  final AulaResumen aula;
  final bool canWrite;
  const _AulaCard({required this.aula, required this.canWrite});

  // Colores precalculados — sin withOpacity() en runtime
  ({Color bg, Color fg}) _estadoColors(String estado) => switch (estado) {
        'ACT'  => (bg: _kActivaBg, fg: _kActivaFg),
        'MANT' => (bg: _kMantBg,   fg: _kMantFg),
        'INAC' => (bg: _kInacBg,   fg: _kInacFg),
        _      => (bg: const Color(0xFFF5F5F5), fg: const Color(0xFF616161)),
      };

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final colores = _estadoColors(aula.estado);

    return Card(
      // elevation y shape vienen del cardTheme global
      child: InkWell(
        borderRadius: BorderRadius.circular(24),
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => AulaDetailScreen(aulaId: aula.id),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: AppTheme.greenSoft,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Icon(Icons.meeting_room, color: AppTheme.greenPrimary),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      aula.codigoAula,
                      style: const TextStyle(
                          fontWeight: FontWeight.w700, fontSize: 16),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '${aula.bloqueNombre} · ${aula.tipoAulaDisplay}',
                      style: TextStyle(
                          fontSize: 13, color: cs.onSurfaceVariant),
                    ),
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        Icon(Icons.people_outline,
                            size: 14, color: cs.onSurfaceVariant),
                        const SizedBox(width: 4),
                        Text(
                          '${aula.capacidad} personas',
                          style: TextStyle(
                              fontSize: 12, color: cs.onSurfaceVariant),
                        ),
                        const SizedBox(width: 12),
                        // Badge sin withOpacity
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: colores.bg,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            aula.estadoDisplay,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: colores.fg,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, color: cs.outlineVariant),
            ],
          ),
        ),
      ),
    );
  }
}