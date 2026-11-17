/// AgriMate AI - 5-Factor Explainable Match Radar Card
import 'package:flutter/material.dart';
import '../../models/buyer_models.dart';
import '../../theme/app_theme.dart';

class BuyerMatchRadarCard extends StatelessWidget {
  final MatchScoreBreakdown match;

  const BuyerMatchRadarCard({
    super.key,
    required this.match,
  });

  Color _getLevelColor(String level) {
    switch (level.toUpperCase()) {
      case 'EXCELLENT':
        return AgriColors.primaryGreen;
      case 'GOOD':
        return AgriColors.primaryGreenLight;
      case 'FAIR':
        return AgriColors.accentYellow;
      case 'LOW':
        return AgriColors.warning;
      default:
        return AgriColors.error;
    }
  }

  @override
  Widget build(BuildContext context) {
    final levelColor = _getLevelColor(match.matchLevel);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: AppTheme.cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: const BoxDecoration(
                      color: AgriColors.cardSurfaceLight,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.auto_awesome_rounded,
                      size: 20,
                      color: AgriColors.primaryGreen,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    'Match Affinity Score',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                        ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: levelColor.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                  border: Border.all(color: levelColor, width: 1.2),
                ),
                child: Text(
                  '${match.totalScore.toStringAsFixed(0)}% • ${match.matchLevel}',
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: levelColor,
                        fontWeight: FontWeight.w800,
                        fontSize: 13,
                      ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 16),

          // 1. Mandatory Crop Gate
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: match.cropMatch
                  ? AgriColors.primaryGreen.withOpacity(0.08)
                  : AgriColors.error.withOpacity(0.08),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: match.cropMatch ? AgriColors.primaryGreen : AgriColors.error,
                width: 1,
              ),
            ),
            child: Row(
              children: [
                Icon(
                  match.cropMatch ? Icons.check_circle_rounded : Icons.cancel_rounded,
                  size: 20,
                  color: match.cropMatch ? AgriColors.primaryGreen : AgriColors.error,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    match.cropMatch
                        ? 'Crop Match Passed: Commodity matches buyer preferred crops (Mandatory Gate)'
                        : 'Crop Mismatch: Crop does not match preferred commodity list',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: match.cropMatch ? AgriColors.textPrimary : AgriColors.error,
                          fontWeight: FontWeight.w600,
                          fontSize: 12.5,
                        ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // 4 Itemized 25% Factors
          _buildScoreBar(
            context,
            label: 'Quantity Fit (25%)',
            score: match.quantityScore,
            maxScore: 25.0,
            icon: Icons.inventory_2_outlined,
          ),
          const SizedBox(height: 10),

          _buildScoreBar(
            context,
            label: 'Distance Fit (25%) • ${match.distanceKm.toStringAsFixed(0)} km',
            score: match.distanceScore,
            maxScore: 25.0,
            icon: Icons.near_me_outlined,
          ),
          const SizedBox(height: 10),

          _buildScoreBar(
            context,
            label: 'Grade Fit (25%)',
            score: match.gradeScore,
            maxScore: 25.0,
            icon: Icons.workspace_premium_outlined,
          ),
          const SizedBox(height: 10),

          _buildScoreBar(
            context,
            label: 'Price Fit (25%)',
            score: match.priceScore,
            maxScore: 25.0,
            icon: Icons.sell_outlined,
          ),

          const SizedBox(height: 14),

          // Explanation Note
          if (match.explanation.isNotEmpty)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AgriColors.cardSurfaceLight,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                match.explanation,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      fontSize: 12.5,
                      color: AgriColors.textSecondary,
                    ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildScoreBar(
    BuildContext context, {
    required String label,
    required double score,
    required double maxScore,
    required IconData icon,
  }) {
    final pct = (score / maxScore).clamp(0.0, 1.0);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Icon(icon, size: 16, color: AgriColors.iconOutline),
                const SizedBox(width: 8),
                Text(
                  label,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AgriColors.textPrimary,
                      ),
                ),
              ],
            ),
            Text(
              '${score.toStringAsFixed(1)} / 25',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AgriColors.textPrimary,
                  ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
          child: LinearProgressIndicator(
            value: pct,
            backgroundColor: AgriColors.cardSurfaceLight,
            valueColor: AlwaysStoppedAnimation<Color>(
              pct >= 0.8
                  ? AgriColors.primaryGreen
                  : (pct >= 0.5 ? AgriColors.accentYellow : AgriColors.warning),
            ),
            minHeight: 7,
          ),
        ),
      ],
    );
  }
}
