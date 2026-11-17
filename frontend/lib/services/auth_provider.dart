import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';
import 'api_service.dart';

class AuthProvider extends ChangeNotifier {
  UserModel? _currentUser;
  bool _isLoading = false;
  String? _errorMessage;

  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _currentUser != null;

  AuthProvider() {
    _tryAutoLogin();
  }

  Future<void> _tryAutoLogin() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('agrimate_jwt_token');
      if (token != null && token.isNotEmpty) {
        _currentUser = await ApiService.getMe(token);
        notifyListeners();
      }
    } catch (_) {
      // Token expired or network offline, proceed to onboarding/login
    }
  }

  Future<bool> login(String phoneOrEmail, String password) async {
    _setLoading(true);
    _errorMessage = null;
    try {
      final user = await ApiService.login(
        phoneOrEmail: phoneOrEmail,
        password: password,
      );
      _currentUser = user;
      if (user.token != null) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('agrimate_jwt_token', user.token!);
      }
      _setLoading(false);
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _setLoading(false);
      return false;
    }
  }

  Future<bool> register({
    required String name,
    required String phoneOrEmail,
    required String password,
    required String role,
    required String location,
  }) async {
    _setLoading(true);
    _errorMessage = null;
    try {
      final user = await ApiService.register(
        name: name,
        phoneOrEmail: phoneOrEmail,
        password: password,
        role: role,
        location: location,
      );
      _currentUser = user;
      if (user.token != null) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('agrimate_jwt_token', user.token!);
      }
      _setLoading(false);
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _setLoading(false);
      return false;
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('agrimate_jwt_token');
    _currentUser = null;
    notifyListeners();
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
}

