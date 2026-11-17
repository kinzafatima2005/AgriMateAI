import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../widgets/custom_gauge.dart';
import '../../widgets/decision_disclaimer_banner.dart';

/// SCREEN 3 – FARM OVERVIEW
/// Full-bleed aerial farmland photo as header, fading into the green background
/// Weather temperature & icon overlaid on the photo
/// Two side-by-side cards:
///   1. "My Farm" with semicircular yellow gauge (white knob) and "Workers 48"
///   2. "Farm Acres" with a photo background and "Acres 848"
/// Full-width "Water" card with yellow droplet icon, status text "Dangerous level", and a circular arrow button
class FarmOverviewScreen extends StatelessWidget {
  const FarmOverviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: Column(
          children: [
            // 1. Full-bleed Aerial Farmland Photo Header Fading into Green Background
            Stack(
              children: [
                // Farmland Image
                Image.asset(
                  'assets/field_aerial_header.jpg',
                  width: double.infinity,
                  height: 330,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(
                    height: 330,
                    color: AgriColors.backgroundDark,
                  ),
                ),

                // Smooth Gradient Fade into the olive green background
                Positioned.fill(
                  child: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        stops: const [0.0, 0.45, 0.85, 1.0],
                        colors: [
                          Colors.black.withOpacity(0.35),
                          Colors.transparent,
                          AgriColors.background.withOpacity(0.85),
                          AgriColors.background,
                        ],
                      ),
                    ),
                  ),
                ),

                // Top Navigation (Back button + Title)
                SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AgriDimensions.screenPadding,
                      vertical: 10,
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        GestureDetector(
                          onTap: () => Navigator.pop(context),
                          child: Container(
                            width: 44,
                            height: 44,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(
                              Icons.arrow_back_ios_new_rounded,
                              color: AgriColors.textWhite,
                              size: 18,
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.35),
                            borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                          ),
                          child: Text(
                            'Farm Overview',
                            style: textTheme.labelSmall?.copyWith(
                              color: AgriColors.textWhite,
                              fontWeight: FontWeight.bold,
                              fontSize: 13,
                            ),
                          ),
                        ),
                        const SizedBox(width: 44), // Balancer
                      ],
                    ),
                  ),
                ),

                // Weather Temperature & Yellow Icon Overlaid on the Photo
                Positioned(
                  left: AgriDimensions.screenPadding,
                  bottom: 24,
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        '34°',
                        style: textTheme.displayLarge?.copyWith(
                          fontSize: 48,
                          fontWeight: FontWeight.bold,
                          color: AgriColors.textWhite,
                          height: 1.0,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: const [
                              Icon(
                                Icons.wb_sunny_outlined,
                                color: AgriColors.iconHighlight,
                                size: 24,
                              ),
                              SizedBox(width: 6),
                              Text(
                                'Clear Sky',
                                style: TextStyle(
                                  color: AgriColors.textWhite,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 2),
                          const Text(
                            'Multan Agro Zone',
                            style: TextStyle(
                              color: AgriColors.textSecondary,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),

            // Content Body
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
              child: Column(
                children: [
                  const SizedBox(height: 6),

                  // 2. Two Side-by-Side Cards
                  Row(
                    children: [
                      // Card 1: "My Farm" with semicircular yellow gauge & "Workers 48"
                      Expanded(
                        child: Container(
                          height: 195,
                          padding: const EdgeInsets.all(18),
                          decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const Text(
                                'My Farm',
                                style: TextStyle(
                                  color: AgriColors.textWhite,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 16,
                                ),
                              ),
                              // Semicircular yellow gauge with white knob
                              const Center(
                                child: SemicircularGauge(progress: 0.76, size: 120),
                              ),
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  const Text(
                                    'Workers',
                                    style: TextStyle(
                                      color: AgriColors.textSecondary,
                                      fontSize: 13,
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                                    decoration: BoxDecoration(
                                      color: AgriColors.cardSurfaceLight,
                                      borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                                    ),
                                    child: const Text(
                                      '48',
                                      style: TextStyle(
                                        color: AgriColors.textWhite,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 13,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(width: AgriDimensions.cardGap),

                      // Card 2: "Farm Acres" with photo background and "Acres 848"
                      Expanded(
                        child: Container(
                          height: 195,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                            image: const DecorationImage(
                              image: AssetImage('assets/field_aerial.jpg'),
                              fit: BoxFit.cover,
                            ),
                          ),
                          child: Container(
                            padding: const EdgeInsets.all(18),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                              gradient: LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomCenter,
                                colors: [
                                  Colors.black.withOpacity(0.3),
                                  Colors.black.withOpacity(0.75),
                                ],
                              ),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    const Text(
                                      'Farm Acres',
                                      style: TextStyle(
                                        color: AgriColors.textWhite,
                                        fontWeight: FontWeight.w600,
                                        fontSize: 16,
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.all(6),
                                      decoration: BoxDecoration(
                                        color: Colors.white.withOpacity(0.18),
                                        shape: BoxShape.circle,
                                      ),
                                      child: const Icon(
                                        Icons.crop_free_rounded,
                                        color: AgriColors.accentYellow,
                                        size: 14,
                                      ),
                                    ),
                                  ],
                                ),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: const [
                                    Text(
                                      '848',
                                      style: TextStyle(
                                        color: AgriColors.textWhite,
                                        fontSize: 34,
                                        fontWeight: FontWeight.bold,
                                        height: 1.0,
                                      ),
                                    ),
                                    SizedBox(height: 4),
                                    Text(
                                      'Total Cultivated',
                                      style: TextStyle(
                                        color: AgriColors.textSecondary,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: AgriDimensions.cardGap),

                  // 3. Full-width "Water" card with yellow droplet icon, "Dangerous level", circular arrow button
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                    decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            // Yellow Droplet Icon Badge
                            Container(
                              width: 48,
                              height: 48,
                              decoration: BoxDecoration(
                                color: AgriColors.cardSurfaceLight,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.water_drop_outlined,
                                color: AgriColors.iconHighlight,
                                size: 26,
                              ),
                            ),
                            const SizedBox(width: 14),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Water Canal Storage',
                                  style: TextStyle(
                                    color: AgriColors.textWhite,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                ),
                                const SizedBox(height: 3),
                                Row(
                                  children: [
                                    Container(
                                      width: 8,
                                      height: 8,
                                      decoration: const BoxDecoration(
                                        color: AgriColors.accentYellow,
                                        shape: BoxShape.circle,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    const Text(
                                      'Dangerous level',
                                      style: TextStyle(
                                        color: AgriColors.accentYellow,
                                        fontWeight: FontWeight.w600,
                                        fontSize: 13,
                                      ),
                                    ),
                                    const Text(
                                      ' (18% capacity)',
                                      style: TextStyle(
                                        color: AgriColors.textSecondary,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ],
                        ),

                        // Circular Arrow Button
                        Container(
                          width: 44,
                          height: 44,
                          decoration: BoxDecoration(
                            color: AgriColors.cardSurfaceLight,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(
                            Icons.arrow_forward_rounded,
                            color: AgriColors.textWhite,
                            size: 20,
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: AgriDimensions.cardGap),

                  // Quick Action Bar: Sowing, Irrigation, Diagnosis
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(18),
                    decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Field Health Telemetry',
                          style: TextStyle(
                            color: AgriColors.textWhite,
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            _buildTelemetryPill('Soil Nitrogen', 'Optimal', Icons.check_circle_outline_rounded),
                            _buildTelemetryPill('Moisture', 'Low (Irrigate)', Icons.warning_amber_rounded),
                            _buildTelemetryPill('Canopy NDVI', '0.82 High', Icons.eco_outlined),
                          ],
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 20),
                  const DecisionDisclaimerBanner(),
                  const SizedBox(height: 36),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTelemetryPill(String title, String status, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: AgriColors.accentYellow, size: 20),
        const SizedBox(height: 6),
        Text(
          status,
          style: const TextStyle(
            color: AgriColors.textWhite,
            fontWeight: FontWeight.bold,
            fontSize: 11.5,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          title,
          style: const TextStyle(
            color: AgriColors.textSecondary,
            fontSize: 10.5,
          ),
        ),
      ],
    );
  }
}

