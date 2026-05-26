import 'package:flutter/foundation.dart';
import '../../../core/api/api_service.dart';
import '../models/aula.dart';
import '../models/bloque.dart';
import '../services/aula_service.dart';

enum AulaStatus { idle, loading, success, error }

class AulaProvider extends ChangeNotifier {
  // AulaService es estático — no se inyecta instancia

  // ── Lista ─────────────────────────────────────────────────────────────────
  List<AulaResumen> aulas = [];
  AulaStatus listStatus = AulaStatus.idle;
  String? listError;

  // ── Detalle ───────────────────────────────────────────────────────────────
  Aula? selected;
  AulaStatus detailStatus = AulaStatus.idle;
  String? detailError;

  // ── Formulario ────────────────────────────────────────────────────────────
  AulaStatus formStatus = AulaStatus.idle;
  String? formError;

  // ── Bloques (dropdown del form) ───────────────────────────────────────────
  List<Bloque> bloques = [];
  AulaStatus bloquesStatus = AulaStatus.idle;

  // ── Filtros activos ───────────────────────────────────────────────────────
  String? filtroSearch;
  String? filtroEstado;
  String? filtroTipo;
  int? filtroBloque;

  // ── Fetch lista ───────────────────────────────────────────────────────────

  Future<void> fetchAulas() async {
    listStatus = AulaStatus.loading;
    listError = null;
    notifyListeners();
    try {
      aulas = await AulaService.getAulas(
        search: filtroSearch,
        estado: filtroEstado,
        tipoAula: filtroTipo,
        bloqueId: filtroBloque,
      );
      listStatus = AulaStatus.success;
    } catch (e) {
      listStatus = AulaStatus.error;
      listError = _friendlyError(e);
    }
    notifyListeners();
  }

  void setFiltros({
    String? search,
    String? estado,
    String? tipo,
    int? bloque,
  }) {
    filtroSearch = search;
    filtroEstado = estado;
    filtroTipo = tipo;
    filtroBloque = bloque;
    fetchAulas();
  }

  void clearFiltros() => setFiltros();

  // ── Fetch detalle ─────────────────────────────────────────────────────────

  Future<void> fetchAula(int id) async {
    detailStatus = AulaStatus.loading;
    detailError = null;
    notifyListeners();
    try {
      selected = await AulaService.getAula(id);
      detailStatus = AulaStatus.success;
    } catch (e) {
      detailStatus = AulaStatus.error;
      detailError = _friendlyError(e);
    }
    notifyListeners();
  }

  // ── Crear ─────────────────────────────────────────────────────────────────

  Future<bool> createAula(Map<String, dynamic> body) async {
    formStatus = AulaStatus.loading;
    formError = null;
    notifyListeners();
    try {
      await AulaService.createAula(body);
      formStatus = AulaStatus.success;
      await fetchAulas();
      notifyListeners();
      return true;
    } catch (e) {
      formStatus = AulaStatus.error;
      formError = _friendlyError(e);
      notifyListeners();
      return false;
    }
  }

  // ── Actualizar ────────────────────────────────────────────────────────────

  Future<bool> updateAula(int id, Map<String, dynamic> body) async {
    formStatus = AulaStatus.loading;
    formError = null;
    notifyListeners();
    try {
      selected = await AulaService.updateAula(id, body);
      formStatus = AulaStatus.success;
      await fetchAulas();
      notifyListeners();
      return true;
    } catch (e) {
      formStatus = AulaStatus.error;
      formError = _friendlyError(e);
      notifyListeners();
      return false;
    }
  }

  // ── Cambiar estado ────────────────────────────────────────────────────────

  Future<bool> updateEstado(int id, String estado) async {
    try {
      await AulaService.updateEstado(id, estado);
      if (selected?.id == id) await fetchAula(id);
      await fetchAulas();
      return true;
    } catch (e) {
      return false;
    }
  }

  // ── Bloques ───────────────────────────────────────────────────────────────

  Future<void> fetchBloques() async {
    if (bloques.isNotEmpty) return;
    bloquesStatus = AulaStatus.loading;
    notifyListeners();
    try {
      bloques = await AulaService.getBloques();
      bloquesStatus = AulaStatus.success;
    } catch (_) {
      bloquesStatus = AulaStatus.error;
    }
    notifyListeners();
  }

  void resetForm() {
    formStatus = AulaStatus.idle;
    formError = null;
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  String _friendlyError(Object e) {
    if (e is ApiException) return e.message;
    return e.toString();
  }
}