class Bloque {
  final int id;
  final String nombre;
  final int piso;
  final int capacidadMaxima;
  final String descripcion;
  final String? imagenUrl;
  final int? totalAulas; // solo en detail

  const Bloque({
    required this.id,
    required this.nombre,
    required this.piso,
    required this.capacidadMaxima,
    required this.descripcion,
    this.imagenUrl,
    this.totalAulas,
  });

  factory Bloque.fromJson(Map<String, dynamic> json) => Bloque(
        id: json['id'] as int,
        nombre: json['nombre'] as String,
        piso: json['piso'] as int,
        capacidadMaxima: json['capacidad_maxima'] as int,
        descripcion: json['descripcion'] as String? ?? '',
        imagenUrl: json['imagen'] as String?,
        totalAulas: json['total_aulas'] as int?,
      );
}