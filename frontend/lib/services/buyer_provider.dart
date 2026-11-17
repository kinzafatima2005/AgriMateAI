/// AgriMate AI - Buyer State Management Provider
import 'package:flutter/material.dart';
import '../models/buyer_models.dart';
import 'buyer_api_service.dart';

class BuyerProvider extends ChangeNotifier {
  final String token;

  BuyerProvider({required this.token}) {
    refreshAll();
  }

  // Summary
  BuyerSummary? _summary;
  bool _isLoadingSummary = false;
  String? _summaryError;

  BuyerSummary? get summary => _summary;
  bool get isLoadingSummary => _isLoadingSummary;
  String? get summaryError => _summaryError;

  // Listings
  List<ListingItem> _listings = [];
  bool _isLoadingListings = false;
  String? _listingsError;
  String _selectedCrop = 'All';
  String _selectedGrade = 'All';
  double? _minQty;
  double? _maxDistanceKm;
  String _searchQuery = '';
  String _selectedSort = 'nearest';

  List<ListingItem> get listings => _listings;
  bool get isLoadingListings => _isLoadingListings;
  String? get listingsError => _listingsError;
  String get selectedCrop => _selectedCrop;
  String get selectedGrade => _selectedGrade;
  double? get minQty => _minQty;
  double? get maxDistanceKm => _maxDistanceKm;
  String get searchQuery => _searchQuery;
  String get selectedSort => _selectedSort;

  // Deals
  List<BuyerDeal> _deals = [];
  bool _isLoadingDeals = false;
  String? _dealsError;
  String _dealStatusFilter = 'all';

  List<BuyerDeal> get deals => _deals;
  bool get isLoadingDeals => _isLoadingDeals;
  String? get dealsError => _dealsError;
  String get dealStatusFilter => _dealStatusFilter;

  // Notifications
  List<BuyerNotification> _notifications = [];
  bool _isLoadingNotifications = false;
  String? _notificationsError;

  List<BuyerNotification> get notifications => _notifications;
  bool get isLoadingNotifications => _isLoadingNotifications;
  String? get notificationsError => _notificationsError;
  int get unreadNotificationsCount => _notifications.where((n) => !n.isRead).length;

  // Profile
  BuyerPreferences? _profile;
  bool _isLoadingProfile = false;
  String? _profileError;

  BuyerPreferences? get profile => _profile;
  bool get isLoadingProfile => _isLoadingProfile;
  String? get profileError => _profileError;

  Future<void> refreshAll() async {
    await Future.wait([
      fetchSummary(),
      fetchListings(),
      fetchDeals(),
      fetchNotifications(),
      fetchProfile(),
    ]);
  }

  // --- Summary ---
  Future<void> fetchSummary() async {
    _isLoadingSummary = true;
    _summaryError = null;
    notifyListeners();

    try {
      _summary = await BuyerApiService.getSummary(token);
    } catch (e) {
      _summaryError = e.toString().replaceFirst('Exception: ', '');
    } finally {
      _isLoadingSummary = false;
      notifyListeners();
    }
  }

  // --- Listings ---
  Future<void> fetchListings() async {
    _isLoadingListings = true;
    _listingsError = null;
    notifyListeners();

    try {
      _listings = await BuyerApiService.getListings(
        token,
        crop: _selectedCrop == 'All' ? null : _selectedCrop,
        grade: _selectedGrade == 'All' ? null : _selectedGrade,
        minQty: _minQty,
        maxDistanceKm: _maxDistanceKm,
        search: _searchQuery.isEmpty ? null : _searchQuery,
        sort: _selectedSort,
      );
    } catch (e) {
      _listingsError = e.toString().replaceFirst('Exception: ', '');
    } finally {
      _isLoadingListings = false;
      notifyListeners();
    }
  }

  void setFilters({
    String? crop,
    String? grade,
    double? minQty,
    double? maxDistanceKm,
    String? sort,
  }) {
    if (crop != null) _selectedCrop = crop;
    if (grade != null) _selectedGrade = grade;
    _minQty = minQty;
    _maxDistanceKm = maxDistanceKm;
    if (sort != null) _selectedSort = sort;
    fetchListings();
  }

  void setSearchQuery(String query) {
    _searchQuery = query.trim();
    fetchListings();
  }

  // --- Express Interest ---
  Future<BuyerDeal> expressInterest(
    int listingId, {
    required double offeredPrice,
    required double quantityWanted,
    String? message,
  }) async {
    final deal = await BuyerApiService.expressInterest(
      token,
      listingId,
      offeredPrice: offeredPrice,
      quantityWanted: quantityWanted,
      message: message,
    );

    // Refresh listings and deals after interest
    await Future.wait([
      fetchListings(),
      fetchDeals(),
      fetchSummary(),
    ]);

    return deal;
  }

  // --- Deals ---
  Future<void> fetchDeals({String? status}) async {
    if (status != null) _dealStatusFilter = status;
    _isLoadingDeals = true;
    _dealsError = null;
    notifyListeners();

    try {
      _deals = await BuyerApiService.getDeals(
        token,
        status: _dealStatusFilter == 'all' ? null : _dealStatusFilter,
      );
    } catch (e) {
      _dealsError = e.toString().replaceFirst('Exception: ', '');
    } finally {
      _isLoadingDeals = false;
      notifyListeners();
    }
  }

  // --- Notifications ---
  Future<void> fetchNotifications() async {
    _isLoadingNotifications = true;
    _notificationsError = null;
    notifyListeners();

    try {
      _notifications = await BuyerApiService.getNotifications(token);
    } catch (e) {
      _notificationsError = e.toString().replaceFirst('Exception: ', '');
    } finally {
      _isLoadingNotifications = false;
      notifyListeners();
    }
  }

  Future<void> markNotificationAsRead(int id) async {
    try {
      await BuyerApiService.markNotificationAsRead(token, id);
      _notifications = _notifications.map((n) {
        if (n.id == id) {
          return BuyerNotification(
            id: n.id,
            type: n.type,
            title: n.title,
            body: n.body,
            isRead: true,
            createdAt: n.createdAt,
          );
        }
        return n;
      }).toList();
      notifyListeners();
    } catch (_) {}
  }

  // --- Profile ---
  Future<void> fetchProfile() async {
    _isLoadingProfile = true;
    _profileError = null;
    notifyListeners();

    try {
      _profile = await BuyerApiService.getProfile(token);
    } catch (e) {
      _profileError = e.toString().replaceFirst('Exception: ', '');
    } finally {
      _isLoadingProfile = false;
      notifyListeners();
    }
  }

  Future<bool> updateProfile(Map<String, dynamic> data) async {
    try {
      _profile = await BuyerApiService.updateProfile(token, data);
      notifyListeners();
      return true;
    } catch (e) {
      _profileError = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
      return false;
    }
  }
}
