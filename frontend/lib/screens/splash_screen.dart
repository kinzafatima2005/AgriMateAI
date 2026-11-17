import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/agri_logo.dart';
import 'onboarding_screen.dart';
import 'dashboard/farmer_home_screen.dart';
import 'dashboard/buyer_home_screen.dart';
import 'dashboard/expert_home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1600),
    );
    _scaleAnimation = Tween<double>(begin: 0.85, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );
    _fadeAnimation = CurvedAnimation(parent: _controller, curve: Curves.easeIn);
    _controller.forward();

    _navigateNext();
  }

  Future<void> _navigateNext() async {
    // 2.5 seconds splash display just like Instagram / Facebook
    await Future.delayed(const Duration(milliseconds: 2500));
    if (!mounted) return;

    final auth = Provider.of<AuthProvider>(context, listen: false);
    if (auth.isAuthenticated && auth.currentUser != null) {
      final role = auth.currentUser!.role;
      Widget target;
      if (role == 'Buyer') {
        target = const BuyerHomeScreen();
      } else if (role == 'Expert/Admin') {
        target = const ExpertHomeScreen();
      } else {
        target = const FarmerHomeScreen();
      }
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => target));
    } else {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const OnboardingScreen()));
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const SizedBox(height: 40),
              // Center Branding (Instagram / Facebook Style)
              ScaleTransition(
                scale: _scaleAnimation,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 104,
                      height: 104,
                      decoration: BoxDecoration(
                        color: AgriColors.cardSurface,
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: AgriColors.primaryGreen.withOpacity(0.12),
                            blurRadius: 28,
                            spreadRadius: 4,
                            offset: const Offset(0, 8),
                          ),
                        ],
                        border: Border.all(color: AgriColors.cardBorder, width: 1.5),
                      ),
                      child: const Center(
                        child: Text(
                          '🌾',
                          style: TextStyle(fontSize: 48),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Text(
                          'AgriMate',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.w900,
                            letterSpacing: -0.5,
                            color: AgriColors.textDark,
                          ),
                        ),
                        SizedBox(width: 4),
                        Text(
                          'AI',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.w900,
                            letterSpacing: -0.5,
                            color: AgriColors.primaryGreen,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      'Smart Farming • پاکستان',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AgriColors.textSecondary,
                        letterSpacing: 0.3,
                      ),
                    ),
                  ],
                ),
              ),

              // Bottom "from Meta" Style Footer
              Padding(
                padding: const EdgeInsets.only(bottom: 24.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'FROM',
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w800,
                        color: AgriColors.textMuted,
                        letterSpacing: 2.0,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          'AgriMate Technologies',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w700,
                            color: AgriColors.textDark,
                            letterSpacing: -0.2,
                          ),
                        ),
                        const SizedBox(width: 4),
                        Icon(
                          Icons.verified,
                          color: AgriColors.primaryGreen,
                          size: 16,
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    SizedBox(
                      width: 50,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(999),
                        child: const LinearProgressIndicator(
                          minHeight: 3,
                          backgroundColor: AgriColors.cardSurfaceLight,
                          valueColor: AlwaysStoppedAnimation<Color>(AgriColors.primaryGreen),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

