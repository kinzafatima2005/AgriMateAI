/// AgriMate AI - Buyer Listings Filter Bottom Sheet
import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class FilterBottomSheet extends StatefulWidget {
  final String currentCrop;
  final String currentGrade;
  final double? currentMinQty;
  final double? currentMaxDistanceKm;
  final String currentSort;
  final Function({
    required String crop,
    required String grade,
    required double? minQty,
    required double? maxDistanceKm,
    required String sort,
  }) onApply;

  const FilterBottomSheet({
    super.key,
    required this.currentCrop,
    required this.currentGrade,
    required this.currentMinQty,
    required this.currentMaxDistanceKm,
    required this.currentSort,
    required this.onApply,
  });

  @override
  State<FilterBottomSheet> createState() => _FilterBottomSheetState();
}

class _FilterBottomSheetState extends State<FilterBottomSheet> {
  late String _selectedCrop;
  late String _selectedGrade;
  late double _minQty;
  late double _maxDistance;
  late String _selectedSort;

  final List<String> _crops = ['All', 'Potato', 'Tomato', 'Wheat'];
  final List<String> _grades = ['All', 'A', 'B', 'C'];
  final List<Map<String, String>> _sortOptions = [
    {'value': 'nearest', 'label': 'Nearest Location'},
    {'value': 'price_low_high', 'label': 'Price: Low to High'},
    {'value': 'newest', 'label': 'Newest Listings'},
    {'value': 'best_match', 'label': 'Highest Match Score'},
  ];

  @override
  void initState() {
    super.initState();
    _selectedCrop = widget.currentCrop;
    _selectedGrade = widget.currentGrade;
    _minQty = widget.currentMinQty ?? 0.0;
    _maxDistance = widget.currentMaxDistanceKm ?? 350.0;
    _selectedSort = widget.currentSort;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: AgriColors.background,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: EdgeInsets.only(
        top: 20,
        left: AgriDimensions.screenPadding,
        right: AgriDimensions.screenPadding,
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Handle bar
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: AgriColors.cardBorder,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Title & Reset
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Filter & Sort Listings',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                      ),
                ),
                TextButton(
                  onPressed: () {
                    setState(() {
                      _selectedCrop = 'All';
                      _selectedGrade = 'All';
                      _minQty = 0.0;
                      _maxDistance = 350.0;
                      _selectedSort = 'nearest';
                    });
                  },
                  child: Text(
                    'Reset All',
                    style: TextStyle(
                      color: AgriColors.primaryGreen,
                      fontWeight: FontWeight.w600,
                      fontSize: 13,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 18),

            // Crop Filter Pills
            Text(
              'Commodity / Crop',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.textPrimary,
                  ),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _crops.map((c) {
                final isSelected = _selectedCrop == c;
                return ChoiceChip(
                  label: Text(c),
                  selected: isSelected,
                  selectedColor: AgriColors.primaryGreen,
                  backgroundColor: AgriColors.cardSurfaceLight,
                  labelStyle: TextStyle(
                    color: isSelected ? AgriColors.textWhite : AgriColors.textPrimary,
                    fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                    fontSize: 13,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                    side: BorderSide(
                      color: isSelected ? AgriColors.primaryGreen : AgriColors.cardBorder,
                    ),
                  ),
                  onSelected: (val) {
                    if (val) setState(() => _selectedCrop = c);
                  },
                );
              }).toList(),
            ),

            const SizedBox(height: 20),

            // Grade Filter Pills
            Text(
              'Grade Threshold',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.textPrimary,
                  ),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              children: _grades.map((g) {
                final isSelected = _selectedGrade == g;
                return ChoiceChip(
                  label: Text(g == 'All' ? 'All Grades' : 'Grade $g'),
                  selected: isSelected,
                  selectedColor: AgriColors.primaryGreen,
                  backgroundColor: AgriColors.cardSurfaceLight,
                  labelStyle: TextStyle(
                    color: isSelected ? AgriColors.textWhite : AgriColors.textPrimary,
                    fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                    fontSize: 13,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                    side: BorderSide(
                      color: isSelected ? AgriColors.primaryGreen : AgriColors.cardBorder,
                    ),
                  ),
                  onSelected: (val) {
                    if (val) setState(() => _selectedGrade = g);
                  },
                );
              }).toList(),
            ),

            const SizedBox(height: 20),

            // Minimum Quantity Slider
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Minimum Available Quantity',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                Text(
                  _minQty <= 0 ? 'Any Quantity' : '${_minQty.toStringAsFixed(0)} kg',
                  style: TextStyle(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.primaryGreen,
                    fontSize: 13,
                  ),
                ),
              ],
            ),
            Slider(
              value: _minQty,
              min: 0.0,
              max: 20000.0,
              divisions: 20,
              activeColor: AgriColors.primaryGreen,
              inactiveColor: AgriColors.cardSurfaceLight,
              onChanged: (val) => setState(() => _minQty = val),
            ),

            const SizedBox(height: 12),

            // Max Distance Slider
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Maximum Radius / Distance',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                Text(
                  '${_maxDistance.toStringAsFixed(0)} km',
                  style: TextStyle(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.primaryGreen,
                    fontSize: 13,
                  ),
                ),
              ],
            ),
            Slider(
              value: _maxDistance,
              min: 20.0,
              max: 500.0,
              divisions: 24,
              activeColor: AgriColors.primaryGreen,
              inactiveColor: AgriColors.cardSurfaceLight,
              onChanged: (val) => setState(() => _maxDistance = val),
            ),

            const SizedBox(height: 16),

            // Sort Options
            Text(
              'Sort Results By',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.textPrimary,
                  ),
            ),
            const SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                color: AgriColors.cardSurfaceLight,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AgriColors.cardBorder, width: 1),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 14),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _selectedSort,
                  isExpanded: true,
                  dropdownColor: AgriColors.cardSurface,
                  items: _sortOptions
                      .map((opt) => DropdownMenuItem(
                            value: opt['value'],
                            child: Text(
                              opt['label']!,
                              style: const TextStyle(
                                color: AgriColors.textPrimary,
                                fontWeight: FontWeight.w600,
                                fontSize: 13.5,
                              ),
                            ),
                          ))
                      .toList(),
                  onChanged: (val) {
                    if (val != null) setState(() => _selectedSort = val);
                  },
                ),
              ),
            ),

            const SizedBox(height: 26),

            // Apply Button
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: () {
                  widget.onApply(
                    crop: _selectedCrop,
                    grade: _selectedGrade,
                    minQty: _minQty > 0 ? _minQty : null,
                    maxDistanceKm: _maxDistance,
                    sort: _selectedSort,
                  );
                  Navigator.pop(context);
                },
                child: const Text('Apply Filters & Sort'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
