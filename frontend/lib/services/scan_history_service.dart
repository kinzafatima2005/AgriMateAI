import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocalScanItem {
  final String id;
  final String crop;
  final String diseaseName;
  final String urduName;
  final double confidence;
  final String severity;
  final String timestamp;
  final bool isSynced;
  final bool needsReview;

  LocalScanItem({
    required this.id,
    required this.crop,
    required this.diseaseName,
    required this.urduName,
    required this.confidence,
    required this.severity,
    required this.timestamp,
    this.isSynced = false,
    this.needsReview = false,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'crop': crop,
    'disease_name': diseaseName,
    'urdu_name': urduName,
    'confidence': confidence,
    'severity': severity,
    'timestamp': timestamp,
    'is_synced': isSynced,
    'needs_review': needsReview,
  };

  factory LocalScanItem.fromJson(Map<String, dynamic> map) => LocalScanItem(
    id: map['id'] ?? '',
    crop: map['crop'] ?? '',
    diseaseName: map['disease_name'] ?? '',
    urduName: map['urdu_name'] ?? '',
    confidence: (map['confidence'] as num?)?.toDouble() ?? 0.0,
    severity: map['severity'] ?? 'MODERATE',
    timestamp: map['timestamp'] ?? '',
    isSynced: map['is_synced'] ?? false,
    needsReview: map['needs_review'] ?? false,
  );
}

class ScanHistoryService extends ChangeNotifier {
  static final ScanHistoryService _instance = ScanHistoryService._internal();
  factory ScanHistoryService() => _instance;
  ScanHistoryService._internal() {
    loadScans();
  }

  final List<LocalScanItem> _scans = [];
  List<LocalScanItem> get scans => List.unmodifiable(_scans);

  Future<void> loadScans() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final raw = prefs.getString('offline_scans_history');
      if (raw != null) {
        final List list = jsonDecode(raw);
        _scans.clear();
        _scans.addAll(list.map((x) => LocalScanItem.fromJson(x)));
        notifyListeners();
      }
    } catch (_) {}
  }

  Future<void> saveScan(LocalScanItem item) async {
    _scans.insert(0, item);
    notifyListeners();
    try {
      final prefs = await SharedPreferences.getInstance();
      final raw = jsonEncode(_scans.map((x) => x.toJson()).toList());
      await prefs.setString('offline_scans_history', raw);
    } catch (_) {}
  }
}

