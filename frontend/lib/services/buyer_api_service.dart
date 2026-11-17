/// AgriMate AI - Buyer API Service
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/buyer_models.dart';
import 'api_service.dart';

class BuyerApiService {
  static String get baseUrl => ApiService.activeBaseUrl;

  static Map<String, String> _headers(String token) => {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      };

  /// GET /buyer/summary
  static Future<BuyerSummary> getSummary(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/buyer/summary'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      return BuyerSummary.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load buyer summary');
    }
  }

  /// GET /buyer/listings
  static Future<List<ListingItem>> getListings(
    String token, {
    String? crop,
    String? grade,
    double? minQty,
    double? maxDistanceKm,
    String? search,
    String sort = 'nearest',
    int page = 1,
    int pageSize = 20,
  }) async {
    final queryParams = <String, String>{
      'sort': sort,
      'page': page.toString(),
      'page_size': pageSize.toString(),
    };
    if (crop != null && crop.isNotEmpty && crop != 'All') queryParams['crop'] = crop;
    if (grade != null && grade.isNotEmpty && grade != 'All') queryParams['grade'] = grade;
    if (minQty != null && minQty > 0) queryParams['min_qty'] = minQty.toString();
    if (maxDistanceKm != null && maxDistanceKm > 0) {
      queryParams['max_distance_km'] = maxDistanceKm.toString();
    }
    if (search != null && search.isNotEmpty) queryParams['search'] = search;

    final uri = Uri.parse('$baseUrl/buyer/listings').replace(queryParameters: queryParams);
    final response = await http.get(uri, headers: _headers(token));

    if (response.statusCode == 200) {
      final list = jsonDecode(response.body) as List<dynamic>;
      return list.map((e) => ListingItem.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load listings');
    }
  }

  /// GET /buyer/listings/{id}
  static Future<ListingDetail> getListingDetail(String token, int listingId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/buyer/listings/$listingId'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      return ListingDetail.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load listing detail');
    }
  }

  /// POST /buyer/listings/{id}/interest
  static Future<BuyerDeal> expressInterest(
    String token,
    int listingId, {
    required double offeredPrice,
    required double quantityWanted,
    String? message,
  }) async {
    final body = jsonEncode({
      'offered_price': offeredPrice,
      'quantity_wanted': quantityWanted,
      'message': message,
    });

    final response = await http.post(
      Uri.parse('$baseUrl/buyer/listings/$listingId/interest'),
      headers: _headers(token),
      body: body,
    );

    if (response.statusCode == 200) {
      return BuyerDeal.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to express interest');
    }
  }

  /// GET /buyer/deals
  static Future<List<BuyerDeal>> getDeals(String token, {String? status}) async {
    final queryParams = <String, String>{};
    if (status != null && status.isNotEmpty && status != 'all') {
      queryParams['status'] = status;
    }

    final uri = Uri.parse('$baseUrl/buyer/deals').replace(queryParameters: queryParams);
    final response = await http.get(uri, headers: _headers(token));

    if (response.statusCode == 200) {
      final list = jsonDecode(response.body) as List<dynamic>;
      return list.map((e) => BuyerDeal.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load deals');
    }
  }

  /// GET /buyer/deals/{id}
  static Future<BuyerDeal> getDealDetail(String token, int dealId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/buyer/deals/$dealId'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      return BuyerDeal.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load deal detail');
    }
  }

  /// GET /buyer/notifications
  static Future<List<BuyerNotification>> getNotifications(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/buyer/notifications'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      final list = jsonDecode(response.body) as List<dynamic>;
      return list.map((e) => BuyerNotification.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load notifications');
    }
  }

  /// PATCH /buyer/notifications/{id}/read
  static Future<bool> markNotificationAsRead(String token, int notificationId) async {
    final response = await http.patch(
      Uri.parse('$baseUrl/buyer/notifications/$notificationId/read'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      return true;
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to mark notification read');
    }
  }

  /// GET /buyer/profile
  static Future<BuyerPreferences> getProfile(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/buyer/profile'),
      headers: _headers(token),
    );

    if (response.statusCode == 200) {
      return BuyerPreferences.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to load profile');
    }
  }

  /// PUT /buyer/profile
  static Future<BuyerPreferences> updateProfile(
    String token,
    Map<String, dynamic> data,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/buyer/profile'),
      headers: _headers(token),
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {
      return BuyerPreferences.fromJson(jsonDecode(response.body));
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err['detail'] ?? 'Failed to update profile');
    }
  }
}
