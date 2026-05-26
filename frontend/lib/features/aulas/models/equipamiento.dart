class Equipamiento {
  final int id;
  final String nombre;
  final int cantidad;
  final String estado;
  final String estadoDisplay;

  const Equipamiento({
    required this.id,
    required this.nombre,
    required this.cantidad,
    required this.estado,
    required this.estadoDisplay,
  });

  factory Equipamiento.fromJson(Map<String, dynamic> json) => Equipamiento(
        id: json['id'] as int,
        nombre: json['nombre'] as String,
        cantidad: json['cantidad'] as int,
        estado: json['estado'] as String,
        estadoDisplay: json['estado_display'] as String,
      );
}