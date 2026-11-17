import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator, 127.0.0.1 for Web / Windows / iOS simulator
  static String get baseUrl {
    if (kIsWeb) return 'http://127.0.0.1:8000/api/v1';
    // By default support local network / emulator
    return 'http://10.0.2.2:8000/api/v1';
  }

  /// Optional override for physical devices or custom backend IP
  static String? customBaseUrl;
  static String get activeBaseUrl => customBaseUrl ?? baseUrl;

  /// Register with minimal 5 fields only
  static Future<UserModel> register({
    required String name,
    required String phoneOrEmail,
    required String password,
    required String role,
    required String location,
  }) async {
    final response = await http.post(
      Uri.parse('$activeBaseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name.trim(),
        'phone_or_email': phoneOrEmail.trim(),
        'password': password,
        'role': role,
        'location': location.trim(),
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 201) {
      final token = data['access_token'] as String;
      final userJson = data['user'] as Map<String, dynamic>;
      return UserModel.fromJson(userJson, token: token);
    } else {
      throw Exception(data['detail'] ?? 'Registration failed. Please check inputs.');
    }
  }

  /// Login with phone or email and password
  static Future<UserModel> login({
    required String phoneOrEmail,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$activeBaseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'phone_or_email': phoneOrEmail.trim(),
        'password': password,
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      final token = data['access_token'] as String;
      final userJson = data['user'] as Map<String, dynamic>;
      return UserModel.fromJson(userJson, token: token);
    } else {
      throw Exception(data['detail'] ?? 'Login failed. Please verify credentials.');
    }
  }

  /// Fetch authenticated profile
  static Future<UserModel> getMe(String token) async {
    final response = await http.get(
      Uri.parse('$activeBaseUrl/auth/me'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return UserModel.fromJson(data, token: token);
    } else {
      throw Exception(data['detail'] ?? 'Session expired.');
    }
  }
}

