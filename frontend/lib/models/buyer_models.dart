/// AgriMate AI - Buyer Models
import 'package:flutter/foundation.dart';

class MatchScoreBreakdown {
  final bool cropMatch;
  final double quantityScore;
  final double distanceScore;
  final double gradeScore;
  final double priceScore;
  final double totalScore;
  final double distanceKm;
  final String matchLevel;
  final String explanation;

  const MatchScoreBreakdown({
    required this.cropMatch,
    required this.quantityScore,
    required this.distanceScore,
    required this.gradeScore,
    required this.priceScore,
    required this.totalScore,
    required this.distanceKm,
    required this.matchLevel,
    required this.explanation,
  });

  factory MatchScoreBreakdown.fromJson(Map<String, dynamic> json) {
    return MatchScoreBreakdown(
      cropMatch: json['crop_match'] as bool? ?? false,
      quantityScore: (json['quantity_score'] as num?)?.toDouble() ?? 0.0,
      distanceScore: (json['distance_score'] as num?)?.toDouble() ?? 0.0,
      gradeScore: (json['grade_score'] as num?)?.toDouble() ?? 0.0,
      priceScore: (json['price_score'] as num?)?.toDouble() ?? 0.0,
      totalScore: (json['total_score'] as num?)?.toDouble() ?? 0.0,
      distanceKm: (json['distance_km'] as num?)?.toDouble() ?? 0.0,
      matchLevel: json['match_level'] as String? ?? 'MISMATCH',
      explanation: json['explanation'] as String? ?? '',
    );
  }
}

class ListingItem {
  final int id;
  final int farmerId;
  final String farmerName;
  final String crop;
  final String grade;
  final double quantity;
  final double askingPrice;
  final String location;
  final double? latitude;
  final double? longitude;
  final double? distanceKm;
  final double? totalMatchScore;
  final String status;
  final DateTime createdAt;
  final bool alreadyInterested;

  const ListingItem({
    required this.id,
    required this.farmerId,
    required this.farmerName,
    required this.crop,
    required this.grade,
    required this.quantity,
    required this.askingPrice,
    required this.location,
    this.latitude,
    this.longitude,
    this.distanceKm,
    this.totalMatchScore,
    required this.status,
    required this.createdAt,
    required this.alreadyInterested,
  });

  factory ListingItem.fromJson(Map<String, dynamic> json) {
    return ListingItem(
      id: json['id'] as int? ?? 0,
      farmerId: json['farmer_id'] as int? ?? 0,
      farmerName: json['farmer_name'] as String? ?? 'Farmer',
      crop: json['crop'] as String? ?? '',
      grade: json['grade'] as String? ?? 'A',
      quantity: (json['quantity'] as num?)?.toDouble() ?? 0.0,
      askingPrice: (json['asking_price'] as num?)?.toDouble() ?? 0.0,
      location: json['location'] as String? ?? '',
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      distanceKm: (json['distance_km'] as num?)?.toDouble(),
      totalMatchScore: (json['total_match_score'] as num?)?.toDouble(),
      status: json['status'] as String? ?? 'active',
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
      alreadyInterested: json['already_interested'] as bool? ?? false,
    );
  }
}

class ListingDetail extends ListingItem {
  final MatchScoreBreakdown? matchBreakdown;
  final String? farmerContact;

  const ListingDetail({
    required super.id,
    required super.farmerId,
    required super.farmerName,
    required super.crop,
    required super.grade,
    required super.quantity,
    required super.askingPrice,
    required super.location,
    super.latitude,
    super.longitude,
    super.distanceKm,
    super.totalMatchScore,
    required super.status,
    required super.createdAt,
    required super.alreadyInterested,
    this.matchBreakdown,
    this.farmerContact,
  });

  factory ListingDetail.fromJson(Map<String, dynamic> json) {
    final base = ListingItem.fromJson(json);
    return ListingDetail(
      id: base.id,
      farmerId: base.farmerId,
      farmerName: base.farmerName,
      crop: base.crop,
      grade: base.grade,
      quantity: base.quantity,
      askingPrice: base.askingPrice,
      location: base.location,
      latitude: base.latitude,
      longitude: base.longitude,
      distanceKm: base.distanceKm,
      totalMatchScore: base.totalMatchScore,
      status: base.status,
      createdAt: base.createdAt,
      alreadyInterested: base.alreadyInterested,
      matchBreakdown: json['match_breakdown'] != null
          ? MatchScoreBreakdown.fromJson(json['match_breakdown'] as Map<String, dynamic>)
          : null,
      farmerContact: json['farmer_contact'] as String?,
    );
  }
}

class DealHistoryItem {
  final int id;
  final String status;
  final String? notes;
  final DateTime changedAt;

  const DealHistoryItem({
    required this.id,
    required this.status,
    this.notes,
    required this.changedAt,
  });

