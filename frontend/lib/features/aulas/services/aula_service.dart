import '../../../core/api/api_service.dart';
import '../../../core/storage/token_storage.dart';
import '../models/aula.dart';
import '../models/bloque.dart';

class AulaService {
  // Lee el token en cada llamada para que siempre use el más reciente
  // (después del retry, TokenStorage ya tiene el nuevo access).

  static Future<String?> _token() => TokenStorage.getAccessToken();

  // ── Aulas ────────────────────────────────────────────────────────────────

  static Future<List<AulaResumen>> getAulas({
    String? search,
    String? estado,
    String? tipoAula,
    int? bloqueId,
    int? capacidadMin,
    int page = 1,
  }) async {
    final params = <String, String>{
      'page': page.toString(),
      if (search != null && search.isNotEmpty) 'search': search,
      if (estado != null) 'estado': estado,
      if (tipoAula != null) 'tipo_aula': tipoAula,
      if (bloqueId != null) 'bloque': bloqueId.toString(),
      if (capacidadMin != null) 'capacidad_min': capacidadMin.toString(),
    };

    final data = await ApiService.get(
      '/aulas/',
      token: await _token(),
      queryParams: params,
    ) as Map<String, dynamic>;

    return (data['results'] as List)
        .map((e) => AulaResumen.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  static Future<Aula> getAula(int id) async {
    final data = await ApiService.get(
      '/aulas/$id/',
      token: await _token(),
    ) as Map<String, dynamic>;
    return Aula.fromJson(data);
  }

  static Future<Aula> createAula(Map<String, dynamic> body) async {
    final data = await ApiService.post(
      '/aulas/create/',
      data: body,
      token: await _token(),
    ) as Map<String, dynamic>;
    return Aula.fromJson(data);
  }

  static Future<Aula> updateAula(int id, Map<String, dynamic> body) async {
    final data = await ApiService.patch(
      '/aulas/$id/update/',
      data: body,
      token: await _token(),
    ) as Map<String, dynamic>;
    return Aula.fromJson(data);
  }

  static Future<void> updateEstado(int id, String estado) async {
    await ApiService.patch(
      '/aulas/$id/estado/',
      data: {'estado': estado},
      token: await _token(),
    );
  }

  // ── Bloques ───────────────────────────────────────────────────────────────

  static Future<List<Bloque>> getBloques({String? search}) async {
    final params = <String, String>{
      if (search != null && search.isNotEmpty) 'search': search,
    };

    final data = await ApiService.get(
      '/aulas/bloques/',
      token: await _token(),
      queryParams: params,
    ) as Map<String, dynamic>;

    return (data['results'] as List)
        .map((e) => Bloque.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}