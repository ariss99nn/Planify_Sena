import 'bloque.dart';
import 'equipamiento.dart';

class Aula {
  final int id;
  final String codigoAula;
  final int capacidad;
  final String tipoAula;
  final String tipoAulaDisplay;
  final String estado;
  final String estadoDisplay;
  final Bloque bloque;
  final String descripcion;
  final String? imagenUrl;
  final List<Equipamiento> equipamiento;

  const Aula({
    required this.id,
    required this.codigoAula,
    required this.capacidad,
    required this.tipoAula,
    required this.tipoAulaDisplay,
    required this.estado,
    required this.estadoDisplay,
    required this.bloque,
    required this.descripcion,
    this.imagenUrl,
    required this.equipamiento,
  });

  factory Aula.fromJson(Map<String, dynamic> json) => Aula(
        id: json['id'] as int,
        codigoAula: json['codigo_aula'] as String,
        capacidad: json['capacidad'] as int,
        tipoAula: json['tipo_aula'] as String,
        tipoAulaDisplay: json['tipo_aula_display'] as String,
        estado: json['estado'] as String,
        estadoDisplay: json['estado_display'] as String,
        bloque: Bloque.fromJson(json['bloque'] as Map<String, dynamic>),
        descripcion: json['descripcion'] as String? ?? '',
        imagenUrl: json['imagen'] as String?,
        equipamiento: (json['equipamiento'] as List<dynamic>? ?? [])
            .map((e) => Equipamiento.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
}

// Lista resumida (AulaListSerializer)
class AulaResumen {
  final int id;
  final String codigoAula;
  final int capacidad;
  final String tipoAula;
  final String tipoAulaDisplay;
  final String estado;
  final String estadoDisplay;
  final String bloqueNombre;

  const AulaResumen({
    required this.id,
    required this.codigoAula,
    required this.capacidad,
    required this.tipoAula,
    required this.tipoAulaDisplay,
    required this.estado,
    required this.estadoDisplay,
    required this.bloqueNombre,
  });

  factory AulaResumen.fromJson(Map<String, dynamic> json) => AulaResumen(
        id: json['id'] as int,
        codigoAula: json['codigo_aula'] as String,
        capacidad: json['capacidad'] as int,
        tipoAula: json['tipo_aula'] as String,
        tipoAulaDisplay: json['tipo_aula_display'] as String,
        estado: json['estado'] as String,
        estadoDisplay: json['estado_display'] as String,
        bloqueNombre: json['bloque_nombre'] as String,
      );
}