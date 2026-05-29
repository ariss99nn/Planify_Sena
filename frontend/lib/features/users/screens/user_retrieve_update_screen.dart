import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/user_service.dart';
import '../providers/user_provider.dart';
import '../../../core/api/api_service.dart';
import '../../../core/theme/theme.dart';

class UserRetrieveUpdateScreen extends StatefulWidget {
  final int userId;

  const UserRetrieveUpdateScreen({super.key, required this.userId});

  @override
  State<UserRetrieveUpdateScreen> createState() => _UserRetrieveUpdateScreenState();
}

class _UserRetrieveUpdateScreenState extends State<UserRetrieveUpdateScreen> {
  final nombreCtrl = TextEditingController();
  final apellidoCtrl = TextEditingController();
  final emailCtrl = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  bool loading = true;
  bool updating = false;
  String selectedRol = 'ESTUDIANTE';

  final roles = ['ESTUDIANTE', 'ADMINISTRATIVO', 'DOCENTE'];

  @override
  void initState() {
    super.initState();
    _loadUser();
  }

  Future<void> _loadUser() async {
    try {
      final user = await UserService.getUser(widget.userId);

      if (!mounted) return;

      setState(() {
        nombreCtrl.text = user['nombre'] ?? '';
        apellidoCtrl.text = user['apellido'] ?? '';
        emailCtrl.text = user['email'] ?? '';
        selectedRol = user['rol'] ?? 'ESTUDIANTE';
        loading = false;
      });
    } on ApiException catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.message),
          backgroundColor: Colors.red.shade700,
        ),
      );

      Navigator.pop(context);
    }
  }

  Future<void> _updateUser() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => updating = true);

    try {
      await UserService.updateUser(
        id: widget.userId,
        data: {
          'nombre': nombreCtrl.text.trim(),
          'apellido': apellidoCtrl.text.trim(),
          'email': emailCtrl.text.trim().toLowerCase(),
          'rol': selectedRol,
        },
      );

      if (!mounted) return;

      // Actualiza la lista
      context.read<UserProvider>().fetchUsers();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Usuario actualizado exitosamente'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );

      Navigator.pop(context);
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
      if (mounted) setState(() => updating = false);
    }
  }

  Future<void> _deactivateUser() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Desactivar usuario'),
        content: const Text('¿Estás seguro de desactivar este usuario?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text(
              'Desactivar',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    setState(() => updating = true);

    try {
      await UserService.deactivateUser(widget.userId);

      if (!mounted) return;

      context.read<UserProvider>().fetchUsers();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Usuario desactivado exitosamente'),
          backgroundColor: AppTheme.greenPrimary,
          behavior: SnackBarBehavior.floating,
        ),
      );

      Navigator.pop(context);
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
      if (mounted) setState(() => updating = false);
    }
  }

  @override
  void dispose() {
    nombreCtrl.dispose();
    apellidoCtrl.dispose();
    emailCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Editar Usuario'),
        backgroundColor: AppTheme.greenPrimary,
        foregroundColor: AppTheme.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: updating ? null : _deactivateUser,
            tooltip: 'Desactivar usuario',
          ),
        ],
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Form(
                key: _formKey,
                child: Column(
                  children: [
                    // Nombre
                    TextFormField(
                      controller: nombreCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Nombre',
                        prefixIcon: Icon(Icons.person),
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Ingresa el nombre';
                        if (v.length < 2) return 'Mínimo 2 caracteres';
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    // Apellido
                    TextFormField(
                      controller: apellidoCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Apellido',
                        prefixIcon: Icon(Icons.person),
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Ingresa el apellido';
                        if (v.length < 2) return 'Mínimo 2 caracteres';
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    // Email
                    TextFormField(
                      controller: emailCtrl,
                      keyboardType: TextInputType.emailAddress,
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        prefixIcon: Icon(Icons.email),
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Ingresa el email';
                        if (!v.contains('@')) return 'Email inválido';
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    // Rol
                    DropdownButtonFormField<String>(
                      value: selectedRol,
                      decoration: const InputDecoration(
                        labelText: 'Rol',
                        prefixIcon: Icon(Icons.security),
                      ),
                      items: roles.map((rol) {
                        return DropdownMenuItem(
                          value: rol,
                          child: Text(rol),
                        );
                      }).toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => selectedRol = value);
                        }
                      },
                    ),
                    const SizedBox(height: 32),

                    // Botón actualizar
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: updating ? null : _updateUser,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.greenPrimary,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        child: updating
                            ? const SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation(Colors.white),
                                ),
                              )
                            : const Text(
                                'Actualizar Usuario',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
