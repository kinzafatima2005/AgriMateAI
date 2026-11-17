import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/auth_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/decision_disclaimer_banner.dart';

class ExpertHomeScreen extends StatelessWidget {
  const ExpertHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final user = auth.currentUser;
    final userName = user != null ? user.name : 'Dr. Farooq Shah';

    return Scaffold(
      backgroundColor: AgriColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text('Agronomy Expert Console', style: Theme.of(context).textTheme.headlineMedium),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout_rounded, color: AgriColors.textWhite),
            onPressed: () => auth.logout(),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 10),
              // Expert Badge
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                child: Row(
                  children: [
                    Container(
                      width: 50,
                      height: 50,
                      decoration: const BoxDecoration(
                        color: AgriColors.accentYellow,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.verified_user_rounded, color: AgriColors.darkGreenText, size: 28),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            userName,
                            style: const TextStyle(
                              color: AgriColors.textWhite,
                              fontWeight: FontWeight.bold,
                              fontSize: 17,
                            ),
                          ),
                          const SizedBox(height: 3),
                          const Text(
                            'PARC / Agri Extension Verified Specialist',
                            style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 18),

              Text(
                'Diagnostic Reviews Queue (Pending Verification)',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontSize: 17),
              ),
              const SizedBox(height: 12),

              _buildReviewCard(
                disease: 'Cotton Leaf Curl Virus (CLCuV)',
                farmer: 'Muhammad Tariq (Multan)',
                confidence: '94.2% AI Confidence',
                urgency: 'HIGH',
              ),

              const SizedBox(height: 12),

              _buildReviewCard(
                disease: 'Wheat Yellow Rust (Puccinia striiformis)',
                farmer: 'Chaudhry Rasheed (Sahiwal)',
                confidence: '91.8% AI Confidence',
                urgency: 'CRITICAL',
              ),

              const SizedBox(height: 24),
              const DecisionDisclaimerBanner(),
              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildReviewCard({
    required String disease,
    required String farmer,
    required String confidence,
    required String urgency,
  }) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  disease,
                  style: const TextStyle(
                    color: AgriColors.textWhite,
                    fontWeight: FontWeight.bold,
                    fontSize: 15,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: urgency == 'CRITICAL' ? AgriColors.error.withOpacity(0.3) : AgriColors.warning.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                ),
                child: Text(
                  urgency,
                  style: TextStyle(
                    color: urgency == 'CRITICAL' ? AgriColors.error : AgriColors.accentYellow,
                    fontWeight: FontWeight.bold,
                    fontSize: 11,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text('Reported by: $farmer', style: const TextStyle(color: AgriColors.textSecondary, fontSize: 13)),
          const SizedBox(height: 3),
          Text(confidence, style: const TextStyle(color: AgriColors.accentYellow, fontSize: 12)),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AgriColors.accentYellow,
                    foregroundColor: AgriColors.darkGreenText,
                    padding: const EdgeInsets.symmetric(vertical: 10),
                  ),
                  child: const Text('Confirm Advisory', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: OutlinedButton(
                  onPressed: () {},
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AgriColors.textWhite,
                    side: const BorderSide(color: AgriColors.divider),
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    shape: const StadiumBorder(),
                  ),
                  child: const Text('View Grad-CAM', style: TextStyle(fontSize: 12)),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

