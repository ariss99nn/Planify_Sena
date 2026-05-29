import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../storage/token_storage.dart';

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
  static const String _defaultApiPath = '/api';
  // static const String _androidEmulatorHost = '10.0.2.2';

  static final String _environmentBaseUrl = const String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );
  static String? _overrideBaseUrl;

  /// Configura la URL base en tiempo de ejecuci�n.
  ///
  /// Ejemplo:
  /// `ApiService.configure(baseUrl: 'http://192.168.0.10:8000');`
  static void configure({String? baseUrl}) {
    if (baseUrl != null && baseUrl.isNotEmpty) {
      _overrideBaseUrl = _ensureApiPath(baseUrl);
    }
  }

  static String get baseUrl {
    if (_overrideBaseUrl != null && _overrideBaseUrl!.isNotEmpty) {
      return _overrideBaseUrl!;
    }
    if (_environmentBaseUrl.isNotEmpty) {
      return _ensureApiPath(_environmentBaseUrl);
    }
    return _resolveBaseUrl();
  }

  static String _resolveBaseUrl() {
  if (kIsWeb) {
    // En web, las peticiones van al mismo origen si el backend está en el mismo servidor
    // En desarrollo local, el frontend Flutter web corre en localhost también
    return 'http://localhost:8000$_defaultApiPath';
  }

  if (defaultTargetPlatform == TargetPlatform.android) {
    // Emulador usa 10.0.2.2, dispositivo físico necesita IP real
    // Sin configure() o --dart-define, esto fallará en físico
    return 'http://192.168.10.27:8000$_defaultApiPath';
  }

  if (defaultTargetPlatform == TargetPlatform.iOS ||
      defaultTargetPlatform == TargetPlatform.macOS) {
    return 'http://localhost:8000$_defaultApiPath';
  }

  // Windows / Linux desktop
  return 'http://localhost:8000$_defaultApiPath';
}

  static String _ensureApiPath(String url) {
    var normalized = url.trim();
    if (normalized.endsWith('/')) {
      normalized = normalized.substring(0, normalized.length - 1);
    }
    if (normalized.endsWith(_defaultApiPath)) {
      return normalized;
    }
    return '$normalized$_defaultApiPath';
  }

  static Uri _buildUri(String endpoint, [Map<String, String>? queryParams]) {
    final normalizedBase = baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl;
    final normalizedEndpoint = endpoint.startsWith('/') ? endpoint : '/$endpoint';

    return Uri.parse('$normalizedBase$normalizedEndpoint').replace(
      queryParameters: queryParams?.isNotEmpty == true ? queryParams : null,
    );
  }

  static Map<String, String> _headers({String? token}) {
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  static Future<dynamic> get(
    String endpoint, {
    String? token,
    Map<String, String>? queryParams,
  }) async {
    final uri = _buildUri(endpoint, queryParams);
    final response = await http.get(uri, headers: _headers(token: token));

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.get(
            uri,
            headers: _headers(token: newToken),
          ));
    }

    return _handle(response);
  }

  static Future<dynamic> post(
    String endpoint, {
    Map<String, dynamic>? data,
    String? token,
  }) async {
    final uri = _buildUri(endpoint);
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

  static Future<dynamic> patch(
    String endpoint, {
    Map<String, dynamic>? data,
    String? token,
  }) async {
    final uri = _buildUri(endpoint);
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

  static Future<dynamic> delete(String endpoint, {String? token}) async {
    final uri = _buildUri(endpoint);
    final response = await http.delete(uri, headers: _headers(token: token));

    if (response.statusCode == 401 && token != null) {
      return _retry((newToken) => http.delete(
            uri,
            headers: _headers(token: newToken),
          ));
    }

    return _handle(response);
  }

  static dynamic _handle(http.Response response) {
    final body = response.body.isNotEmpty ? jsonDecode(response.body) : null;

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

  static Future<dynamic> _retry(
    Future<http.Response> Function(String newToken) requestFn,
  ) async {
    final refresh = await TokenStorage.getRefreshToken();

    if (refresh == null) {
      await TokenStorage.clear();
      throw ApiException(
        message: 'Sesi�n expirada. Inicia sesi�n nuevamente.',
        statusCode: 401,
        code: 'session_expired',
      );
    }

    final refreshResponse = await http.post(
      _buildUri('/auth/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refresh}),
    );

    if (refreshResponse.statusCode != 200) {
      await TokenStorage.clear();
      throw ApiException(
        message: 'Sesi�n expirada. Inicia sesi�n nuevamente.',
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
