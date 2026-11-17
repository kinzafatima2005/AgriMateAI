import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/auth_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/decision_disclaimer_banner.dart';
import 'farm_overview_screen.dart';
import '../scan/disease_camera_screen.dart';
import '../advisory/advisor_chat_screen.dart';
import '../diary/crop_diary_screen.dart';

/// SCREEN 2 – HOME DASHBOARD (Farmer)
/// Header: "Hello, [Name]" with location line (pin icon + city) and round translucent bell & settings
/// Weather card: large temperature (34°), location, yellow cloud icon, divider line, 4 mini stats
/// Horizontally scrollable filter chips: All (active, yellow), Fruit, Orchards, Grains
/// "My Fields" cards: circular thumbnail, field name, location, yellow pill with yield, large rounded aerial field photo
class FarmerHomeScreen extends StatefulWidget {
  const FarmerHomeScreen({super.key});

  @override
  State<FarmerHomeScreen> createState() => _FarmerHomeScreenState();
}

class _FarmerHomeScreenState extends State<FarmerHomeScreen> {
  String _activeFilter = 'All';
  final List<String> _filters = ['All', 'Fruit', 'Orchards', 'Grains'];

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final auth = Provider.of<AuthProvider>(context);
    final user = auth.currentUser;
    final userName = user != null ? user.name.split(' ').first : 'Muhammad';
    final userLocation = user != null ? user.location : 'Multan, Punjab';

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),

              // 1. Header: "Hello, [Name]" + Location + Translucent Bell & Settings Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Hello, $userName',
                        style: textTheme.headlineLarge?.copyWith(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: AgriColors.textWhite,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          const Icon(
                            Icons.location_on_outlined,
                            color: AgriColors.accentYellow,
                            size: 15,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            userLocation,
                            style: textTheme.bodyMedium?.copyWith(
                              color: AgriColors.textSecondary,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),

                  // Translucent round bell & settings buttons
                  Row(
                    children: [
                      _buildRoundIconButton(
                        icon: Icons.notifications_none_rounded,
                        onTap: () {},
                      ),
                      const SizedBox(width: 10),
                      _buildRoundIconButton(
                        icon: Icons.tune_rounded,
                        onTap: () => _showSettingsSheet(context),
                      ),
                    ],
                  ),
                ],
              ),

              const SizedBox(height: AgriDimensions.cardGap + 6),

              // 2. Weather Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(22),
                decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                child: Column(
                  children: [
                    // Top Weather Row: Temp (34°) + Location + Yellow Cloud Icon
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '34°',
                              style: textTheme.displayLarge?.copyWith(
                                fontSize: 44,
                                fontWeight: FontWeight.bold,
                                color: AgriColors.textWhite,
                                height: 1.0,
                              ),
                            ),
                            const SizedBox(height: 6),
                            Row(
                              children: [
                                Text(
                                  userLocation,
                                  style: textTheme.bodyMedium?.copyWith(
                                    color: AgriColors.textSecondary,
                                    fontSize: 13,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AgriColors.cardSurfaceLight,
                                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                  ),
                                  child: Text(
                                    'Sunny & Clear',
                                    style: textTheme.labelSmall?.copyWith(
                                      color: AgriColors.accentYellow,
                                      fontSize: 11,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),

                        // Yellow Cloud & Sun Outline Icon
                        Container(
                          width: 52,
                          height: 52,
                          decoration: BoxDecoration(
                            color: AgriColors.cardSurfaceLight,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(
                            Icons.wb_sunny_outlined,
                            color: AgriColors.iconHighlight,
                            size: 28,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 18),
                    const Divider(),
                    const SizedBox(height: 14),

                    // Row of 4 mini stats: wind 5km/h, humidity 88%, rain 5mm, feels-like +24°C
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _buildMiniStat(label: 'Wind', value: '5 km/h', icon: Icons.air_rounded),
                        _buildMiniStat(label: 'Humidity', value: '88%', icon: Icons.water_drop_outlined),
                        _buildMiniStat(label: 'Rain', value: '5 mm', icon: Icons.grain_rounded),
                        _buildMiniStat(label: 'Feels-like', value: '+24°C', icon: Icons.thermostat_rounded),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AgriDimensions.cardGap + 6),

              // Disease Screening Quick-Action Card with Grad-CAM Badge
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const DiseaseCameraScreen()),
                  );
                },
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                    border: Border.all(color: AgriColors.accentYellow.withOpacity(0.4), width: 1.5),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 48,
                        height: 48,
                        decoration: const BoxDecoration(
                          color: AgriColors.accentYellow,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.document_scanner_rounded, color: AgriColors.darkGreenText, size: 26),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  'Scan Leaf Disease',
                                  style: TextStyle(
                                    color: AgriColors.textWhite,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AgriColors.accentYellow,
                                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                  ),
                                  child: const Text(
                                    'Grad-CAM',
                                    style: TextStyle(color: AgriColors.darkGreenText, fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 2),
                            const Text(
                              'Offline TFLite diagnosis & visual heatmap',
                              style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios_rounded, color: AgriColors.accentYellow, size: 16),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 10),

              // Crop-Health Diary (Phase 5: Offline-First SQLite Sync)
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CropDiaryScreen()),
                  );
                },
                child: Container(
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurface,
                    borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                    border: Border.all(color: AgriColors.cardSurfaceLight),
                  ),
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          color: AgriColors.accentYellow.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                          border: Border.all(color: AgriColors.accentYellow),
                        ),
                        child: const Icon(Icons.book_rounded, color: AgriColors.accentYellow, size: 22),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  'Crop-Health Diary',
                                  style: TextStyle(
                                    color: AgriColors.textWhite,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AgriColors.cardSurfaceLight,
                                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                  ),
                                  child: const Text(
                                    'Offline-First Sync',
                                    style: TextStyle(color: AgriColors.accentYellow, fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 2),
                            const Text(
                              'Dated photos, growth stages, treatments & 2-way sync',
                              style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios_rounded, color: AgriColors.accentYellow, size: 16),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 10),

              // Phase 3: Citation-Backed RAG Advisor Card
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const AdvisorChatScreen()),
                  );
                },
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurface,
                    borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                    border: Border.all(color: AgriColors.divider),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 48,
                        height: 48,
                        decoration: BoxDecoration(
                          color: AgriColors.cardSurfaceLight,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.chat_bubble_outline_rounded, color: AgriColors.accentYellow, size: 24),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  'Ask AI Agronomist',
                                  style: TextStyle(
                                    color: AgriColors.textWhite,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AgriColors.cardSurfaceLight,
                                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                  ),
                                  child: const Text(
                                    'PARC Grounded',
                                    style: TextStyle(color: AgriColors.accentYellow, fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 2),
                            const Text(
                              'Urdu & English voice/text chat with citations',
                              style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios_rounded, color: AgriColors.accentYellow, size: 16),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 10),

              // Crop-Health Diary (Phase 5: Offline-First SQLite Sync)
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CropDiaryScreen()),
                  );
                },
                child: Container(
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurface,
                    borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                    border: Border.all(color: AgriColors.cardSurfaceLight),
                  ),
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          color: AgriColors.accentYellow.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                          border: Border.all(color: AgriColors.accentYellow),
                        ),
                        child: const Icon(Icons.book_rounded, color: AgriColors.accentYellow, size: 22),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  'Crop-Health Diary',
                                  style: TextStyle(
                                    color: AgriColors.textWhite,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AgriColors.cardSurfaceLight,
                                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                  ),
                                  child: const Text(
                                    'Offline-First Sync',
                                    style: TextStyle(color: AgriColors.accentYellow, fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 2),
                            const Text(
                              'Dated photos, growth stages, treatments & 2-way sync',
                              style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios_rounded, color: AgriColors.accentYellow, size: 16),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: AgriDimensions.cardGap + 6),

              // 3. Horizontally Scrollable Filter Chips: All (active, yellow), Fruit, Orchards, Grains
              SizedBox(
                height: 42,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  physics: const BouncingScrollPhysics(),
                  itemCount: _filters.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 10),
                  itemBuilder: (context, index) {
                    final item = _filters[index];
                    final isActive = item == _activeFilter;
                    return GestureDetector(
                      onTap: () => setState(() => _activeFilter = item),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 10),
                        decoration: AppTheme.pillChipDecoration(isActive: isActive),
                        alignment: Alignment.center,
                        child: Text(
                          item,
                          style: textTheme.labelSmall?.copyWith(
                            color: isActive ? AgriColors.darkGreenText : AgriColors.textWhite,
                            fontWeight: isActive ? FontWeight.bold : FontWeight.w500,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),

              const SizedBox(height: AgriDimensions.cardGap + 8),

              // Section Header: "My Fields"
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'My Fields',
                    style: textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AgriColors.textWhite,
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const FarmOverviewScreen()),
                      );
                    },
                    child: Row(
                      children: [
                        Text(
                          'View Overview',
                          style: textTheme.labelSmall?.copyWith(
                            color: AgriColors.accentYellow,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(width: 4),
                        const Icon(Icons.arrow_forward_ios_rounded, size: 12, color: AgriColors.accentYellow),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              // 4. "My Fields" Card 1 (Tap opens Farm Overview)
              _buildFieldCard(
                fieldName: 'Chak 12-WB Cotton Field',
                location: 'Multan, South Punjab',
                yieldText: '7200 kg/ha',
                imagePath: 'assets/field_aerial.jpg',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const FarmOverviewScreen()),
                  );
                },
              ),

              const SizedBox(height: AgriDimensions.cardGap),

              // "My Fields" Card 2
              _buildFieldCard(
                fieldName: 'Riverbed Wheat Acreage',
                location: 'Khanewal Canal Zone',
                yieldText: '5400 kg/ha',
                imagePath: 'assets/field_aerial_header.jpg',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const FarmOverviewScreen()),
                  );
                },
              ),

              const SizedBox(height: 18),
              const DecisionDisclaimerBanner(compact: true),
              const SizedBox(height: 28),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRoundIconButton({required IconData icon, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          color: AgriColors.cardSurface,
          shape: BoxShape.circle,
        ),
        child: Icon(icon, color: AgriColors.iconOutline, size: 20),
      ),
    );
  }

  Widget _buildMiniStat({required String label, required String value, required IconData icon}) {
    return Column(
      children: [
        Icon(icon, color: AgriColors.iconHighlight, size: 18),
        const SizedBox(height: 6),
        Text(
          value,
          style: const TextStyle(
            color: AgriColors.textWhite,
            fontWeight: FontWeight.bold,
            fontSize: 13,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: const TextStyle(
            color: AgriColors.textSecondary,
            fontSize: 11,
          ),
        ),
      ],
    );
  }

  Widget _buildFieldCard({
    required String fieldName,
    required String location,
    required String yieldText,
    required String imagePath,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(18),
        decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top row: Circular thumbnail + Name/Location + Yellow Pill Yield
            Row(
              children: [
                // Circular thumbnail
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    shape: BoxShape.circle,
                  ),
                  child: ClipOval(
                    child: Image.asset(
                      imagePath,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => const Icon(
                        Icons.grass_rounded,
                        color: AgriColors.accentYellow,
                        size: 22,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        fieldName,
                        style: const TextStyle(
                          color: AgriColors.textWhite,
                          fontWeight: FontWeight.bold,
                          fontSize: 15,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        location,
                        style: const TextStyle(
                          color: AgriColors.textSecondary,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
                // Yellow Pill with Yield
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                  decoration: BoxDecoration(
                    color: AgriColors.accentYellow,
                    borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                  ),
                  child: Text(
                    yieldText,
                    style: const TextStyle(
                      color: AgriColors.darkGreenText,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 16),

            // Large rounded aerial field photo below
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: Image.asset(
                imagePath,
                width: double.infinity,
                height: 160,
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => Container(
                  height: 160,
                  color: AgriColors.cardSurfaceLight,
                  alignment: Alignment.center,
                  child: const Icon(
                    Icons.landscape_rounded,
                    color: AgriColors.textSecondary,
                    size: 48,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showSettingsSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: AgriColors.backgroundDark,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) {
        final auth = Provider.of<AuthProvider>(context, listen: false);
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Account & Role Settings',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: AgriColors.textWhite,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close_rounded, color: AgriColors.textWhite),
                      onPressed: () => Navigator.pop(ctx),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                ListTile(
                  leading: const Icon(Icons.person_outline, color: AgriColors.accentYellow),
                  title: Text(auth.currentUser?.name ?? 'User', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(
                    'Role: ${auth.currentUser?.role ?? 'Farmer'} | ${auth.currentUser?.location ?? 'Pakistan'}',
                    style: const TextStyle(color: AgriColors.textSecondary),
                  ),
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.logout_rounded, color: AgriColors.error),
                  title: const Text('Sign Out', style: TextStyle(color: AgriColors.error, fontWeight: FontWeight.bold)),
                  onTap: () async {
                    Navigator.pop(ctx);
                    await auth.logout();
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

