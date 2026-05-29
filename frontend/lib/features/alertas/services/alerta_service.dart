import '../../../core/api/api_service.dart';
import '../../../core/storage/token_storage.dart';
import '../models/alerta_model.dart';

class AlertaService {
  static const _base = '/alertas';

  static Future<List<AlertaModel>> listar({
    String? tipo,
    String? estado,
    bool? soloNoLeidas,
    int? page,
  }) async {
    final token = await TokenStorage.getAccessToken();
    final params = <String, String>{
      if (tipo != null) 'tipo': tipo,
      if (estado != null) 'estado': estado,
      if (soloNoLeidas == true) 'leidas': 'true',
      if (page != null) 'page': page.toString(),
    };
    final data = await ApiService.get(
      '$_base/',
      token: token,
      queryParams: params.isNotEmpty ? params : null,
    );
    final results = data['results'] as List<dynamic>;
    return results
        .map((e) => AlertaModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  static Future<AlertaModel> marcarLeida(int id) async {
    final token = await TokenStorage.getAccessToken();
    final data = await ApiService.patch(
      '$_base/$id/update/',
      token: token,
      data: {'estado': 'LEIDA'},
    );
    return AlertaModel.fromJson(data as Map<String, dynamic>);
  }

  static Future<AlertaModel> crear({
    required String tipo,
    required String descripcion,
    required String formatoAlerta,
    int? destinatario,
    int? bloqueOrigen,
  }) async {
    final token = await TokenStorage.getAccessToken();
    final data = await ApiService.post(
      '$_base/create/',
      token: token,
      data: {
        'tipo': tipo,
        'descripcion': descripcion,
        'formato_alerta': formatoAlerta,
        if (destinatario != null) 'destinatario': destinatario,
        if (bloqueOrigen != null) 'bloque_origen': bloqueOrigen,
      },
    );
    return AlertaModel.fromJson(data as Map<String, dynamic>);
  }
}