import 'package:shared_preferences/shared_preferences.dart';

/// Usando SharedPreferences mientras se agrega flutter_secure_storage.
/// Para producción: agregar flutter_secure_storage: ^9.0.0 en pubspec.yaml
/// y reemplazar esta implementación.
class TokenStorage {
  static const _accessKey  = 'access';
  static const _refreshKey = 'refresh';

  static Future<void> saveTokens(String access, String refresh) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_accessKey, access);
    await prefs.setString(_refreshKey, refresh);
  }

  static Future<String?> getAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_accessKey);
  }

  static Future<String?> getRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_refreshKey);
  }

  static Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_accessKey);
    await prefs.remove(_refreshKey);
  }
}