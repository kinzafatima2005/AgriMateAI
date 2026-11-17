import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class DecisionDisclaimerBanner extends StatelessWidget {
  final bool compact;

  const DecisionDisclaimerBanner({super.key, this.compact = false});

  @override
  Widget build(BuildContext context) {
    if (compact) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: AgriColors.cardSurfaceSubtle,
          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
          border: Border.all(color: AgriColors.divider),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.shield_outlined, color: AgriColors.accentYellow, size: 14),
            const SizedBox(width: 6),
            Text(
              'Decision-Support Advisory Only • Verify with Extension Officer',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11),
            ),
          ],
        ),
      );
    }

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: AppTheme.cardBoxDecoration(
        color: AgriColors.cardSurface,
        border: Border.all(color: AgriColors.divider),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline_rounded, color: AgriColors.accentYellow, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Agricultural Decision-Support Disclaimer',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AgriColors.accentYellow,
                      ),
                ),
                const SizedBox(height: 4),
                Text(
                  'AgriMate AI provides advisory estimates and diagnostic decision support. Always consult certified local agricultural extension officers before applying chemical pest controls.',
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: AgriColors.textSecondary,
                        height: 1.35,
                      ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

