enum TipoWsMensaje { conexion, alerta_nueva, conflicto_horario, pong, desconocido }

class WsMensaje {
  final TipoWsMensaje tipo;
  final String? descripcion;
  final String? fecha;
  final int? id;
  final String? tipoAlerta;
  final int? bloqueId;
  final String? mensaje;

  const WsMensaje({
    required this.tipo,
    this.descripcion,
    this.fecha,
    this.id,
    this.tipoAlerta,
    this.bloqueId,
    this.mensaje,
  });

  factory WsMensaje.fromJson(Map<String, dynamic> json) {
    final raw = json['tipo'] as String? ?? '';
    final tipo = TipoWsMensaje.values.firstWhere(
      (e) => e.name == raw,
      orElse: () => TipoWsMensaje.desconocido,
    );
    return WsMensaje(
      tipo:        tipo,
      descripcion: json['descripcion'] as String?,
      fecha:       json['fecha']       as String?,
      id:          json['id']          as int?,
      tipoAlerta:  json['tipo_alerta'] as String?,
      bloqueId:    json['bloque_id']   as int?,
      mensaje:     json['mensaje']     as String?,
    );
  }
}