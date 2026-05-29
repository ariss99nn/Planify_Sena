import '../../../core/api/api_service.dart';
import '../../../core/storage/token_storage.dart';

class UserService {
  static Future<dynamic> getUsers({String? search}) async {
    final token = await TokenStorage.getAccessToken();

    return await ApiService.get(
      '/users/?search=${search ?? ''}',
      token: token,
    );
  }

  static Future<dynamic> getUser(int id) async {
    final token = await TokenStorage.getAccessToken();

    return await ApiService.get(
      '/users/$id/',
      token: token,
    );
  }

  static Future<dynamic> createUser({
    required String nombre,
    required String apellido,
    required String email,
    required String password,
    required String rol,
  }) async {
    final token = await TokenStorage.getAccessToken();

    return await ApiService.post(
      '/users/',
      token: token,
      data: {
        'nombre': nombre.trim(),
        'apellido': apellido.trim(),
        'email': email.trim().toLowerCase(),
        'password': password,
        'rol': rol,
      },
    );
  }

  static Future<dynamic> updateUser({
    required int id,
    required Map<String, dynamic> data,
  }) async {
    final token = await TokenStorage.getAccessToken();

    return await ApiService.patch(
      '/users/$id/',
      token: token,
      data: data,
    );
  }

  static Future<void> deactivateUser(int id) async {
    final token = await TokenStorage.getAccessToken();

    await ApiService.post(
      '/users/$id/deactivate/',
      token: token,
      data: {},
    );
  }
}
