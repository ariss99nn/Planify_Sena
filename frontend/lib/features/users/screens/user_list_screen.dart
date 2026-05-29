import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/user_service.dart';
import '../providers/user_provider.dart';
import '../../../core/api/api_service.dart';
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
                        trailing: PopupMenuButton(
                          itemBuilder: (context) => [
                            PopupMenuItem(
                              child: const Text('Editar'),
                              onTap: () {
                                Navigator.pushNamed(
                                  context,
                                  '/users/edit/${u.id}',
                                );
                              },
                            ),
                            PopupMenuItem(
                              child: const Text(
                                'Desactivar',
                                style: TextStyle(color: Colors.red),
                              ),
                              onTap: () {
                                _showDeactivateConfirmDialog(context, u);
                              },
                            ),
                          ],
                          child: Container(
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
                        ),
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
          Navigator.pushNamed(context, '/users/create');
        },
        backgroundColor: AppTheme.greenPrimary,
        foregroundColor: AppTheme.white,
        child: const Icon(Icons.add),
        tooltip: 'Crear usuario',
      ),
    );
  }

  void _showDeactivateConfirmDialog(BuildContext context, dynamic user) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Desactivar usuario'),
        content: Text('¿Desactivar a ${user.nombre}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _deactivateUser(user.id);
            },
            child: const Text(
              'Desactivar',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _deactivateUser(int userId) async {
    try {
      await UserService.deactivateUser(userId);

      if (!mounted) return;

      context.read<UserProvider>().fetchUsers();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Usuario desactivado exitosamente'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.message),
          backgroundColor: Colors.red.shade700,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }
}