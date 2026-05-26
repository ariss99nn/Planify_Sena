import 'package:flutter/material.dart';

import '../services/auth_service.dart';
import '../../../core/api/api_service.dart';
import '../../../core/theme/theme.dart';

/// Pantalla que recibe el token desde el deep link:
/// /reset-password?token=<uuid>
/// Configurar en AndroidManifest / Info.plist el esquema de URL.
class ResetPasswordScreen extends StatefulWidget {
  const ResetPasswordScreen({super.key});

  @override
  State<ResetPasswordScreen> createState() => _ResetPasswordScreenState();
}

class _ResetPasswordScreenState extends State<ResetPasswordScreen> {
  final tokenCtrl  = TextEditingController();
  final passCtrl   = TextEditingController();
  final pass2Ctrl  = TextEditingController();
  final _formKey   = GlobalKey<FormState>();

  bool loading = false;
  bool obscure1 = true;
  bool obscure2 = true;

  @override
    void didChangeDependencies() {
        super.didChangeDependencies();

  // 1. Desde arguments (navegación interna)
  final args = ModalRoute.of(context)?.settings.arguments;
  if (args is String && args.isNotEmpty) {
    tokenCtrl.text = args;
    return;
  }

  // 2. Desde el fragment de la URL del navegador
  // URL: http://localhost:3000/#/reset-password/TOKEN
  final fragment = Uri.base.fragment; // → /reset-password/TOKEN
  final parts = fragment.split('/');  // → ['', 'reset-password', 'TOKEN']
  if (parts.length >= 3 && parts[parts.length - 2] == 'reset-password') {
    tokenCtrl.text = parts.last;
  }
}

  Future<void> resetPassword() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => loading = true);

    try {
      await AuthService.confirmPasswordReset(
        token:    tokenCtrl.text.trim(),
        password: passCtrl.text,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Contraseña actualizada. Inicia sesión.'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );

      Navigator.pushNamedAndRemoveUntil(context, '/login', (_) => false);
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.message),
          backgroundColor: Colors.red.shade700,
          behavior: SnackBarBehavior.floating,
        ),
      );
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  void dispose() {
    tokenCtrl.dispose();
    passCtrl.dispose();
    pass2Ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Nueva contraseña')),
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
                      const Icon(Icons.lock_reset, size: 64, color: AppTheme.greenPrimary),
                      const SizedBox(height: 16),

                      Text(
                        'Restablecer contraseña',
                        textAlign: TextAlign.center,
                        style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontSize: 22),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        'Ingresa el token recibido por correo y tu nueva contraseña.',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 14, color: Color(0xFF558B5A)),
                      ),
                      const SizedBox(height: 28),

                      // TOKEN
                      TextFormField(
                        controller: tokenCtrl,
                        decoration: const InputDecoration(
                          labelText: 'Token de recuperación',
                          prefixIcon: Icon(Icons.vpn_key_outlined),
                        ),
                        validator: (v) =>
                            v == null || v.trim().isEmpty ? 'Ingresa el token' : null,
                      ),
                      const SizedBox(height: 15),

                      // NUEVA CONTRASEÑA
                      TextFormField(
                        controller: passCtrl,
                        obscureText: obscure1,
                        decoration: InputDecoration(
                          labelText: 'Nueva contraseña',
                          prefixIcon: const Icon(Icons.lock_outline),
                          suffixIcon: IconButton(
                            icon: Icon(obscure1 ? Icons.visibility_off : Icons.visibility),
                            onPressed: () => setState(() => obscure1 = !obscure1),
                          ),
                        ),
                        validator: (v) =>
                            v == null || v.length < 8 ? 'Mínimo 8 caracteres' : null,
                      ),
                      const SizedBox(height: 15),

                      // CONFIRMAR CONTRASEÑA
                      TextFormField(
                        controller: pass2Ctrl,
                        obscureText: obscure2,
                        decoration: InputDecoration(
                          labelText: 'Confirmar contraseña',
                          prefixIcon: const Icon(Icons.lock_outline),
                          suffixIcon: IconButton(
                            icon: Icon(obscure2 ? Icons.visibility_off : Icons.visibility),
                            onPressed: () => setState(() => obscure2 = !obscure2),
                          ),
                        ),
                        validator: (v) =>
                            v != passCtrl.text ? 'Las contraseñas no coinciden' : null,
                      ),
                      const SizedBox(height: 25),

                      ElevatedButton(
                        onPressed: loading ? null : resetPassword,
                        child: loading
                            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
                            : const Text('Restablecer contraseña'),
                      ),
                      const SizedBox(height: 16),

                      TextButton(
                        onPressed: () => Navigator.pushNamedAndRemoveUntil(context, '/login', (_) => false),
                        style: TextButton.styleFrom(foregroundColor: Colors.grey.shade600),
                        child: const Text('← Volver al login'),
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