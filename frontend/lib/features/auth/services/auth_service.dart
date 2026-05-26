import '../../../core/api/api_service.dart';

class AuthService {

  // =========================
  // LOGIN
  // =========================
  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    return await ApiService.post(
      '/auth/login/',
      data: {
        'email': email.trim().toLowerCase(),
        'password': password,
      },
    );
  }

  // =========================
  // REGISTER
  // =========================
  static Future<Map<String, dynamic>> register({
    required String nombre,
    required String apellido,              // ✅ añadido
    required String email,
    required String password,
    required String password2,
    // ✅ rol eliminado del cliente — el backend asigna ESTUDIANTE por defecto
    // enviar rol desde el cliente es un riesgo de seguridad
  }) async {
    return await ApiService.post(
      '/auth/register/',
      data: {
        'nombre':    nombre.trim(),
        'apellido':  apellido.trim(),      // ✅ añadido
        'email':     email.trim().toLowerCase(),
        'password':  password,
        'password2': password2,
      },
    );
  }

  // =========================
  // PROFILE
  // =========================
  static Future<Map<String, dynamic>> getProfile(String token) async {
    return await ApiService.get(
      '/auth/profile/',
      token: token,
    );
  }

  static Future<Map<String, dynamic>> updateProfile({
    required String token,
    required Map<String, dynamic> data,
  }) async {
    return await ApiService.patch(
      '/auth/profile/',
      token: token,
      data: data,
    );
  }

  // =========================
  // VERIFY EMAIL
  // =========================
  static Future<Map<String, dynamic>> verifyEmail({
    required String email,
    required String code,
  }) async {
    return await ApiService.post(
      '/auth/verify-email/',
      data: {
        'email': email.trim().toLowerCase(),
        'code':  code.trim(),
      },
    );
  }

  // =========================
  // RESEND VERIFICATION
  // =========================
  static Future<void> resendVerification(String email) async {
    await ApiService.post(
      '/auth/resend-verification/',
      data: {'email': email.trim().toLowerCase()},
    );
  }

  // =========================
  // PASSWORD RESET REQUEST
  // =========================
  static Future<void> requestPasswordReset(String email) async {
    await ApiService.post(
      '/auth/password-reset/',
      data: {'email': email.trim().toLowerCase()},
    );
  }

  // =========================
  // PASSWORD RESET CONFIRM
  // =========================
  static Future<void> confirmPasswordReset({
    required String token,
    required String password,
  }) async {
    await ApiService.post(
      '/auth/password-reset/confirm/',
      data: {
        'token':    token,
        'password': password,
      },
    );
  }

  // =========================
  // EMAIL CHANGE REQUEST
  // =========================
  static Future<void> requestEmailChange({
    required String token,
    required String newEmail,
  }) async {
    await ApiService.post(
      '/auth/profile/email/',
      token: token,
      data: {'new_email': newEmail.trim().toLowerCase()},
    );
  }

  // =========================
  // EMAIL CHANGE CONFIRM
  // =========================
  static Future<void> confirmEmailChange({
    required String token,
    required String code,
  }) async {
    await ApiService.post(
      '/auth/profile/email/confirm/',
      token: token,
      data: {'code': code.trim()},
    );
  }

  // =========================
  // LOGOUT
  // =========================
  static Future<void> logout({
    required String refreshToken,
    required String accessToken,
  }) async {
    await ApiService.post(
      '/auth/logout/',
      token: accessToken,
      data: {'refresh': refreshToken},
    );
  }
}