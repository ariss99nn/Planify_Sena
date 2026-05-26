import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/theme.dart';
import '../providers/aula_provider.dart';
import '../models/aula.dart';

class AulaFormScreen extends StatefulWidget {
  /// null → crear, non-null → editar
  final Aula? aula;
  const AulaFormScreen({super.key, this.aula});

  @override
  State<AulaFormScreen> createState() => _AulaFormScreenState();
}

class _AulaFormScreenState extends State<AulaFormScreen> {
  final _formKey = GlobalKey<FormState>();

  late final TextEditingController _codigoCtrl;
  late final TextEditingController _capacidadCtrl;
  late final TextEditingController _descripcionCtrl;

  String? _tipoAula;
  String? _estado;
  int?    _bloqueId;

  bool get _isEdit => widget.aula != null;

  static const _tipos = [
    ('LAB', 'Laboratorio'),
    ('TEO', 'Teórica'),
    ('SIS', 'Sistemas de Información'),
    ('OTR', 'Otro'),
  ];
  static const _estados = [
    ('ACT',  'Activa'),
    ('MANT', 'Mantenimiento'),
    ('INAC', 'Inactiva'),
  ];

  @override
  void initState() {
    super.initState();
    final a = widget.aula;
    _codigoCtrl     = TextEditingController(text: a?.codigoAula ?? '');
    _capacidadCtrl  = TextEditingController(
        text: a != null ? a.capacidad.toString() : '');
    _descripcionCtrl = TextEditingController(text: a?.descripcion ?? '');
    _tipoAula = a?.tipoAula;
    _estado   = a?.estado ?? 'ACT';
    _bloqueId = a?.bloque.id;

    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AulaProvider>()
        ..resetForm()
        ..fetchBloques();
    });
  }

  @override
  void dispose() {
    _codigoCtrl.dispose();
    _capacidadCtrl.dispose();
    _descripcionCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final body = <String, dynamic>{
      if (!_isEdit) 'codigo_aula': _codigoCtrl.text.trim(),
      'capacidad':   int.parse(_capacidadCtrl.text.trim()),
      'tipo_aula':   _tipoAula,
      'estado':      _estado,
      'bloque':      _bloqueId,
      'descripcion': _descripcionCtrl.text.trim(),
    };

    final provider = context.read<AulaProvider>();
    final ok = _isEdit
        ? await provider.updateAula(widget.aula!.id, body)
        : await provider.createAula(body);

    if (!mounted) return;
    if (ok) {
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(_isEdit ? 'Aula actualizada.' : 'Aula creada.'),
          backgroundColor: AppTheme.greenPrimary,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider   = context.watch<AulaProvider>();
    final isLoading  = provider.formStatus == AulaStatus.loading;
    // inputDecorationTheme global cubre border, fill y colores — no se repite aquí

    return Scaffold(
      appBar: AppBar(
        title: Text(_isEdit ? 'Editar aula' : 'Nueva aula'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Banner de error del servidor
              if (provider.formStatus == AulaStatus.error)
                _ErrorBanner(message: provider.formError),

              // Código (solo creación)
              if (!_isEdit) ...[
                const _Label('Código del aula'),
                TextFormField(
                  controller: _codigoCtrl,
                  textCapitalization: TextCapitalization.characters,
                  decoration:
                      const InputDecoration(hintText: 'Ej. A-101'),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? 'Campo requerido' : null,
                ),
                const SizedBox(height: 16),
              ],

              // Capacidad
              const _Label('Capacidad (personas)'),
              TextFormField(
                controller: _capacidadCtrl,
                keyboardType: TextInputType.number,
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                decoration: const InputDecoration(hintText: 'Ej. 30'),
                validator: (v) {
                  if (v == null || v.isEmpty) return 'Campo requerido';
                  final n = int.tryParse(v);
                  if (n == null || n <= 0) return 'Debe ser mayor a 0';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Tipo de aula
              const _Label('Tipo de aula'),
              DropdownButtonFormField<String>(
                value: _tipoAula,
                decoration:
                    const InputDecoration(hintText: 'Selecciona un tipo'),
                items: _tipos
                    .map((e) =>
                        DropdownMenuItem(value: e.$1, child: Text(e.$2)))
                    .toList(),
                onChanged: (v) => setState(() => _tipoAula = v),
                validator: (v) => v == null ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),

              // Estado
              const _Label('Estado'),
              DropdownButtonFormField<String>(
                value: _estado,
                decoration:
                    const InputDecoration(hintText: 'Selecciona el estado'),
                items: _estados
                    .map((e) =>
                        DropdownMenuItem(value: e.$1, child: Text(e.$2)))
                    .toList(),
                onChanged: (v) => setState(() => _estado = v),
                validator: (v) => v == null ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),

              // Bloque
              const _Label('Bloque'),
              if (provider.bloquesStatus == AulaStatus.loading)
                const Center(child: CircularProgressIndicator())
              else
                DropdownButtonFormField<int>(
                  value: _bloqueId,
                  decoration:
                      const InputDecoration(hintText: 'Selecciona un bloque'),
                  items: provider.bloques
                      .map((b) =>
                          DropdownMenuItem(value: b.id, child: Text(b.nombre)))
                      .toList(),
                  onChanged: (v) => setState(() => _bloqueId = v),
                  validator: (v) => v == null ? 'Campo requerido' : null,
                ),
              const SizedBox(height: 16),

              // Descripción
              const _Label('Descripción (opcional)'),
              TextFormField(
                controller: _descripcionCtrl,
                maxLines: 3,
                decoration:
                    const InputDecoration(hintText: 'Descripción del aula…'),
              ),
              const SizedBox(height: 28),

              // Submit — usa ElevatedButton para heredar elevatedButtonTheme global
              ElevatedButton(
                onPressed: isLoading ? null : _submit,
                child: isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white),
                      )
                    : Text(_isEdit ? 'Guardar cambios' : 'Crear aula'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ── Widgets auxiliares ────────────────────────────────────────────────────────

class _Label extends StatelessWidget {
  final String text;
  const _Label(this.text);

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 6),
        child: Text(
          text,
          style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
        ),
      );
}

class _ErrorBanner extends StatelessWidget {
  final String? message;
  const _ErrorBanner({this.message});

  @override
  Widget build(BuildContext context) {
    // Usa colorScheme.error y errorContainer en lugar de Colors.red hardcodeado
    final cs = Theme.of(context).colorScheme;
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: cs.errorContainer,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: cs.error),
      ),
      child: Row(
        children: [
          Icon(Icons.error_outline, color: cs.error, size: 18),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              message ?? 'Ocurrió un error. Intenta de nuevo.',
              style: TextStyle(color: cs.onErrorContainer, fontSize: 13),
            ),
          ),
        ],
      ),
    );
  }
}