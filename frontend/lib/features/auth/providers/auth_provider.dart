import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../../../core/api/api_service.dart';
import '../../../core/storage/token_storage.dart';
import '../models/user_model.dart';

enum AuthStatus {
  checking,
  authenticated,
  unauthenticated,
  pendingVerification,   // ✅ nuevo estado — email registrado pero no verificado
}

class AuthProvider with ChangeNotifier {
  AuthStatus _status = AuthStatus.checking;
  UserModel? _user;
  // Guarda el email pendiente para la pantalla de verificación
  String? _pendingEmail;

  AuthStatus get status  => _status;
  UserModel?  get user   => _user;
  String?     get pendingEmail => _pendingEmail;

  bool get isAuthenticated => _status == AuthStatus.authenticated;

  // =========================
  // INIT / CHECK AUTH
  // =========================
  Future<void> checkAuth() async {
  _status = AuthStatus.checking;
  notifyListeners();

  try {
    final token = await TokenStorage.getAccessToken();

    if (token == null) {
      _status = AuthStatus.unauthenticated;
      notifyListeners();  // ✅ notifica aquí antes del return
      return;
    }

    final userData = await AuthService.getProfile(token);
    _user = UserModel.fromJson(userData);
    _status = AuthStatus.authenticated;
  } on ApiException catch (e) {
    if (e.code == 'session_expired') {
      await _clearSession();
      return;              // ✅ _clearSession ya notifica
    } else {
      _setUnauthenticated();
    }
  } catch (_) {
    _setUnauthenticated();
  }

  notifyListeners();
}

  // =========================
  // LOGIN
  // =========================
  Future<void> login(String email, String password) async {
    // Puede lanzar ApiException — el widget lo captura y muestra el mensaje
    final res = await AuthService.login(email: email, password: password);

    final access   = res['access']  as String?;
    final refresh  = res['refresh'] as String?;
    final userData = res['user']    as Map<String, dynamic>?;

    if (access == null || refresh == null || userData == null) {
      throw ApiException(
        message: 'Respuesta inválida del servidor.',
        statusCode: 200,
      );
    }

    await TokenStorage.saveTokens(access, refresh);

    _user   = UserModel.fromJson(userData);
    _status = AuthStatus.authenticated;
    _pendingEmail = null;

    notifyListeners();
  }

  // =========================
  // REGISTER
  // =========================
  Future<void> register({
    required String nombre,
    required String apellido,
    required String email,
    required String password,
    required String password2,
  }) async {
    await AuthService.register(
      nombre:    nombre,
      apellido:  apellido,
      email:     email,
      password:  password,
      password2: password2,
    );

    // Tras registrarse el usuario debe verificar su correo
    _pendingEmail = email.trim().toLowerCase();
    _status = AuthStatus.pendingVerification;
    notifyListeners();
  }

  // =========================
  // VERIFY EMAIL
  // =========================
  Future<void> verifyEmail({
  required String email,
  required String code,
}) async {
  await AuthService.verifyEmail(email: email, code: code);

  _pendingEmail = null;
  _status = AuthStatus.unauthenticated;
  notifyListeners();  // ✅ faltaba esto
}

  // =========================
  // RESEND VERIFICATION
  // =========================
  Future<void> resendVerification(String email) async {
    await AuthService.resendVerification(email);
  }

  // =========================
  // LOGOUT
  // =========================
  Future<void> logout() async {
    try {
      final refresh = await TokenStorage.getRefreshToken();
      final access  = await TokenStorage.getAccessToken();
      if (refresh != null && access != null) {
        await AuthService.logout(
          refreshToken: refresh,
          accessToken: access,
        );
      }
    } catch (_) {
      // Si el logout en el servidor falla, limpiamos igual localmente
    }

    await _clearSession();
  }

  // =========================
  // UPDATE PROFILE (local)
  // =========================
  /// Actualiza el modelo local tras un PATCH exitoso en el servidor.
  void updateLocalUser(UserModel updated) {
    _user = updated;
    notifyListeners();
  }

  // =========================
  // HELPERS PRIVADOS
  // =========================
  void _setUnauthenticated() {
    _user   = null;
    _status = AuthStatus.unauthenticated;
  }

  Future<void> _clearSession() async {
    await TokenStorage.clear();
    _setUnauthenticated();
    notifyListeners();
  }

  // =========================
  // GETTERS DE CONVENIENCIA
  // =========================
  String? get nombre   => _user?.nombre;
  String? get apellido => _user?.apellido;
  String? get email    => _user?.email;
  String? get rol      => _user?.rol;
  String? get imagenUrl => _user?.imagenUrl;
  bool get emailVerificado => _user?.emailVerificado ?? false;
  bool get puedeGestionarUsuarios => _user?.puedeGestionarUsuarios ?? false;
}