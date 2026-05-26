import 'package:flutter/material.dart';
import '../../auth/models/user_model.dart';
import '../services/user_service.dart';

class UserProvider with ChangeNotifier {
  List<UserModel> users = [];
  bool loading = false;

  Future<void> fetchUsers({String? search}) async {
    loading = true;
    notifyListeners();

    try {
      final data = await UserService.getUsers(search: search);
      users = (data['results'] as List)
          .map((e) => UserModel.fromJson(e))
          .toList();
    } catch (e) {
      users = [];
    }

    loading = false;
    notifyListeners();
  }
}