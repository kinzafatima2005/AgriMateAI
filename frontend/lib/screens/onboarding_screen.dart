import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'auth/login_screen.dart';

/// SCREEN 1 – ONBOARDING
/// Headline: "Control Every Field with Ease"
/// Short description below in light white text
/// Yellow pill button "Get Started"
/// 3D illustration of a smiling elderly farmer with a straw hat holding wheat stalks at the bottom
class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        bottom: false,
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                physics: const BouncingScrollPhysics(),
                padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 24),
                    // Small branding chip
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                      decoration: BoxDecoration(
                        color: AgriColors.cardSurface,
                        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.spa_rounded, color: AgriColors.accentYellow, size: 14),
                          const SizedBox(width: 6),
                          Text(
                            'AgriMate Pakistan AI',
                            style: textTheme.labelSmall?.copyWith(
                              color: AgriColors.textWhite,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 28),

                    // Hero Headline: 36-44px bold
                    Text(
                      'Control Every\nField with Ease',
                      style: textTheme.displayLarge?.copyWith(
                        fontSize: 40.0,
                        fontWeight: FontWeight.bold,
                        color: AgriColors.textWhite,
                        height: 1.15,
                        letterSpacing: -0.5,
                      ),
                    ),

                    const SizedBox(height: 16),

                    // Short description in light white text (~65% opacity)
                    Text(
                      'Precision leaf disease detection with explainable Grad-CAM heatmaps, certified citation advisory, and direct mandi buyer connections.',
                      style: textTheme.bodyLarge?.copyWith(
                        color: AgriColors.textSecondary,
                        height: 1.5,
                        fontSize: 15.0,
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Yellow Pill Button "Get Started" (Accent Lime-Yellow with Dark Green Text)
                    SizedBox(
                      width: double.infinity,
                      height: 58,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const LoginScreen()),
                          );
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AgriColors.accentYellow,
                          foregroundColor: AgriColors.darkGreenText,
                          elevation: 0,
                          shape: const StadiumBorder(),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              'Get Started',
                              style: textTheme.headlineMedium?.copyWith(
                                fontSize: 17,
                                fontWeight: FontWeight.bold,
                                color: AgriColors.darkGreenText,
                              ),
                            ),
                            const SizedBox(width: 8),
                            const Icon(
                              Icons.arrow_forward_rounded,
                              color: AgriColors.darkGreenText,
                              size: 20,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // 3D illustration of a smiling elderly farmer with a straw hat holding wheat stalks
            SizedBox(
              height: 340,
              width: double.infinity,
              child: Stack(
                alignment: Alignment.bottomCenter,
                children: [
                  // Subtle ambient background gradient
                  Positioned.fill(
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            AgriColors.background.withOpacity(0.0),
                            AgriColors.backgroundDark.withOpacity(0.7),
                          ],
                        ),
                      ),
                    ),
                  ),
                  Image.asset(
                    'assets/farmer_3d.png',
                    height: 320,
                    fit: BoxFit.contain,
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        height: 260,
                        alignment: Alignment.center,
                        child: const Icon(
                          Icons.person_pin_rounded,
                          size: 140,
                          color: AgriColors.cardSurfaceLight,
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

