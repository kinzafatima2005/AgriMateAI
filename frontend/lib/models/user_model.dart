/// AgriMate AI - User Model
/// Strictly reflects minimal registration fields.
class UserModel {
  final int id;
  final String name;
  final String phoneOrEmail;
  final String role;
  final String location;
  final String? token;

  UserModel({
    required this.id,
    required this.name,
    required this.phoneOrEmail,
    required this.role,
    required this.location,
    this.token,
  });

  factory UserModel.fromJson(Map<String, dynamic> json, {String? token}) {
    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      phoneOrEmail: json['phone_or_email'] as String,
      role: json['role'] as String,
      location: json['location'] as String,
      token: token,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'phone_or_email': phoneOrEmail,
      'role': role,
      'location': location,
    };
  }
}

