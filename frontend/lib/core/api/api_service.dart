import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/token_storage.dart';

/// Excepción tipada que preserva el código de error del backend.
class ApiException implements Exception {
  final String message;
  final String? code;
  final int statusCode;

  ApiException({
    required this.message,
    required this.statusCode,
    this.code,
  });

  @override
  String toString() => 'ApiException($statusCode): $message [code: $code]';
}

class ApiService {
  // Cambiar por variable de entorno o flavor en producción
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  static Map<String, String> _headers({String? token}) {
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // ===================== GET =====================
  // CAMBIO: agregado queryParams opcional para filtros y paginación
  static Future<dynamic> get(
    String endpoint, {
    String? token,
    Map<String, String>? queryParams,
  }) async {
    final uri = Uri.parse('$baseUrl$endpoint').replace(
      queryParameters: queryParams?.isNotEmpty == true ? queryParams : null,
    );
    final response = await http.get(uri, headers: _headers(token: token));

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.get(
            uri,
            headers: _headers(token: newToken),
          ));
    }

    return _handle(response);
  }

  // ===================== POST =====================
  static Future<dynamic> post(
    String endpoint, {
    Map<String, dynamic>? data,
    String? token,
  }) async {
    final uri = Uri.parse('$baseUrl$endpoint');
    final body = jsonEncode(data);
    final response = await http.post(
      uri,
      headers: _headers(token: token),
      body: body,
    );

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.post(
            uri,
            headers: _headers(token: newToken),
            body: body,
          ));
    }

    return _handle(response);
  }

  // ===================== PATCH =====================
  static Future<dynamic> patch(
    String endpoint, {
    Map<String, dynamic>? data,
    String? token,
  }) async {
    final uri = Uri.parse('$baseUrl$endpoint');
    final body = jsonEncode(data);
    final response = await http.patch(
      uri,
      headers: _headers(token: token),
      body: body,
    );

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.patch(
            uri,
            headers: _headers(token: newToken),
            body: body,
          ));
    }

    return _handle(response);
  }

  // ===================== DELETE =====================
  static Future<dynamic> delete(String endpoint, {String? token}) async {
    final uri = Uri.parse('$baseUrl$endpoint');
    final response = await http.delete(uri, headers: _headers(token: token));

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.delete(
            uri,
            headers: _headers(token: newToken),
          ));
    }

    return _handle(response);
  }

  // ===================== HANDLE =====================
  static dynamic _handle(http.Response response) {
    final body =
        response.body.isNotEmpty ? jsonDecode(response.body) : null;

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return body;
    }

    final message = _extractMessage(body);
    final code = body is Map ? body['code'] as String? : null;

    throw ApiException(
      message: message,
      statusCode: response.statusCode,
      code: code,
    );
  }

  static String _extractMessage(dynamic body) {
    if (body == null) return 'Error desconocido';
    if (body is Map) {
      final detail = body['detail'];
      if (detail is String) return detail;
      if (detail is Map) return detail['detail'] as String? ?? 'Error';
      if (body.isNotEmpty) {
        final first = body.values.first;
        if (first is List && first.isNotEmpty) return first.first.toString();
      }
    }
    return 'Error desconocido';
  }

  // ===================== RETRY =====================
  static Future<dynamic> _retry(
    Future<http.Response> Function(String newToken) requestFn,
  ) async {
    final refresh = await TokenStorage.getRefreshToken();

    if (refresh == null) {
      await TokenStorage.clear();
      throw ApiException(
        message: 'Sesión expirada. Inicia sesión nuevamente.',
        statusCode: 401,
        code: 'session_expired',
      );
    }

    final refreshResponse = await http.post(
      Uri.parse('$baseUrl/auth/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refresh}),
    );

    if (refreshResponse.statusCode != 200) {
      await TokenStorage.clear();
      throw ApiException(
        message: 'Sesión expirada. Inicia sesión nuevamente.',
        statusCode: 401,
        code: 'session_expired',
      );
    }

    final data = jsonDecode(refreshResponse.body);
    final newAccess = data['access'] as String;

    await TokenStorage.saveTokens(newAccess, refresh);

    final retryResponse = await requestFn(newAccess);
    return _handle(retryResponse);
  }
}