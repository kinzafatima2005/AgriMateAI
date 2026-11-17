import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/app_theme.dart';
import '../../services/auth_provider.dart';
import '../../services/offline_diary_service.dart';
import '../../widgets/decision_disclaimer_banner.dart';

/// PHASE 5 – CROP-HEALTH DIARY SCREEN
/// Features:
/// - Dated photos, prediction results, growth stage, notes, treatments
/// - Search and filter by crop, growth stage, and disease presence
/// - Local SQLite/storage as source of truth (offline-first)
/// - Automatic two-way background sync with conflict handling (Latest Timestamp Wins)
class CropDiaryScreen extends StatefulWidget {
  const CropDiaryScreen({super.key});

  @override
  State<CropDiaryScreen> createState() => _CropDiaryScreenState();
}

class _CropDiaryScreenState extends State<CropDiaryScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _selectedCrop = 'All';
  String _selectedGrowthStage = 'All';
  bool? _filterHasDisease;

  final List<String> _cropFilters = ['All', 'Potato', 'Tomato'];
  final List<String> _stageFilters = [
    'All',
    'Vegetative',
    'Flowering/Fruit Set',
    'Tuber Bulking/Ripening',
    'Harvest Ready',
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final diaryService = Provider.of<OfflineDiaryService>(context);
    final auth = Provider.of<AuthProvider>(context, listen: false);

    final filteredEntries = diaryService.searchAndFilter(
      query: _searchController.text,
      crop: _selectedCrop,
      growthStage: _selectedGrowthStage,
      hasDisease: _filterHasDisease,
    );

    return Scaffold(
      backgroundColor: AgriColors.background,
      appBar: AppBar(
        backgroundColor: AgriColors.background,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AgriColors.textWhite, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Crop-Health Diary',
          style: textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
            color: AgriColors.textWhite,
          ),
        ),
        actions: [
          // Background Sync Status Pill & Button
          Padding(
            padding: const EdgeInsets.only(right: 14.0),
            child: InkWell(
              onTap: diaryService.isSyncing
                  ? null
                  : () async {
                      final success = await diaryService.syncWithServer(auth.currentUser?.token);
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                              success
                                  ? 'Two-Way Sync Complete (Latest Timestamp Won)'
                                  : 'Sync failed or device offline. Saved locally.',
                            ),
                            backgroundColor: success ? AgriColors.backgroundDark : AgriColors.warning,
                          ),
                        );
                      }
                    },
              borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: diaryService.pendingSyncCount > 0
                      ? AgriColors.accentYellow.withOpacity(0.2)
                      : AgriColors.cardSurfaceLight,
                  borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                  border: Border.all(
                    color: diaryService.pendingSyncCount > 0
                        ? AgriColors.accentYellow
                        : Colors.transparent,
                    width: 1,
                  ),
                ),
                child: Row(
                  children: [
                    if (diaryService.isSyncing)
                      const SizedBox(
                        width: 12,
                        height: 12,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: AgriColors.accentYellow,
                        ),
                      )
                    else
                      Icon(
                        diaryService.pendingSyncCount > 0
                            ? Icons.sync_problem_rounded
                            : Icons.cloud_done_rounded,
                        color: diaryService.pendingSyncCount > 0
                            ? AgriColors.accentYellow
                            : AgriColors.accentYellow,
                        size: 16,
                      ),
                    const SizedBox(width: 5),
                    Text(
                      diaryService.isSyncing
                          ? 'Syncing...'
                          : diaryService.pendingSyncCount > 0
                              ? '${diaryService.pendingSyncCount} Pending'
                              : 'Synced',
                      style: const TextStyle(
                        color: AgriColors.textWhite,
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Search Bar & Filter Header
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: AgriDimensions.screenPadding,
                vertical: 8,
              ),
              child: Container(
                decoration: BoxDecoration(
                  color: AgriColors.cardSurface,
                  borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                  border: Border.all(color: AgriColors.cardSurfaceLight),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 14),
                child: Row(
                  children: [
                    const Icon(Icons.search_rounded, color: AgriColors.accentYellow, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: TextField(
                        controller: _searchController,
                        onChanged: (_) => setState(() {}),
                        style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                        decoration: const InputDecoration(
                          hintText: 'Search potato, tomato, blight, spray...',
                          hintStyle: TextStyle(color: AgriColors.textSecondary, fontSize: 13),
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                    if (_searchController.text.isNotEmpty)
                      IconButton(
                        icon: const Icon(Icons.clear_rounded, color: AgriColors.textSecondary, size: 18),
                        onPressed: () {
                          _searchController.clear();
                          setState(() {});
                        },
                      ),
                  ],
                ),
              ),
            ),

            // Crop Filter Chips
            SizedBox(
              height: 38,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
                itemCount: _cropFilters.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (context, idx) {
                  final crop = _cropFilters[idx];
                  final isSelected = crop == _selectedCrop;
                  return GestureDetector(
                    onTap: () => setState(() => _selectedCrop = crop),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: isSelected ? AgriColors.accentYellow : AgriColors.cardSurface,
                        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                      ),
                      child: Text(
                        crop == 'All' ? 'All Crops' : (crop == 'Potato' ? '🥔 Potato' : '🍅 Tomato'),
                        style: TextStyle(
                          color: isSelected ? AgriColors.darkGreenText : AgriColors.textWhite,
                          fontSize: 12,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),

            const SizedBox(height: 8),

            // Growth Stage Horizontal Chips
            SizedBox(
              height: 34,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
                itemCount: _stageFilters.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (context, idx) {
                  final stage = _stageFilters[idx];
                  final isSelected = stage == _selectedGrowthStage;
                  return GestureDetector(
                    onTap: () => setState(() => _selectedGrowthStage = stage),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: isSelected ? AgriColors.cardSurfaceLight : Colors.transparent,
                        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                        border: Border.all(
                          color: isSelected ? AgriColors.accentYellow : AgriColors.divider,
                          width: 1,
                        ),
                      ),
                      child: Text(
                        stage,
                        style: TextStyle(
                          color: isSelected ? AgriColors.accentYellow : AgriColors.textSecondary,
                          fontSize: 11,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),

            const SizedBox(height: 10),

            // Timeline Entries List
            Expanded(
              child: filteredEntries.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.menu_book_rounded, size: 54, color: AgriColors.textSecondary.withOpacity(0.5)),
                          const SizedBox(height: 12),
                          const Text(
                            'No crop health records found',
                            style: TextStyle(color: AgriColors.textWhite, fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          const Text(
                            'Tap + to log an offline disease scan or treatment',
                            style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                          ),
                        ],
                      ),
                    )
                  : ListView.separated(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AgriDimensions.screenPadding,
                        vertical: 8,
                      ),
                      itemCount: filteredEntries.length,
                      separatorBuilder: (_, __) => const SizedBox(height: AgriDimensions.cardGap),
                      itemBuilder: (context, index) {
                        final entry = filteredEntries[index];
                        return _buildDiaryCard(context, entry, diaryService);
                      },
                    ),
            ),

            // Mandatory Decision-Support Disclaimer
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding, vertical: 4),
              child: DecisionDisclaimerBanner(),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AgriColors.accentYellow,
        foregroundColor: AgriColors.darkGreenText,
        icon: const Icon(Icons.add_rounded, size: 22),
        label: const Text(
          'Log Crop Entry',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        ),
        onPressed: () => _showAddEntryModal(context),
      ),
    );
  }

  /// Builds a rich, dated crop diary timeline card
  Widget _buildDiaryCard(BuildContext context, CropDiaryModel entry, OfflineDiaryService service) {
    final textTheme = Theme.of(context).textTheme;
    final isDiseased = !(entry.diseasePrediction ?? '').toLowerCase().contains('healthy');
    final formattedDate = "${entry.entryDate.day}/${entry.entryDate.month}/${entry.entryDate.year}";

    return Container(
      decoration: BoxDecoration(
        color: AgriColors.cardSurface,
        borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
        border: Border.all(
          color: entry.isSynced ? Colors.transparent : AgriColors.accentYellow.withOpacity(0.4),
          width: 1,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header: Date + Crop + Sync Status
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    decoration: BoxDecoration(
                      color: AgriColors.cardSurfaceLight,
                      borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      entry.cropName.contains('Tomato') ? '🍅' : '🥔',
                      style: const TextStyle(fontSize: 16),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        entry.cropName,
                        style: textTheme.titleMedium?.copyWith(
                          color: AgriColors.textWhite,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                      Text(
                        '${entry.fieldName} • $formattedDate',
                        style: const TextStyle(color: AgriColors.textSecondary, fontSize: 11),
                      ),
                    ],
                  ),
                ],
              ),

              // Growth Stage Pill
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AgriColors.accentYellow,
                  borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                ),
                child: Text(
                  entry.growthStage,
                  style: const TextStyle(
                    color: AgriColors.darkGreenText,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          // Disease Prediction Badge (if diagnosed)
          if (entry.diseasePrediction != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: isDiseased ? Colors.red.withOpacity(0.2) : Colors.green.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: isDiseased ? Colors.red.withOpacity(0.4) : Colors.green.withOpacity(0.4),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    isDiseased ? Icons.coronavirus_outlined : Icons.check_circle_outline_rounded,
                    color: isDiseased ? const Color(0xFFFF8A80) : const Color(0xFFB9F6CA),
                    size: 16,
                  ),
                  const SizedBox(width: 6),
                  Expanded(
                    child: Text(
                      '${entry.diseasePrediction} (${(entry.confidence * 100).toStringAsFixed(1)}%)',
                      style: TextStyle(
                        color: isDiseased ? const Color(0xFFFF8A80) : const Color(0xFFB9F6CA),
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Text(
                    entry.severity,
                    style: TextStyle(
                      color: isDiseased ? const Color(0xFFFF8A80) : const Color(0xFFB9F6CA),
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),

          if (entry.diseasePrediction != null) const SizedBox(height: 10),

          // Farmer Notes
          if (entry.notes != null && entry.notes!.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 8.0),
              child: Text(
                '📝 ${entry.notes}',
                style: const TextStyle(
                  color: AgriColors.textWhite,
                  fontSize: 12,
                  height: 1.35,
                ),
              ),
            ),

          // Treatment Applied & Cost
          if (entry.treatmentApplied != null && entry.treatmentApplied!.isNotEmpty)
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AgriColors.cardSurfaceLight,
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Applied Treatment',
                          style: TextStyle(color: AgriColors.accentYellow, fontSize: 10, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          entry.treatmentApplied!,
                          style: const TextStyle(color: AgriColors.textWhite, fontSize: 11),
                        ),
                      ],
                    ),
                  ),
                  if (entry.costPkr > 0)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: AgriColors.cardSurface,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        'Rs. ${entry.costPkr.toStringAsFixed(0)}',
                        style: const TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ),
                ],
              ),
            ),

          const SizedBox(height: 10),

          // Bottom Bar: Sync Flag + Delete Tombstone Option
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(
                    entry.isSynced ? Icons.cloud_done_rounded : Icons.cloud_off_rounded,
                    size: 14,
                    color: entry.isSynced ? AgriColors.accentYellow : AgriColors.textSecondary,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    entry.isSynced ? 'Synced to server' : 'Saved offline (Source of truth)',
                    style: TextStyle(
                      color: entry.isSynced ? AgriColors.accentYellow : AgriColors.textSecondary,
                      fontSize: 10,
                    ),
                  ),
                ],
              ),
              IconButton(
                icon: const Icon(Icons.delete_outline_rounded, color: AgriColors.textSecondary, size: 18),
                onPressed: () async {
                  await service.deleteEntry(entry.clientUuid);
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Record soft-deleted (tombstone marked for sync)')),
                    );
                  }
                },
              ),
            ],
          ),
        ],
      ),
    );
  }

  /// Bottom sheet to add new diary entry offline
  void _showAddEntryModal(BuildContext context) {
    final diaryService = Provider.of<OfflineDiaryService>(context, listen: false);
    final formKey = GlobalKey<FormState>();

    String crop = 'Potato (آلو)';
    String fieldName = 'Okara North Block 3';
    String growthStage = 'Vegetative';
    String? disease = 'Potato Late Blight';
    double confidence = 0.92;
    String? notes = '';
    String? treatment = 'Ridomil Gold @ 250g/100L foliar spray';
    double cost = 2800.0;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: AgriColors.backgroundDark,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
            left: 20,
            right: 20,
            top: 20,
          ),
          child: Form(
            key: formKey,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Log Crop Health Observation',
                        style: TextStyle(color: AgriColors.textWhite, fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      IconButton(
                        icon: const Icon(Icons.close_rounded, color: AgriColors.textWhite),
                        onPressed: () => Navigator.pop(ctx),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Crop Selector
                  DropdownButtonFormField<String>(
                    value: crop,
                    dropdownColor: AgriColors.backgroundDark,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Crop', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    items: const [
                      DropdownMenuItem(value: 'Potato (آلو)', child: Text('🥔 Potato (آلو)')),
                      DropdownMenuItem(value: 'Tomato (ٹماٹر)', child: Text('🍅 Tomato (ٹماٹر)')),
                    ],
                    onChanged: (v) => setModalState(() => crop = v!),
                  ),

                  // Growth Stage
                  DropdownButtonFormField<String>(
                    value: growthStage,
                    dropdownColor: AgriColors.backgroundDark,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Growth Stage', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    items: const [
                      DropdownMenuItem(value: 'Emergence', child: Text('Emergence')),
                      DropdownMenuItem(value: 'Vegetative', child: Text('Vegetative')),
                      DropdownMenuItem(value: 'Flowering/Fruit Set', child: Text('Flowering/Fruit Set')),
                      DropdownMenuItem(value: 'Tuber Bulking/Ripening', child: Text('Tuber Bulking/Ripening')),
                      DropdownMenuItem(value: 'Harvest Ready', child: Text('Harvest Ready')),
                    ],
                    onChanged: (v) => setModalState(() => growthStage = v!),
                  ),

                  // Field Name
                  TextFormField(
                    initialValue: fieldName,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Field / Plot Identifier', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    onSaved: (v) => fieldName = v ?? 'Main Field',
                  ),

                  // Disease Diagnosis
                  TextFormField(
                    initialValue: disease,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Disease / Diagnosis Result', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    onSaved: (v) => disease = v,
                  ),

                  // Notes
                  TextFormField(
                    maxLines: 2,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Farmer Field Observations & Notes', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    onSaved: (v) => notes = v,
                  ),

                  // Treatment
                  TextFormField(
                    initialValue: treatment,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Treatment Applied', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    onSaved: (v) => treatment = v,
                  ),

                  // Cost (PKR)
                  TextFormField(
                    initialValue: cost.toString(),
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 13),
                    decoration: const InputDecoration(labelText: 'Cost in PKR', labelStyle: TextStyle(color: AgriColors.textSecondary)),
                    onSaved: (v) => cost = double.tryParse(v ?? '0') ?? 0.0,
                  ),

                  const SizedBox(height: 18),

                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AgriColors.accentYellow,
                      foregroundColor: AgriColors.darkGreenText,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AgriDimensions.pillRadius)),
                      minimumSize: const Size.fromHeight(48),
                    ),
                    onPressed: () async {
                      formKey.currentState?.save();
                      final now = DateTime.now();
                      final newEntry = CropDiaryModel(
                        clientUuid: 'local-uuid-${DateTime.now().millisecondsSinceEpoch}',
                        cropName: crop,
                        fieldName: fieldName,
                        growthStage: growthStage,
                        entryDate: now,
                        activityType: 'Monitoring & Treatment',
                        diseasePrediction: disease,
                        confidence: confidence,
                        severity: 'Moderate',
                        notes: notes,
                        treatmentApplied: treatment,
                        costPkr: cost,
                        clientUpdatedAt: now,
                        isSynced: false,
                      );
                      await diaryService.addEntry(newEntry);
                      if (ctx.mounted) Navigator.pop(ctx);
                    },
                    child: const Text('Save Locally (Offline-First)', style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
