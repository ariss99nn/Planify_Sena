import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/auth_provider.dart';
import '../../../core/api/api_service.dart';
import '../../../core/theme/theme.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final nombreCtrl   = TextEditingController();
  final apellidoCtrl = TextEditingController();  // ✅ campo nuevo
  final emailCtrl    = TextEditingController();
  final passCtrl     = TextEditingController();
  final pass2Ctrl    = TextEditingController();

  final _formKey = GlobalKey<FormState>();
  bool loading   = false;

  Future<void> register() async {
  if (!_formKey.currentState!.validate()) return;
  setState(() => loading = true);

  try {
    await context.read<AuthProvider>().register(
          nombre:    nombreCtrl.text.trim(),
          apellido:  apellidoCtrl.text.trim(),
          email:     emailCtrl.text.trim(),
          password:  passCtrl.text,
          password2: pass2Ctrl.text,
        );

    if (!mounted) return;

    // ✅ Navegar manualmente — RegisterScreen no está dentro de AuthGuard
    Navigator.pushNamedAndRemoveUntil(
      context,
      '/verify-email',
      (_) => false,
      arguments: emailCtrl.text.trim().toLowerCase(),
    );

  } on ApiException catch (e) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(e.message),
        backgroundColor: Colors.red.shade700,
      ),
    );
  } catch (_) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Error al registrar. Intenta nuevamente.'),
        backgroundColor: Colors.red.shade700,
      ),
    );
  } finally {
    if (mounted) setState(() => loading = false);
  }
}

  @override
  void dispose() {
    nombreCtrl.dispose();
    apellidoCtrl.dispose();
    emailCtrl.dispose();
    passCtrl.dispose();
    pass2Ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Registro')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(28),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Icon(Icons.person_add_alt_1,
                          size: 64, color: AppTheme.greenPrimary),
                      const SizedBox(height: 16),

                      Text(
                        'Crear cuenta',
                        textAlign: TextAlign.center,
                        style: Theme.of(context)
                            .textTheme
                            .headlineMedium
                            ?.copyWith(fontSize: 26),
                      ),
                      const Text(
                        'Regístrate para comenzar',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 14, color: Color(0xFF558B5A)),
                      ),
                      const SizedBox(height: 30),

                      // NOMBRE
                      TextFormField(
                        controller: nombreCtrl,
                        textCapitalization: TextCapitalization.words,
                        decoration: const InputDecoration(
                          labelText: 'Nombre',
                          prefixIcon: Icon(Icons.person_outline),
                        ),
                        validator: (v) =>
                            v == null || v.trim().isEmpty ? 'Ingresa tu nombre' : null,
                      ),
                      const SizedBox(height: 15),

                      // APELLIDO ✅
                      TextFormField(
                        controller: apellidoCtrl,
                        textCapitalization: TextCapitalization.words,
                        decoration: const InputDecoration(
                          labelText: 'Apellido',
                          prefixIcon: Icon(Icons.person_outline),
                        ),
                        validator: (v) =>
                            v == null || v.trim().isEmpty ? 'Ingresa tu apellido' : null,
                      ),
                      const SizedBox(height: 15),

                      // EMAIL
                      TextFormField(
                        controller: emailCtrl,
                        keyboardType: TextInputType.emailAddress,
                        decoration: const InputDecoration(
                          labelText: 'Correo electrónico',
                          prefixIcon: Icon(Icons.email_outlined),
                        ),
                        validator: (v) {
                          if (v == null || v.trim().isEmpty) return 'Ingresa tu email';
                          if (!v.contains('@')) return 'Email inválido';
                          return null;
                        },
                      ),
                      const SizedBox(height: 15),

                      // PASSWORD
                      TextFormField(
                        controller: passCtrl,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'Contraseña',
                          prefixIcon: Icon(Icons.lock_outline),
                        ),
                        // ✅ mínimo 8 — alineado con el validador del backend
                        validator: (v) =>
                            v == null || v.length < 8 ? 'Mínimo 8 caracteres' : null,
                      ),
                      const SizedBox(height: 15),

                      // CONFIRM PASSWORD
                      TextFormField(
                        controller: pass2Ctrl,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'Confirmar contraseña',
                          prefixIcon: Icon(Icons.lock_outline),
                        ),
                        validator: (v) =>
                            v != passCtrl.text ? 'Las contraseñas no coinciden' : null,
                      ),
                      const SizedBox(height: 25),

                      ElevatedButton(
                        onPressed: loading ? null : register,
                        child: loading
                            ? const SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : const Text('Registrar'),
                      ),
                      const SizedBox(height: 20),

                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('¿Ya tienes cuenta? Inicia sesión'),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}