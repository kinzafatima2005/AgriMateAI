import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'api_service.dart';

/// Offline-First Crop Health Diary Entry Model
class CropDiaryModel {
  final String clientUuid;
  final String cropName;
  final String? variety;
  final String fieldName;
  final double acreage;
  final String growthStage;
  final DateTime entryDate;
  final String activityType;
  final String? photoUrl;
  final String? diseasePrediction;
  final double confidence;
  final String severity;
  final String? notes;
  final String? treatmentApplied;
  final double costPkr;
  final DateTime clientUpdatedAt;
  final bool isSynced;
  final bool isDeleted;

  CropDiaryModel({
    required this.clientUuid,
    required this.cropName,
    this.variety,
    this.fieldName = 'Main Field',
    this.acreage = 1.0,
    required this.growthStage,
    required this.entryDate,
    this.activityType = 'Disease Scan',
    this.photoUrl,
    this.diseasePrediction,
    this.confidence = 0.0,
    this.severity = 'Optimal',
    this.notes,
    this.treatmentApplied,
    this.costPkr = 0.0,
    required this.clientUpdatedAt,
    this.isSynced = false,
    this.isDeleted = false,
  });

  Map<String, dynamic> toJson() => {
    'client_uuid': clientUuid,
    'crop_name': cropName,
    'variety': variety,
    'field_name': fieldName,
    'acreage': acreage,
    'growth_stage': growthStage,
    'entry_date': entryDate.toIso8601String(),
    'activity_type': activityType,
    'photo_url': photoUrl,
    'disease_prediction': diseasePrediction,
    'confidence': confidence,
    'severity': severity,
    'notes': notes,
    'treatment_applied': treatmentApplied,
    'cost_pkr': costPkr,
    'client_updated_at': clientUpdatedAt.toIso8601String(),
    'is_synced': isSynced,
    'is_deleted': isDeleted,
  };

  factory CropDiaryModel.fromJson(Map<String, dynamic> json) => CropDiaryModel(
    clientUuid: json['client_uuid'] ?? '',
    cropName: json['crop_name'] ?? 'Potato (آلو)',
    variety: json['variety'],
    fieldName: json['field_name'] ?? 'Main Field',
    acreage: (json['acreage'] as num?)?.toDouble() ?? 1.0,
    growthStage: json['growth_stage'] ?? 'Vegetative',
    entryDate: json['entry_date'] != null ? DateTime.parse(json['entry_date']) : DateTime.now(),
    activityType: json['activity_type'] ?? 'Disease Scan',
    photoUrl: json['photo_url'],
    diseasePrediction: json['disease_prediction'],
    confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
    severity: json['severity'] ?? 'Optimal',
    notes: json['notes'],
    treatmentApplied: json['treatment_applied'],
    costPkr: (json['cost_pkr'] as num?)?.toDouble() ?? 0.0,
    clientUpdatedAt: json['client_updated_at'] != null 
        ? DateTime.parse(json['client_updated_at']) 
        : DateTime.now(),
    isSynced: json['is_synced'] ?? false,
    isDeleted: json['is_deleted'] ?? false,
  );

  CropDiaryModel copyWith({
    String? cropName,
    String? variety,
    String? fieldName,
    double? acreage,
    String? growthStage,
    DateTime? entryDate,
    String? activityType,
    String? photoUrl,
    String? diseasePrediction,
    double? confidence,
    String? severity,
    String? notes,
    String? treatmentApplied,
    double? costPkr,
    DateTime? clientUpdatedAt,
    bool? isSynced,
    bool? isDeleted,
  }) => CropDiaryModel(
    clientUuid: clientUuid,
    cropName: cropName ?? this.cropName,
    variety: variety ?? this.variety,
    fieldName: fieldName ?? this.fieldName,
    acreage: acreage ?? this.acreage,
    growthStage: growthStage ?? this.growthStage,
    entryDate: entryDate ?? this.entryDate,
    activityType: activityType ?? this.activityType,
    photoUrl: photoUrl ?? this.photoUrl,
    diseasePrediction: diseasePrediction ?? this.diseasePrediction,
    confidence: confidence ?? this.confidence,
    severity: severity ?? this.severity,
    notes: notes ?? this.notes,
    treatmentApplied: treatmentApplied ?? this.treatmentApplied,
    costPkr: costPkr ?? this.costPkr,
    clientUpdatedAt: clientUpdatedAt ?? this.clientUpdatedAt,
    isSynced: isSynced ?? this.isSynced,
    isDeleted: isDeleted ?? this.isDeleted,
  );
}

