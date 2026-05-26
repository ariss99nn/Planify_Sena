import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/auth_provider.dart';
import '../../../core/api/api_service.dart';
import '../../../core/theme/theme.dart';

class VerifyEmailScreen extends StatefulWidget {
  final String email;

  const VerifyEmailScreen({super.key, required this.email});

  @override
  State<VerifyEmailScreen> createState() => _VerifyEmailScreenState();
}

class _VerifyEmailScreenState extends State<VerifyEmailScreen> {
  final codeCtrl = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool loading   = false;
  bool resending = false;

  Future<void> verify() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => loading = true);

    try {
      // ✅ Usa AuthProvider — no llama ApiService directamente
      await context.read<AuthProvider>().verifyEmail(
            email: widget.email,
            code:  codeCtrl.text.trim(),
          );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Correo verificado correctamente. Inicia sesión.'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );

      // ✅ Limpiar stack — no volver atrás sino ir al login
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

  Future<void> resendCode() async {
    setState(() => resending = true);

    try {
      // ✅ Endpoint correcto: resend-verification, no resend-code
      await context.read<AuthProvider>().resendVerification(widget.email);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Nuevo código enviado a tu correo.'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('No se pudo reenviar el código.'),
          backgroundColor: Colors.red.shade700,
          behavior: SnackBarBehavior.floating,
        ),
      );
    } finally {
      if (mounted) setState(() => resending = false);
    }
  }

  @override
  void dispose() {
    codeCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Verificar Email')),
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
                      const Icon(Icons.verified_outlined,
                          size: 80, color: AppTheme.greenPrimary),
                      const SizedBox(height: 16),

                      Text(
                        'Verifica tu correo',
                        style: Theme.of(context)
                            .textTheme
                            .headlineMedium
                            ?.copyWith(fontSize: 24),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 12),

                      const Text(
                        'Ingresa el código de 6 dígitos que enviamos a:',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 14, color: Color(0xFF558B5A)),
                      ),
                      const SizedBox(height: 8),

                      // Email destacado
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: AppTheme.greenSoft,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: AppTheme.greenLight),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.email_outlined,
                                size: 18, color: AppTheme.greenPrimary),
                            const SizedBox(width: 8),
                            Flexible(
                              child: Text(
                                widget.email,
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.greenPrimary,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 32),

                      TextFormField(
                        controller: codeCtrl,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Código de verificación',
                          hintText: 'Ej: 123456',
                          prefixIcon: Icon(Icons.pin_outlined),
                        ),
                        validator: (v) {
                          if (v == null || v.isEmpty) return 'Ingresa el código';
                          if (v.length != 6) return 'Debe tener 6 dígitos';
                          return null;
                        },
                      ),
                      const SizedBox(height: 25),

                      ElevatedButton(
                        onPressed: loading ? null : verify,
                        child: loading
                            ? const SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : const Text('Verificar'),
                      ),
                      const SizedBox(height: 12),

                      TextButton.icon(
                        onPressed: resending ? null : resendCode,
                        icon: resending
                            ? const SizedBox(
                                height: 16,
                                width: 16,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : const Icon(Icons.refresh_outlined,
                                size: 18, color: AppTheme.greenPrimary),
                        label: Text(
                          resending ? 'Reenviando...' : 'Reenviar código',
                          style: const TextStyle(color: AppTheme.greenPrimary),
                        ),
                      ),
                      const SizedBox(height: 8),

                      TextButton(
                        onPressed: () => Navigator.pushNamedAndRemoveUntil(
                            context, '/login', (_) => false),
                        style: TextButton.styleFrom(
                            foregroundColor: Colors.grey.shade600),
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