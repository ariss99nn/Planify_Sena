class UserModel {
  final int id;
  final String nombre;
  final String apellido;                 // ✅ añadido
  final String nombreCompleto;           // ✅ añadido
  final String email;
  final String rol;
  final bool isActive;
  final bool emailVerificado;            // ✅ añadido — solo presente en UserSelfSerializer
  final String? imagenUrl;
  final DateTime fechaCreacion;
  final DateTime fechaModificacion;      // ✅ añadido

  UserModel({
    required this.id,
    required this.nombre,
    required this.apellido,
    required this.nombreCompleto,
    required this.email,
    required this.rol,
    required this.isActive,
    required this.emailVerificado,
    this.imagenUrl,
    required this.fechaCreacion,
    required this.fechaModificacion,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id:               json['id'] as int,
      nombre:           json['nombre'] as String,
      apellido:         json['apellido'] as String,
      nombreCompleto:   json['nombre_completo'] as String,
      email:            json['email'] as String,
      rol:              json['rol'] as String,
      isActive:         json['is_active'] as bool,
      // email_verificado solo viene en UserSelfSerializer — default false si ausente
      emailVerificado:  json['email_verificado'] as bool? ?? false,
      imagenUrl:        json['imagen_url'] as String?,    // ✅ corregido: era 'imagen'
      fechaCreacion:    DateTime.parse(json['fecha_creacion'] as String),
      fechaModificacion: DateTime.parse(json['fecha_modificacion'] as String),
    );
  }

  /// Helpers de rol — evitan comparar strings sueltos en la UI
  bool get esEstudiante    => rol == 'ESTUDIANTE';
  bool get esDocente       => rol == 'DOCENTE';
  bool get esAdministrativo => rol == 'ADMINISTRATIVO';
  bool get esCoordinador   => rol == 'COORDINADOR';
  bool get puedeGestionarUsuarios =>
      rol == 'ADMINISTRATIVO' || rol == 'COORDINADOR';

  UserModel copyWith({
    int? id,
    String? nombre,
    String? apellido,
    String? nombreCompleto,
    String? email,
    String? rol,
    bool? isActive,
    bool? emailVerificado,
    String? imagenUrl,
    DateTime? fechaCreacion,
    DateTime? fechaModificacion,
  }) {
    return UserModel(
      id:                id               ?? this.id,
      nombre:            nombre           ?? this.nombre,
      apellido:          apellido         ?? this.apellido,
      nombreCompleto:    nombreCompleto   ?? this.nombreCompleto,
      email:             email            ?? this.email,
      rol:               rol              ?? this.rol,
      isActive:          isActive         ?? this.isActive,
      emailVerificado:   emailVerificado  ?? this.emailVerificado,
      imagenUrl:         imagenUrl        ?? this.imagenUrl,
      fechaCreacion:     fechaCreacion    ?? this.fechaCreacion,
      fechaModificacion: fechaModificacion ?? this.fechaModificacion,
    );
  }
}