/// Offline-First Local Store & Background Sync Service
class OfflineDiaryService extends ChangeNotifier {
  static const String _storageKey = 'agrimate_offline_crop_diary_v1';
  static const String _lastSyncKey = 'agrimate_crop_diary_last_sync_timestamp';

  static final OfflineDiaryService _instance = OfflineDiaryService._internal();
  factory OfflineDiaryService() => _instance;

  OfflineDiaryService._internal() {
    _initDefaultEntries();
  }

  List<CropDiaryModel> _entries = [];
  bool _isSyncing = false;
  String? _lastSyncTimestamp;

  List<CropDiaryModel> get entries => _entries.where((e) => !e.isDeleted).toList();
  List<CropDiaryModel> get allEntriesIncludingDeleted => _entries;
  bool get isSyncing => _isSyncing;
  int get pendingSyncCount => _entries.where((e) => !e.isSynced).length;
  String? get lastSyncTimestamp => _lastSyncTimestamp;

  /// Load local SQLite / Persistent storage
  Future<void> _initDefaultEntries() async {
    final prefs = await SharedPreferences.getInstance();
    _lastSyncTimestamp = prefs.getString(_lastSyncKey);
    final rawData = prefs.getString(_storageKey);

    if (rawData != null) {
      try {
        final List<dynamic> list = jsonDecode(rawData);
        _entries = list.map((item) => CropDiaryModel.fromJson(item)).toList();
      } catch (e) {
        _entries = [];
      }
    } else {
      // Seed default offline Pakistani Potato & Tomato diary records
      final now = DateTime.now();
      _entries = [
        CropDiaryModel(
          clientUuid: 'seed-uuid-potato-1',
          cropName: 'Potato (آلو)',
          variety: 'Asterix',
          fieldName: 'Okara North Block 3',
          acreage: 12.5,
          growthStage: 'Tuber Bulking/Ripening',
          entryDate: now.subtract(const Duration(days: 3)),
          activityType: 'Disease Scan',
          diseasePrediction: 'Potato Late Blight',
          confidence: 0.942,
          severity: 'High',
          notes: 'Late blight water-soaked lesions observed on lower leaves after fog.',
          treatmentApplied: 'Ridomil Gold @ 250g/100L water foliar spray',
          costPkr: 3800.0,
          clientUpdatedAt: now.subtract(const Duration(days: 3)),
          isSynced: true,
        ),
        CropDiaryModel(
          clientUuid: 'seed-uuid-tomato-2',
          cropName: 'Tomato (ٹماٹر)',
          variety: 'Sahil F1',
          fieldName: 'Tunnel Bed 2',
          acreage: 4.0,
          growthStage: 'Flowering/Fruit Set',
          entryDate: now.subtract(const Duration(days: 1)),
          activityType: 'Disease Scan',
          diseasePrediction: 'Tomato Early Blight',
          confidence: 0.918,
          severity: 'Moderate',
          notes: 'Concentric rings spotted on older leaves. Weather humid.',
          treatmentApplied: 'Difenoconazole @ 125ml/acre + calcium nitrate',
          costPkr: 2450.0,
          clientUpdatedAt: now.subtract(const Duration(days: 1)),
          isSynced: true,
        ),
        CropDiaryModel(
          clientUuid: 'seed-uuid-potato-3',
          cropName: 'Potato (آلو)',
          variety: 'Lady Rosetta',
          fieldName: 'South Plot 5',
          acreage: 8.0,
          growthStage: 'Vegetative',
          entryDate: now.subtract(const Duration(hours: 8)),
          activityType: 'Monitoring',
          diseasePrediction: 'Healthy Leaf',
          confidence: 0.965,
          severity: 'Optimal',
          notes: 'Regular scouting done. Vigorous crop canopy. Drip fertigation active.',
          treatmentApplied: 'None (Balanced NPK fertigation)',
          costPkr: 0.0,
          clientUpdatedAt: now.subtract(const Duration(hours: 8)),
          isSynced: false,
        ),
      ];
      await _saveLocal();
    }
    notifyListeners();
  }

