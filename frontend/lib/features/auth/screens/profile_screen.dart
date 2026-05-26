import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/auth_provider.dart';
import '../models/user_model.dart';
import '../../../core/theme/theme.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  String _rolLabel(UserModel user) {
    if (user.esAdministrativo) return 'Administrativo';
    if (user.esCoordinador)    return 'Coordinador';
    if (user.esDocente)        return 'Docente';
    return 'Estudiante';
  }

  IconData _rolIcon(UserModel user) {
    if (user.puedeGestionarUsuarios) return Icons.admin_panel_settings;
    if (user.esDocente)              return Icons.school_outlined;
    return Icons.person_outline;
  }

  @override
  Widget build(BuildContext context) {
    final auth        = context.watch<AuthProvider>();
    final UserModel? user = auth.user;

    if (user == null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.warning_amber_rounded,
                  size: 64, color: AppTheme.greenPrimary),
              const SizedBox(height: 16),
              const Text('No hay usuario autenticado',
                  style: TextStyle(fontSize: 18, color: AppTheme.textDark)),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () =>
                    Navigator.pushReplacementNamed(context, '/login'),
                child: const Text('Ir al login'),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Mi Perfil')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(28),
                child: Column(
                  children: [
                    // AVATAR
                    Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border:
                            Border.all(color: AppTheme.greenPrimary, width: 3),
                      ),
                      child: CircleAvatar(
                        radius: 50,
                        backgroundColor: AppTheme.greenSoft,
                        child: ClipOval(
                          child: user.imagenUrl != null &&
                                  user.imagenUrl!.isNotEmpty
                              ? Image.network(
                                  user.imagenUrl!,
                                  width: 100,
                                  height: 100,
                                  fit: BoxFit.cover,
                                  errorBuilder: (_, __, ___) => const Icon(
                                      Icons.person,
                                      size: 60,
                                      color: AppTheme.greenPrimary),
                                )
                              : const Icon(Icons.person,
                                  size: 60, color: AppTheme.greenPrimary),
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // NOMBRE COMPLETO ✅
                    Text(
                      user.nombreCompleto,
                      style: Theme.of(context)
                          .textTheme
                          .headlineMedium
                          ?.copyWith(fontSize: 24),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),

                    // ROL ✅ usando helpers del modelo, no strings hardcodeados
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 6),
                      decoration: BoxDecoration(
                        color: AppTheme.greenSoft,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: AppTheme.greenLight),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(_rolIcon(user),
                              size: 16, color: AppTheme.greenPrimary),
                          const SizedBox(width: 6),
                          Text(
                            _rolLabel(user),
                            style: const TextStyle(
                                color: AppTheme.greenPrimary,
                                fontWeight: FontWeight.w600),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // EMAIL
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.email_outlined,
                            size: 20, color: AppTheme.greenPrimary),
                        const SizedBox(width: 8),
                        Text(user.email,
                            style: const TextStyle(
                                fontSize: 14, color: AppTheme.textDark)),
                      ],
                    ),

                    // BADGE correo no verificado
                    if (!user.emailVerificado) ...[
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.orange.shade50,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.orange.shade300),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.warning_amber_rounded,
                                size: 14, color: Colors.orange.shade700),
                            const SizedBox(width: 4),
                            Text('Correo no verificado',
                                style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.orange.shade700)),
                          ],
                        ),
                      ),
                    ],

                    // MIEMBRO DESDE ✅ usando fecha real del modelo
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.calendar_today,
                            size: 16, color: AppTheme.greenPrimary),
                        const SizedBox(width: 8),
                        Text(
                          'Miembro desde ${user.fechaCreacion.year}',
                          style: const TextStyle(
                              fontSize: 12, color: AppTheme.textDark),
                        ),
                      ],
                    ),

                    const SizedBox(height: 32),

                    ElevatedButton.icon(
                      onPressed: () => auth.logout(),
                      icon: const Icon(Icons.logout),
                      label: const Text('Cerrar sesión'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red.shade600,
                        foregroundColor: AppTheme.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(40)),
                      ),
                    ),
                    const SizedBox(height: 12),

                    TextButton.icon(
                      onPressed: () {
                        // TODO: navegar a editar perfil
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Próximamente: Editar perfil'),
                            backgroundColor: AppTheme.greenPrimary,
                          ),
                        );
                      },
                      icon: const Icon(Icons.edit_outlined,
                          color: AppTheme.greenPrimary),
                      label: const Text('Editar perfil',
                          style: TextStyle(color: AppTheme.greenPrimary)),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}