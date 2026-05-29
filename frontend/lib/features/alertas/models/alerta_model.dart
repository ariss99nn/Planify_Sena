enum TipoAlerta { CONFLICTO, DISPONIBILIDAD, SISTEMA }
enum FormatoAlerta { EMAIL, SMS, APP }
enum EstadoAlerta { PENDIENTE, ENVIADA, LEIDA }

class AlertaModel {
  final int id;
  final TipoAlerta tipo;
  final String tipoDisplay;
  final EstadoAlerta estado;
  final String estadoDisplay;
  final FormatoAlerta formatoAlerta;
  final String formatoDisplay;
  final String descripcion;
  final int? destinatarioId;
  final String? destinatarioNombre;
  final int? bloqueOrigen;
  final DateTime fechaCreacion;
  final DateTime? fechaLectura;

  const AlertaModel({
    required this.id,
    required this.tipo,
    required this.tipoDisplay,
    required this.estado,
    required this.estadoDisplay,
    required this.formatoAlerta,
    required this.formatoDisplay,
    required this.descripcion,
    this.destinatarioId,
    this.destinatarioNombre,
    this.bloqueOrigen,
    required this.fechaCreacion,
    this.fechaLectura,
  });

  bool get isLeida => estado == EstadoAlerta.LEIDA;

  factory AlertaModel.fromJson(Map<String, dynamic> json) {
    return AlertaModel(
      id: json['id'] as int,
      tipo: TipoAlerta.values.byName(json['tipo'] as String),
      tipoDisplay: json['tipo_display'] as String,
      estado: EstadoAlerta.values.byName(json['estado'] as String),
      estadoDisplay: json['estado_display'] as String,
      formatoAlerta: FormatoAlerta.values.byName(json['formato_alerta'] as String),
      formatoDisplay: json['formato_display'] as String,
      descripcion: json['descripcion'] as String,
      destinatarioId: json['destinatario'] as int?,
      destinatarioNombre: json['destinatario_nombre'] as String?,
      bloqueOrigen: json['bloque_origen'] as int?,
      fechaCreacion: DateTime.parse(json['fecha_creacion'] as String),
      fechaLectura: json['fecha_lectura'] != null
          ? DateTime.parse(json['fecha_lectura'] as String)
          : null,
    );
  }
}