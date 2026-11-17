/// AgriMate AI - Buyer Profile & Preferences Tab
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../services/auth_provider.dart';
import '../../../../services/buyer_provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../widgets/buyer/state_views.dart';

class BuyerProfileTab extends StatefulWidget {
  const BuyerProfileTab({super.key});

  @override
  State<BuyerProfileTab> createState() => _BuyerProfileTabState();
}

class _BuyerProfileTabState extends State<BuyerProfileTab> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController _nameController;
  late TextEditingController _contactController;
  late TextEditingController _locationController;
  late TextEditingController _minQtyController;
  late TextEditingController _maxQtyController;
  late TextEditingController _budgetController;

  List<String> _selectedCrops = ['Potato', 'Tomato'];
  String _selectedGrade = 'A';
  bool _isSaving = false;

  final List<String> _availableCrops = ['Potato', 'Tomato', 'Wheat'];
  final List<String> _availableGrades = ['A', 'B', 'C'];

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _contactController = TextEditingController();
    _locationController = TextEditingController();
    _minQtyController = TextEditingController();
    _maxQtyController = TextEditingController();
    _budgetController = TextEditingController();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _populateFromProfile();
    });
  }

  void _populateFromProfile() {
    final buyerProv = Provider.of<BuyerProvider>(context, listen: false);
    final p = buyerProv.profile;
    if (p != null) {
      _nameController.text = p.name;
      _contactController.text = p.phoneOrEmail;
      _locationController.text = p.location;
      _minQtyController.text = p.minQty.toStringAsFixed(0);
      _maxQtyController.text = p.maxQty.toStringAsFixed(0);
      _budgetController.text = p.maxBudgetPrice.toStringAsFixed(0);
      setState(() {
        _selectedCrops = List.from(p.preferredCrops);
        _selectedGrade = p.preferredGrade;
      });
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _contactController.dispose();
    _locationController.dispose();
    _minQtyController.dispose();
    _maxQtyController.dispose();
    _budgetController.dispose();
    super.dispose();
  }

  Future<void> _savePreferences() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedCrops.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select at least one preferred commodity crop.'),
          backgroundColor: AgriColors.warning,
        ),
      );
      return;
    }

    setState(() => _isSaving = true);
    final buyerProv = Provider.of<BuyerProvider>(context, listen: false);

    final payload = {
      'name': _nameController.text.trim(),
      'phone_or_email': _contactController.text.trim(),
      'location': _locationController.text.trim(),
      'preferred_crops': _selectedCrops,
      'preferred_grade': _selectedGrade,
      'min_qty': double.tryParse(_minQtyController.text.trim()) ?? 1000.0,
      'max_qty': double.tryParse(_maxQtyController.text.trim()) ?? 10000.0,
      'max_budget_price': double.tryParse(_budgetController.text.trim()) ?? 2600.0,
    };

    final success = await buyerProv.updateProfile(payload);
    setState(() => _isSaving = false);

    if (mounted) {
      if (success) {
        buyerProv.refreshAll();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile and trading preferences saved successfully!'),
            backgroundColor: AgriColors.primaryGreen,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(buyerProv.profileError ?? 'Failed to update preferences'),
            backgroundColor: AgriColors.error,
          ),
        );
      }
    }
  }

  void _showLogoutDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AgriColors.background,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
        ),
        title: const Text('Log Out', style: TextStyle(fontWeight: FontWeight.bold)),
        content: const Text('Are you sure you want to log out of AgriMate AI?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel', style: TextStyle(color: AgriColors.textSecondary)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AgriColors.error),
            onPressed: () {
              Navigator.pop(ctx);
              Provider.of<AuthProvider>(context, listen: false).logout();
            },
            child: const Text('Log Out'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);

    if (buyerProv.isLoadingProfile && buyerProv.profile == null) {
      return const BuyerLoadingView(message: 'Loading trading profile...');
    }

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 14),

                // Profile Header Card
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  decoration: AppTheme.cardDecoration(),
                  child: Row(
                    children: [
                      Container(
                        width: 56,
                        height: 56,
                        decoration: const BoxDecoration(
                          color: AgriColors.cardSurfaceLight,
                          shape: BoxShape.circle,
                        ),
                        alignment: Alignment.center,
                        child: const Icon(Icons.person_rounded, size: 30, color: AgriColors.primaryGreen),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              buyerProv.profile?.name ?? 'Buyer Account',
                              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                                    fontSize: 18,
                                    fontWeight: FontWeight.w700,
                                  ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              'Role: Buyer • Role Restricted (403 Protected)',
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    color: AgriColors.primaryGreen,
                                    fontWeight: FontWeight.w600,
                                  ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // Section 1: Contact & Location Info
                Text(
                  'Account Information',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                      ),
                ),
                const SizedBox(height: 12),

                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: 'Full Name / Company',
                    prefixIcon: Icon(Icons.business_outlined, size: 20, color: AgriColors.iconOutline),
                  ),
                  validator: (val) => val == null || val.trim().isEmpty ? 'Enter name' : null,
                ),
                const SizedBox(height: 12),

                TextFormField(
                  controller: _contactController,
                  decoration: const InputDecoration(
                    labelText: 'Phone or Email',
                    prefixIcon: Icon(Icons.phone_outlined, size: 20, color: AgriColors.iconOutline),
                  ),
                  validator: (val) => val == null || val.trim().isEmpty ? 'Enter contact' : null,
                ),
                const SizedBox(height: 12),

                TextFormField(
                  controller: _locationController,
                  decoration: const InputDecoration(
                    labelText: 'Mandi Terminal / Delivery Location',
                    prefixIcon: Icon(Icons.location_on_outlined, size: 20, color: AgriColors.iconOutline),
                  ),
                  validator: (val) => val == null || val.trim().isEmpty ? 'Enter location' : null,
                ),

                const SizedBox(height: 24),

                // Section 2: Trading & Match Preferences
                Text(
                  'Trading Preferences & Match Criteria',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                      ),
                ),
                const SizedBox(height: 6),
                Text(
                  'The deterministic matching engine matches produce listings based on these settings.',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontSize: 12.5),
                ),

                const SizedBox(height: 14),

                // Preferred Crops
                Text(
                  'Preferred Crops (Mandatory Crop Match Gate)',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 8,
                  children: _availableCrops.map((crop) {
                    final isSelected = _selectedCrops.contains(crop);
                    return FilterChip(
                      label: Text(crop),
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
                        setState(() {
                          if (val) {
                            _selectedCrops.add(crop);
                          } else {
                            _selectedCrops.remove(crop);
                          }
                        });
                      },
                    );
                  }).toList(),
                ),

                const SizedBox(height: 18),

                // Preferred Grade
                Text(
                  'Preferred Minimum Grade',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 8,
                  children: _availableGrades.map((g) {
                    final isSelected = _selectedGrade == g;
                    return ChoiceChip(
                      label: Text('Grade $g'),
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

                const SizedBox(height: 18),

                // Typical Quantity Range (Min and Max)
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _minQtyController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Min Quantity (kg)',
                          prefixIcon: Icon(Icons.scale_outlined, size: 18, color: AgriColors.iconOutline),
                        ),
                        validator: (val) => val == null || val.trim().isEmpty ? 'Enter min qty' : null,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextFormField(
                        controller: _maxQtyController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Max Quantity (kg)',
                          prefixIcon: Icon(Icons.scale_outlined, size: 18, color: AgriColors.iconOutline),
                        ),
                        validator: (val) => val == null || val.trim().isEmpty ? 'Enter max qty' : null,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 14),

                // Max Budget Price
                TextFormField(
                  controller: _budgetController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Target / Max Budget Price (PKR / 40kg maund)',
                    prefixIcon: Icon(Icons.sell_outlined, size: 18, color: AgriColors.iconOutline),
                  ),
                  validator: (val) => val == null || val.trim().isEmpty ? 'Enter target budget' : null,
                ),

                const SizedBox(height: 24),

                // Save Preferences Button
                SizedBox(
                  width: double.infinity,
                  height: 52,
                  child: ElevatedButton(
                    onPressed: _isSaving ? null : _savePreferences,
                    child: _isSaving
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(AgriColors.textWhite),
                            ),
                          )
                        : const Text('Save Preferences'),
                  ),
                ),

                const SizedBox(height: 14),

                // Logout Button
                SizedBox(
                  width: double.infinity,
                  height: 48,
                  child: OutlinedButton.icon(
                    onPressed: _showLogoutDialog,
                    icon: const Icon(Icons.logout_rounded, size: 18, color: AgriColors.error),
                    label: const Text('Log Out', style: TextStyle(color: AgriColors.error, fontWeight: FontWeight.w700)),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: AgriColors.error, width: 1.2),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 36),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