  /// Save to local device storage (Source of Truth)
  Future<void> _saveLocal() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = jsonEncode(_entries.map((e) => e.toJson()).toList());
    await prefs.setString(_storageKey, jsonString);
    if (_lastSyncTimestamp != null) {
      await prefs.setString(_lastSyncKey, _lastSyncTimestamp!);
    }
  }

  /// Add new entry offline
  Future<void> addEntry(CropDiaryModel entry) async {
    _entries.insert(0, entry);
    await _saveLocal();
    notifyListeners();
  }

  /// Update entry offline (updates timestamp)
  Future<void> updateEntry(CropDiaryModel updated) async {
    final idx = _entries.indexWhere((e) => e.clientUuid == updated.clientUuid);
    if (idx != -1) {
      _entries[idx] = updated.copyWith(
        clientUpdatedAt: DateTime.now(),
        isSynced: false,
      );
      await _saveLocal();
      notifyListeners();
    }
  }

  /// Soft delete tombstone (Offline-first sync deletion)
  Future<void> deleteEntry(String clientUuid) async {
    final idx = _entries.indexWhere((e) => e.clientUuid == clientUuid);
    if (idx != -1) {
      _entries[idx] = _entries[idx].copyWith(
        isDeleted: true,
        clientUpdatedAt: DateTime.now(),
        isSynced: false,
      );
      await _saveLocal();
      notifyListeners();
    }
  }

  /// Multi-criteria search and filter
  List<CropDiaryModel> searchAndFilter({
    String? query,
    String? crop,
    String? growthStage,
    bool? hasDisease,
  }) {
    return _entries.where((e) {
      if (e.isDeleted) return false;

      // Query filter
      if (query != null && query.trim().isNotEmpty) {
        final q = query.toLowerCase().trim();
        final matchCrop = e.cropName.toLowerCase().contains(q);
        final matchField = e.fieldName.toLowerCase().contains(q);
        final matchNotes = (e.notes ?? '').toLowerCase().contains(q);
        final matchDisease = (e.diseasePrediction ?? '').toLowerCase().contains(q);
        final matchTreatment = (e.treatmentApplied ?? '').toLowerCase().contains(q);
        if (!matchCrop && !matchField && !matchNotes && !matchDisease && !matchTreatment) {
          return false;
        }
      }

      // Crop filter
      if (crop != null && crop != 'All') {
        if (!e.cropName.toLowerCase().contains(crop.toLowerCase())) {
          return false;
        }
      }

      // Growth stage filter
      if (growthStage != null && growthStage != 'All') {
        if (e.growthStage != growthStage) {
          return false;
        }
      }

      // Disease status filter
      if (hasDisease != null) {
        final isHealthy = (e.diseasePrediction ?? '').toLowerCase().contains('healthy');
        if (hasDisease && isHealthy) return false;
        if (!hasDisease && !isHealthy) return false;
      }

      return true;
    }).toList();
  }

  /// Two-Way Automatic Background Sync to Server
  /// Conflict handling: "Latest Timestamp Wins"
  Future<bool> syncWithServer(String? token) async {
    if (_isSyncing) return false;
    _isSyncing = true;
    notifyListeners();

    try {
      final unSyncedItems = _entries.where((e) => !e.isSynced).toList();
      final body = {
        'items': unSyncedItems.map((e) => e.toJson()).toList(),
        'last_sync_timestamp': _lastSyncTimestamp,
      };

      final response = await http.post(
        Uri.parse('${ApiService.activeBaseUrl}/diary/sync'),
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final List<dynamic> syncedUuids = data['synced_uuids'] ?? [];
        final List<dynamic> serverUpdates = data['server_updates'] ?? [];
        _lastSyncTimestamp = data['server_timestamp'];

        // 1. Mark successfully accepted client items as synced
        for (var uuid in syncedUuids) {
          final idx = _entries.indexWhere((e) => e.clientUuid == uuid);
          if (idx != -1) {
            _entries[idx] = _entries[idx].copyWith(isSynced: true);
          }
        }

        // 2. Reconcile server updates ("Latest Timestamp Wins" server resolution)
        for (var item in serverUpdates) {
          final serverModel = CropDiaryModel.fromJson(item).copyWith(isSynced: true);
          final existingIdx = _entries.indexWhere((e) => e.clientUuid == serverModel.clientUuid);
          if (existingIdx != -1) {
            _entries[existingIdx] = serverModel;
          } else {
            _entries.add(serverModel);
          }
        }

        await _saveLocal();
        _isSyncing = false;
        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('[OfflineDiaryService] Sync failed or offline: $e');
    }

    _isSyncing = false;
    notifyListeners();
    return false;
  }
}
