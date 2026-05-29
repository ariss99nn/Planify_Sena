import 'package:flutter/material.dart';
import '../../../core/theme/theme.dart';
import '../models/alerta_model.dart';
import '../services/alerta_service.dart';
import '../widgets/alerta_card.dart';
import '../widgets/alerta_filter_chips.dart';

class AlertasScreen extends StatefulWidget {
  const AlertasScreen({super.key});

  @override
  State<AlertasScreen> createState() => _AlertasScreenState();
}

class _AlertasScreenState extends State<AlertasScreen> {
  List<AlertaModel> _alertas = [];
  bool _loading = true;
  String? _error;
  String? _filtroEstado;
  String? _filtroTipo;

  @override
  void initState() {
    super.initState();
    _cargar();
  }

  Future<void> _cargar() async {
    setState(() { _loading = true; _error = null; });
    try {
      final result = await AlertaService.listar(
        estado: _filtroEstado,
        tipo: _filtroTipo,
      );
      setState(() { _alertas = result; _loading = false; });
    } catch (e) {
      setState(() { _error = e.toString(); _loading = false; });
    }
  }

  Future<void> _marcarLeida(AlertaModel alerta) async {
    if (alerta.isLeida) return;
    try {
      final updated = await AlertaService.marcarLeida(alerta.id);
      setState(() {
        final idx = _alertas.indexWhere((a) => a.id == alerta.id);
        if (idx != -1) _alertas[idx] = updated;
      });
    } catch (_) {
      // silencioso — el usuario puede reintentar
    }
  }

  int get _noLeidas => _alertas.where((a) => !a.isLeida).length;

  List<AlertaModel> get _hoy {
    final now = DateTime.now();
    return _alertas.where((a) =>
      a.fechaCreacion.year == now.year &&
      a.fechaCreacion.month == now.month &&
      a.fechaCreacion.day == now.day,
    ).toList();
  }

  List<AlertaModel> get _anteriores {
    final now = DateTime.now();
    return _alertas.where((a) =>
      !(a.fechaCreacion.year == now.year &&
        a.fechaCreacion.month == now.month &&
        a.fechaCreacion.day == now.day),
    ).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alertas'),
        actions: [
          if (_noLeidas > 0)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.25),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '$_noLeidas nuevas',
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          AlertaFilterChips(
            filtroEstado: _filtroEstado,
            filtroTipo: _filtroTipo,
            onEstadoChanged: (v) {
              setState(() => _filtroEstado = v);
              _cargar();
            },
            onTipoChanged: (v) {
              setState(() => _filtroTipo = v);
              _cargar();
            },
          ),
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _error != null
                    ? _ErrorView(error: _error!, onRetry: _cargar)
                    : _alertas.isEmpty
                        ? const _EmptyView()
                        : RefreshIndicator(
                            onRefresh: _cargar,
                            color: AppTheme.greenPrimary,
                            child: ListView(
                              padding: const EdgeInsets.all(12),
                              children: [
                                if (_hoy.isNotEmpty) ...[
                                  _SectionLabel(label: 'Hoy'),
                                  ..._hoy.map((a) => AlertaCard(
                                    alerta: a,
                                    onTap: () => _marcarLeida(a),
                                  )),
                                ],
                                if (_anteriores.isNotEmpty) ...[
                                  _SectionLabel(label: 'Anteriores'),
                                  ..._anteriores.map((a) => AlertaCard(
                                    alerta: a,
                                    onTap: () => _marcarLeida(a),
                                  )),
                                ],
                              ],
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  final String label;
  const _SectionLabel({required this.label});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 8, bottom: 4),
      child: Text(
        label.toUpperCase(),
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.8,
          color: Colors.grey.shade500,
        ),
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
              size: 56, color: AppTheme.greenPrimary.withOpacity(0.4)),
          const SizedBox(height: 12),
          Text(
            'Sin alertas',
            style: Theme.of(context)
                .textTheme
                .bodyMedium
                ?.copyWith(color: Colors.grey.shade500),
          ),
        ],
      ),
    );
  }
}

class _ErrorView extends StatelessWidget {
  final String error;
  final VoidCallback onRetry;
  const _ErrorView({required this.error, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.error_outline, size: 48, color: Colors.redAccent),
          const SizedBox(height: 8),
          Text(error,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 13)),
          const SizedBox(height: 16),
          ElevatedButton(onPressed: onRetry, child: const Text('Reintentar')),
        ],
      ),
    );
  }
}