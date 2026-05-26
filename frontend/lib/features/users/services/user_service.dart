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

  static Future<void> deactivateUser(int id) async {
    final token = await TokenStorage.getAccessToken();

    await ApiService.patch(
      '/users/$id/deactivate/',
      token: token,
      data: {'confirmacion': true},
    );
  }
}