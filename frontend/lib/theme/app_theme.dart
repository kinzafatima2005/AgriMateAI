import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Central Design System for AgriMate AI
/// Modern Clean White Background Theme with Emerald Green & Golden Accents
class AgriColors {
  AgriColors._();

  // Primary Theme Palette (Clean White + Emerald Green)
  static const Color background = Color(0xFFFFFFFF);           // Clean Pure White (#FFFFFF)
  static const Color backgroundDark = Color(0xFFF8FAFC);       // Soft Slate / Off-white background (#F8FAFC)
  static const Color primaryGreen = Color(0xFF15803D);         // Rich Agricultural Emerald Green (#15803D)
  static const Color primaryGreenLight = Color(0xFF22C55E);    // Bright Leaf Green (#22C55E)
  static const Color accentYellow = Color(0xFFEAB308);         // Vibrant Golden Yellow (#EAB308)
  static const Color darkGreenText = Color(0xFF0F172A);        // Deep Slate Dark Text (#0F172A)

  // Surface & Cards
  static const Color cardSurface = Color(0xFFFFFFFF);          // Pure White Card Surface
  static const Color cardSurfaceLight = Color(0xFFF1F5F9);     // Slate 100 for Inputs/Pills
  static const Color cardSurfaceSubtle = Color(0xFFE2E8F0);    // Slate 200 for subtle borders
  static const Color cardBorder = Color(0xFFE2E8F0);           // Clean crisp card border

  // Text Colors
  static const Color textPrimary = Color(0xFF0F172A);          // Deep Slate primary text
  static const Color textDark = Color(0xFF0F172A);             // High contrast dark text
  static const Color textSecondary = Color(0xFF64748B);        // Slate 500 for secondary descriptions
  static const Color textMuted = Color(0xFF94A3B8);            // Slate 400 for placeholder hints
  static const Color textWhite = Color(0xFFFFFFFF);            // Crisp white for buttons & badges

  // Functional / Feedback Colors
  static const Color error = Color(0xFFEF4444);
  static const Color warning = Color(0xFFF59E0B);
  static const Color success = Color(0xFF10B981);
  static const Color info = Color(0xFF0EA5E9);
  static const Color divider = Color(0xFFE2E8F0);              // Clean light divider
  static const Color iconOutline = Color(0xFF64748B);          // Slate for utility icons
  static const Color iconHighlight = Color(0xFF15803D);        // Green highlight
}

class AgriDimensions {
  AgriDimensions._();

  static const double screenPadding = 22.0;                    // 20-24px screen padding
  static const double cardGap = 14.0;                          // 12-16px gap between cards
  static const double cardRadius = 24.0;                       // 24px soft rounded corners
  static const double pillRadius = 999.0;                      // Fully rounded pill shapes
}

class AppTheme {
  AppTheme._();

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: AgriColors.background,
      primaryColor: AgriColors.primaryGreen,
      
      colorScheme: const ColorScheme(
        brightness: Brightness.light,
        primary: AgriColors.primaryGreen,
        onPrimary: AgriColors.textWhite,
        secondary: AgriColors.accentYellow,
        onSecondary: AgriColors.darkGreenText,
        error: AgriColors.error,
        onError: AgriColors.textWhite,
        surface: AgriColors.cardSurface,
        onSurface: AgriColors.textPrimary,
      ),

      // Rounded Geometric Sans-Serif Typography (Outfit / Poppins style)
      textTheme: TextTheme(
        displayLarge: GoogleFonts.outfit(
          fontSize: 38.0,
          fontWeight: FontWeight.bold,
          color: AgriColors.textPrimary,
          height: 1.15,
          letterSpacing: -0.5,
        ),
        displayMedium: GoogleFonts.outfit(
          fontSize: 30.0,
          fontWeight: FontWeight.bold,
          color: AgriColors.textPrimary,
          height: 1.2,
        ),
        headlineLarge: GoogleFonts.outfit(
          fontSize: 24.0,
          fontWeight: FontWeight.w700,
          color: AgriColors.textPrimary,
        ),
        headlineMedium: GoogleFonts.outfit(
          fontSize: 20.0,
          fontWeight: FontWeight.w600,
          color: AgriColors.textPrimary,
        ),
        titleMedium: GoogleFonts.outfit(
          fontSize: 16.0,
          fontWeight: FontWeight.w600,
          color: AgriColors.textPrimary,
        ),
        bodyLarge: GoogleFonts.outfit(
          fontSize: 15.0,
          fontWeight: FontWeight.normal,
          color: AgriColors.textPrimary,
        ),
        bodyMedium: GoogleFonts.outfit(
          fontSize: 14.0,
          fontWeight: FontWeight.normal,
          color: AgriColors.textSecondary,
        ),
        labelSmall: GoogleFonts.outfit(
          fontSize: 12.0,
          fontWeight: FontWeight.w500,
          color: AgriColors.textSecondary,
        ),
      ),

      // Elevated Buttons (Pill shaped with smooth shadow)
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AgriColors.primaryGreen,
          foregroundColor: AgriColors.textWhite,
          elevation: 0,
          shadowColor: Colors.transparent,
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
          ),
          textStyle: GoogleFonts.outfit(
            fontSize: 15.0,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),

      // Text Fields (Modern light theme with clean border)
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AgriColors.cardSurfaceLight,
        contentPadding: const EdgeInsets.symmetric(horizontal: 18.0, vertical: 16.0),
        hintStyle: GoogleFonts.outfit(color: AgriColors.textMuted, fontSize: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16.0),
          borderSide: const BorderSide(color: AgriColors.cardBorder, width: 1),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16.0),
          borderSide: const BorderSide(color: AgriColors.cardBorder, width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16.0),
          borderSide: const BorderSide(color: AgriColors.primaryGreen, width: 1.8),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16.0),
          borderSide: const BorderSide(color: AgriColors.error, width: 1.2),
        ),
      ),
    );
  }

  // Card Decorations
  static BoxDecoration cardDecoration({bool withBorder = true}) {
    return BoxDecoration(
      color: AgriColors.cardSurface,
      borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
      border: withBorder ? Border.all(color: AgriColors.cardBorder, width: 1) : null,
      boxShadow: const [
        BoxShadow(
          color: Color(0x0A000000), // 4% subtle drop shadow
          blurRadius: 16,
          offset: Offset(0, 4),
        ),
      ],
    );
  }

  // Filter Chips / Pills
  static BoxDecoration pillChipDecoration({required bool isActive}) {
    return BoxDecoration(
      color: isActive ? AgriColors.primaryGreen : AgriColors.cardSurfaceLight,
      borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
      border: Border.all(
        color: isActive ? AgriColors.primaryGreen : AgriColors.cardBorder,
        width: 1,
      ),
    );
  }
}
