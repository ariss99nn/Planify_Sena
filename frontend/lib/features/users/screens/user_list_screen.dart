import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';
import '../../../core/theme/theme.dart';

class UserListScreen extends StatefulWidget {
  const UserListScreen({super.key});

  @override
  State<UserListScreen> createState() => _UserListScreenState();
}

class _UserListScreenState extends State<UserListScreen> {
  final searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    Future.microtask(() => context.read<UserProvider>().fetchUsers());
  }

  @override
  void dispose() {
    searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<UserProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Usuarios",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: AppTheme.greenPrimary,
        foregroundColor: AppTheme.white,
        elevation: 0,
        actions: [
          // Botón para recargar lista
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<UserProvider>().fetchUsers(search: searchCtrl.text);
            },
            tooltip: 'Recargar',
          ),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppTheme.greenSoft, AppTheme.white],
          ),
        ),
        child: Column(
          children: [
            // Barra de búsqueda mejorada
            Padding(
              padding: const EdgeInsets.all(16),
              child: Card(
                elevation: 2,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: TextField(
                  controller: searchCtrl,
                  decoration: InputDecoration(
                    hintText: "Buscar usuarios...",
                    hintStyle: TextStyle(color: Colors.grey.shade500),
                    prefixIcon: Icon(
                      Icons.search,
                      color: AppTheme.greenPrimary,
                    ),
                    suffixIcon: IconButton(
                      icon: Icon(
                        Icons.clear,
                        color: searchCtrl.text.isEmpty
                            ? Colors.grey.shade400
                            : AppTheme.greenPrimary,
                      ),
                      onPressed: () {
                        if (searchCtrl.text.isNotEmpty) {
                          searchCtrl.clear();
                          context.read<UserProvider>().fetchUsers(search: '');
                        }
                      },
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    filled: true,
                    fillColor: AppTheme.white,
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 14,
                    ),
                  ),
                  onSubmitted: (value) {
                    context.read<UserProvider>().fetchUsers(search: value);
                  },
                ),
              ),
            ),

            // Contador de resultados
            if (!provider.loading && provider.users.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '${provider.users.length} usuarios encontrados',
                    style: TextStyle(
                      fontSize: 12,
                      color: AppTheme.textDark.withOpacity(0.6),
                    ),
                  ),
                ),
              ),

            // Loading o lista
            if (provider.loading)
              const Expanded(
                child: Center(
                  child: CircularProgressIndicator(),
                ),
              )
            else if (provider.users.isEmpty)
              Expanded(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.people_outline,
                        size: 64,
                        color: AppTheme.greenPrimary.withOpacity(0.5),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        "No hay usuarios",
                        style: TextStyle(
                          fontSize: 18,
                          color: AppTheme.textDark.withOpacity(0.7),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        "Prueba con otra búsqueda",
                        style: TextStyle(
                          fontSize: 14,
                          color: AppTheme.textDark.withOpacity(0.5),
                        ),
                      ),
                    ],
                  ),
                ),
              )
            else
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  itemCount: provider.users.length,
                  itemBuilder: (_, i) {
                    final u = provider.users[i];

                    return Card(
                      elevation: 2,
                      margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        leading: Container(
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(
                              color: AppTheme.greenPrimary,
                              width: 1.5,
                            ),
                          ),
                          child: CircleAvatar(
                            backgroundColor: AppTheme.greenSoft,
                            child: Text(
                              u.nombre.isNotEmpty ? u.nombre[0].toUpperCase() : '?',
                              style: TextStyle(
                                color: AppTheme.greenPrimary,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ),
                        title: Text(
                          u.nombre,
                          style: const TextStyle(
                            fontWeight: FontWeight.w600,
                            fontSize: 16,
                          ),
                        ),
                        subtitle: Text(
                          u.email,
                          style: TextStyle(
                            fontSize: 13,
                            color: AppTheme.textDark.withOpacity(0.7),
                          ),
                        ),
                        trailing: Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 12,
                            vertical: 6,
                          ),
                          decoration: BoxDecoration(
                            gradient: u.rol == 'ADMINISTRATIVO'
                                ? LinearGradient(
                                    colors: [AppTheme.greenPrimary, AppTheme.greenLight],
                                  )
                                : null,
                            color: u.rol != 'ADMINISTRATIVO'
                                ? Colors.grey.shade200
                                : null,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            u.rol == 'ADMINISTRATIVO' ? 'Admin' : 'Usuario',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: u.rol == 'ADMINISTRATIVO'
                                  ? AppTheme.white
                                  : AppTheme.textDark,
                            ),
                          ),
                        ),
                        onTap: () {
                          // Aquí puedes mostrar un dialog con detalles del usuario
                          _showUserDetailsDialog(context, u);
                        },
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Aquí puedes abrir un dialog para crear usuario
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text("Próximamente: Crear usuario"),
              backgroundColor: AppTheme.greenPrimary,
              behavior: SnackBarBehavior.floating,
            ),
          );
        },
        backgroundColor: AppTheme.greenPrimary,
        foregroundColor: AppTheme.white,
        child: const Icon(Icons.add),
        tooltip: 'Crear usuario',
      ),
    );
  }

  void _showUserDetailsDialog(BuildContext context, dynamic user) {
    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        child: Container(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: AppTheme.greenPrimary, width: 2),
                ),
                child: CircleAvatar(
                  radius: 40,
                  backgroundColor: AppTheme.greenSoft,
                  child: Text(
                    user.nombre.isNotEmpty ? user.nombre[0].toUpperCase() : '?',
                    style: TextStyle(
                      fontSize: 32,
                      color: AppTheme.greenPrimary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                user.nombre,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.email, size: 16, color: AppTheme.greenPrimary),
                  const SizedBox(width: 6),
                  Text(user.email),
                ],
              ),
              const SizedBox(height: 8),
              Chip(
                label: Text(user.rol == 'ADMINISTRATIVO' ? 'Administrador' : 'Usuario'),
                backgroundColor: AppTheme.greenSoft,
                labelStyle: TextStyle(color: AppTheme.greenPrimary),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.greenPrimary,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(40),
                  ),
                ),
                child: const Text("Cerrar"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}