  factory DealHistoryItem.fromJson(Map<String, dynamic> json) {
    return DealHistoryItem(
      id: json['id'] as int? ?? 0,
      status: json['status'] as String? ?? '',
      notes: json['notes'] as String?,
      changedAt: json['changed_at'] != null
          ? DateTime.tryParse(json['changed_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }
}

class BuyerDeal {
  final int id;
  final int listingId;
  final int buyerId;
  final String crop;
  final String grade;
  final double quantityWanted;
  final double offeredPrice;
  final double askingPrice;
  final String farmerName;
  final String farmerLocation;
  final String? farmerContact;
  final String status;
  final String? message;
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<DealHistoryItem> history;

  const BuyerDeal({
    required this.id,
    required this.listingId,
    required this.buyerId,
    required this.crop,
    required this.grade,
    required this.quantityWanted,
    required this.offeredPrice,
    required this.askingPrice,
    required this.farmerName,
    required this.farmerLocation,
    this.farmerContact,
    required this.status,
    this.message,
    required this.createdAt,
    required this.updatedAt,
    this.history = const [],
  });

  factory BuyerDeal.fromJson(Map<String, dynamic> json) {
    return BuyerDeal(
      id: json['id'] as int? ?? 0,
      listingId: json['listing_id'] as int? ?? 0,
      buyerId: json['buyer_id'] as int? ?? 0,
      crop: json['crop'] as String? ?? 'Produce',
      grade: json['grade'] as String? ?? 'A',
      quantityWanted: (json['quantity_wanted'] as num?)?.toDouble() ?? 0.0,
      offeredPrice: (json['offered_price'] as num?)?.toDouble() ?? 0.0,
      askingPrice: (json['asking_price'] as num?)?.toDouble() ?? 0.0,
      farmerName: json['farmer_name'] as String? ?? 'Farmer',
      farmerLocation: json['farmer_location'] as String? ?? '',
      farmerContact: json['farmer_contact'] as String?,
      status: json['status'] as String? ?? 'interested',
      message: json['message'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
      updatedAt: json['updated_at'] != null
          ? DateTime.tryParse(json['updated_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
      history: (json['history'] as List<dynamic>?)
              ?.map((e) => DealHistoryItem.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

class PriceTickerItem {
  final String crop;
  final String mandi;
  final double rate;
  final String unit;
  final String trend;
  final String date;

  const PriceTickerItem({
    required this.crop,
    required this.mandi,
    required this.rate,
    required this.unit,
    required this.trend,
    required this.date,
  });

  factory PriceTickerItem.fromJson(Map<String, dynamic> json) {
    return PriceTickerItem(
      crop: json['crop'] as String? ?? '',
      mandi: json['mandi'] as String? ?? '',
      rate: (json['rate'] as num?)?.toDouble() ?? 0.0,
      unit: json['unit'] as String? ?? 'PKR / 40kg',
      trend: json['trend'] as String? ?? 'stable',
      date: json['date'] as String? ?? '',
    );
  }
}

class BuyerNotification {
  final int id;
  final String type;
  final String title;
  final String body;
  final bool isRead;
  final DateTime createdAt;

  const BuyerNotification({
    required this.id,
    required this.type,
    required this.title,
    required this.body,
    required this.isRead,
    required this.createdAt,
  });

  factory BuyerNotification.fromJson(Map<String, dynamic> json) {
    return BuyerNotification(
      id: json['id'] as int? ?? 0,
      type: json['type'] as String? ?? 'SYSTEM',
      title: json['title'] as String? ?? '',
      body: json['body'] as String? ?? '',
      isRead: json['is_read'] as bool? ?? false,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }
}

class BuyerSummary {
  final String buyerName;
  final String buyerLocation;
  final int activeListingsCount;
  final int myInterestsCount;
  final int dealsInProgressCount;
  final List<PriceTickerItem> priceTicker;
  final List<BuyerNotification> recentNotifications;
  final String disclaimer;

  const BuyerSummary({
    required this.buyerName,
    required this.buyerLocation,
    required this.activeListingsCount,
    required this.myInterestsCount,
    required this.dealsInProgressCount,
    required this.priceTicker,
    required this.recentNotifications,
    required this.disclaimer,
  });

  factory BuyerSummary.fromJson(Map<String, dynamic> json) {
    return BuyerSummary(
      buyerName: json['buyer_name'] as String? ?? 'Buyer',
      buyerLocation: json['buyer_location'] as String? ?? 'Punjab',
      activeListingsCount: json['active_listings_count'] as int? ?? 0,
      myInterestsCount: json['my_interests_count'] as int? ?? 0,
      dealsInProgressCount: json['deals_in_progress_count'] as int? ?? 0,
      priceTicker: (json['price_ticker'] as List<dynamic>?)
              ?.map((e) => PriceTickerItem.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      recentNotifications: (json['recent_notifications'] as List<dynamic>?)
              ?.map((e) => BuyerNotification.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      disclaimer: json['disclaimer'] as String? ??
          'Decision-support prototype: no payments or legal contracts',
    );
  }
}

class BuyerPreferences {
  final int id;
  final String name;
  final String phoneOrEmail;
  final String location;
  final String role;
  final List<String> preferredCrops;
  final String preferredGrade;
  final double minQty;
  final double maxQty;
  final double? latitude;
  final double? longitude;
  final double maxBudgetPrice;

  const BuyerPreferences({
    required this.id,
    required this.name,
    required this.phoneOrEmail,
    required this.location,
    required this.role,
    required this.preferredCrops,
    required this.preferredGrade,
    required this.minQty,
    required this.maxQty,
    this.latitude,
    this.longitude,
    required this.maxBudgetPrice,
  });

  factory BuyerPreferences.fromJson(Map<String, dynamic> json) {
    return BuyerPreferences(
      id: json['id'] as int? ?? 0,
      name: json['name'] as String? ?? '',
      phoneOrEmail: json['phone_or_email'] as String? ?? '',
      location: json['location'] as String? ?? '',
      role: json['role'] as String? ?? 'Buyer',
      preferredCrops: (json['preferred_crops'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          ['Potato', 'Tomato'],
      preferredGrade: json['preferred_grade'] as String? ?? 'A',
      minQty: (json['min_qty'] as num?)?.toDouble() ?? 1000.0,
      maxQty: (json['max_qty'] as num?)?.toDouble() ?? 10000.0,
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      maxBudgetPrice: (json['max_budget_price'] as num?)?.toDouble() ?? 2600.0,
    );
  }
}
