import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class AgriLogo extends StatelessWidget {
  final double size;
  final bool showText;
  final bool isLight;

  const AgriLogo({
    super.key,
    this.size = 80.0,
    this.showText = true,
    this.isLight = true,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: AgriColors.accentYellow.withOpacity(0.15),
                blurRadius: 20,
                spreadRadius: 4,
              ),
            ],
          ),
          child: ClipOval(
            child: Image.asset(
              'assets/logo.png',
              width: size,
              height: size,
              fit: BoxFit.contain,
              errorBuilder: (context, error, stackTrace) {
                // Fallback clean geometric vector logo: Sprout blooming from harvest basket/crate
                return Container(
                  width: size,
                  height: size,
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    shape: BoxShape.circle,
                    border: Border.all(color: AgriColors.accentYellow, width: 2),
                  ),
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      // Warm basket / crate base
                      Positioned(
                        bottom: size * 0.16,
                        child: Icon(
                          Icons.shopping_basket_rounded,
                          color: AgriColors.accentYellow,
                          size: size * 0.44,
                        ),
                      ),
                      // Fresh emerald green sprout growing upward
                      Positioned(
                        top: size * 0.14,
                        child: Icon(
                          Icons.eco_rounded,
                          color: AgriColors.primaryGreen,
                          size: size * 0.44,
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ),
        if (showText) ...[
          const SizedBox(height: 12),
          Text(
            'AgriMate',
            style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                  letterSpacing: -0.5,
                  color: isLight ? AgriColors.textWhite : AgriColors.darkGreenText,
                ),
          ),
          Text(
            'PAKISTAN SMART FARMING',
            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                  color: isLight ? AgriColors.accentYellow : AgriColors.darkGreenText,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 2.0,
                ),
          ),
        ],
      ],
    );
  }
}

