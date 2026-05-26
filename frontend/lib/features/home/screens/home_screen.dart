import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../auth/providers/auth_provider.dart';
import '../../users/screens/user_list_screen.dart';
import '../../aulas/screens/aula_list_screen.dart';
import '../../../core/theme/theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final user = auth.user;

    if (user == null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.person_off, size: 64, color: AppTheme.greenPrimary),
              const SizedBox(height: 16),
              const Text('No hay sesión activa',
                  style: TextStyle(color: AppTheme.textDark)),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () =>
                    Navigator.pushReplacementNamed(context, '/login'),
                child: const Text('Iniciar sesión'),
              ),
            ],
          ),
        ),
      );
    }

    // ✅ puedeGestionarUsuarios cubre COORDINADOR y ADMINISTRATIVO
    final screens = <Widget>[
      const DashboardView(),
      if (user.puedeGestionarUsuarios) const UserListScreen(),
      if (user.puedeGestionarUsuarios) const AulaListScreen(),
    ];

    final items = <BottomNavigationBarItem>[
      const BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Inicio'),
      if (user.puedeGestionarUsuarios)
        const BottomNavigationBarItem(
            icon: Icon(Icons.people), label: 'Usuarios'),
      if (user.puedeGestionarUsuarios)
        const BottomNavigationBarItem(
            icon: Icon(Icons.meeting_room), label: 'Aulas'),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('CHRONOSIA'),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Center(
              child: Text(
                user.nombreCompleto,
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await auth.logout();
              if (!mounted) return;
              Navigator.pushNamedAndRemoveUntil(
                  context, '/login', (_) => false);
            },
          ),
        ],
      ),
      body: IndexedStack(index: currentIndex, children: screens),
      // ✅ Oculta el nav si solo hay una tab (rol sin acceso a usuarios)
      bottomNavigationBar: items.length > 1
          ? BottomNavigationBar(
              currentIndex: currentIndex,
              onTap: (i) => setState(() => currentIndex = i),
              items: items,
              selectedItemColor: AppTheme.greenPrimary,
              unselectedItemColor: Colors.grey.shade600,
            )
          : null,
    );
  }
}

class DashboardView extends StatelessWidget {
  const DashboardView({super.key});

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().user!;

    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: AppTheme.greenPrimary, width: 2),
              ),
              child: CircleAvatar(
                radius: 50,
                backgroundColor: AppTheme.greenSoft,
                backgroundImage: user.imagenUrl != null
                    ? NetworkImage(user.imagenUrl!)
                    : null,
                child: user.imagenUrl == null
                    ? const Icon(Icons.person,
                        size: 50, color: AppTheme.greenPrimary)
                    : null,
              ),
            ),
            const SizedBox(height: 20),
            Text(
              'Bienvenido, ${user.nombreCompleto}',
              style: const TextStyle(
                  fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(user.email,
                style: const TextStyle(
                    fontSize: 16, color: AppTheme.textDark)),
            const SizedBox(height: 10),
            Chip(
              label: Text(user.rol),
              backgroundColor: AppTheme.greenSoft,
              labelStyle: const TextStyle(color: AppTheme.greenPrimary),
            ),
          ],
        ),
      ),
    );
  }
}