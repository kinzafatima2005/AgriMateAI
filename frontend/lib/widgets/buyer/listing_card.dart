/// AgriMate AI - Buyer Listing Card
import 'package:flutter/material.dart';
import '../../models/buyer_models.dart';
import '../../theme/app_theme.dart';

class ListingCard extends StatelessWidget {
  final ListingItem listing;
  final VoidCallback onTap;

  const ListingCard({
    super.key,
    required this.listing,
    required this.onTap,
  });

  String _getCropEmoji(String crop) {
    final lower = crop.toLowerCase();
    if (lower.contains('potato')) return '🥔';
    if (lower.contains('tomato')) return '🍅';
    if (lower.contains('wheat')) return '🌾';
    if (lower.contains('cotton')) return '☁️';
    if (lower.contains('rice')) return '🍚';
    return '🌱';
  }

  Color _getMatchColor(double? score) {
    if (score == null) return AgriColors.textSecondary;
    if (score >= 80) return AgriColors.primaryGreen;
    if (score >= 60) return AgriColors.accentYellow;
    return AgriColors.warning;
  }

  @override
  Widget build(BuildContext context) {
    final matchScore = listing.totalMatchScore;
    final matchColor = _getMatchColor(matchScore);

    return Container(
      margin: const EdgeInsets.only(bottom: AgriDimensions.cardGap),
      decoration: AppTheme.cardDecoration(),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
        child: InkWell(
          borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Top row: Crop icon + Name & Grade + Match badge
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      width: 44,
                      height: 44,
                      decoration: const BoxDecoration(
                        color: AgriColors.cardSurfaceLight,
                        shape: BoxShape.circle,
                      ),
                      alignment: Alignment.center,
                      child: Text(
                        _getCropEmoji(listing.crop),
                        style: const TextStyle(fontSize: 22),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(
                                listing.crop,
                                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                                      fontSize: 17,
                                      fontWeight: FontWeight.w700,
                                    ),
                              ),
                              const SizedBox(width: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: AgriColors.cardSurfaceLight,
                                  borderRadius: BorderRadius.circular(6),
                                  border: Border.all(color: AgriColors.cardBorder, width: 1),
                                ),
                                child: Text(
                                  'Grade ${listing.grade}',
                                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                        fontSize: 11,
                                        fontWeight: FontWeight.w700,
                                        color: AgriColors.primaryGreen,
                                      ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 2),
                          Text(
                            listing.farmerName,
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  fontSize: 13,
                                  color: AgriColors.textSecondary,
                                ),
                          ),
                        ],
                      ),
                    ),
                    if (matchScore != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: matchColor.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                          border: Border.all(color: matchColor, width: 1),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.bolt_rounded, size: 14, color: matchColor),
                            const SizedBox(width: 2),
                            Text(
                              '${matchScore.toStringAsFixed(0)}% Match',
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    fontWeight: FontWeight.w700,
                                    color: matchColor,
                                    fontSize: 11.5,
                                  ),
                            ),
                          ],
                        ),
                      ),
                  ],
                ),

                const SizedBox(height: 14),

                // Metrics Row: Quantity, Asking Price, Distance
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildMetric(
                        context,
                        label: 'Available',
                        value: '${listing.quantity.toStringAsFixed(0)} kg',
                      ),
                      Container(width: 1, height: 28, color: AgriColors.divider),
                      _buildMetric(
                        context,
                        label: 'Asking Price',
                        value: 'PKR ${listing.askingPrice.toStringAsFixed(0)}',
                        subtext: '/ 40kg',
                      ),
                      Container(width: 1, height: 28, color: AgriColors.divider),
                      _buildMetric(
                        context,
                        label: 'Distance',
                        value: listing.distanceKm != null
                            ? '${listing.distanceKm!.toStringAsFixed(0)} km'
                            : '-- km',
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                // Footer Row: Location & Status / Already Interested Pill
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Row(
                        children: [
                          const Icon(
                            Icons.location_on_outlined,
                            size: 16,
                            color: AgriColors.iconOutline,
                          ),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              listing.location,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    fontSize: 12.5,
                                    color: AgriColors.textSecondary,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    if (listing.alreadyInterested)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: AgriColors.primaryGreen.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                        ),
                        child: Text(
                          'Interest Sent',
                          style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                color: AgriColors.primaryGreen,
                                fontWeight: FontWeight.w700,
                              ),
                        ),
                      )
                    else
                      const Icon(
                        Icons.arrow_forward_ios_rounded,
                        size: 14,
                        color: AgriColors.iconOutline,
                      ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMetric(
    BuildContext context, {
    required String label,
    required String value,
    String? subtext,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.labelSmall?.copyWith(
                fontSize: 11,
                color: AgriColors.textSecondary,
              ),
        ),
        const SizedBox(height: 2),
        RichText(
          text: TextSpan(
            text: value,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w700,
              color: AgriColors.textPrimary,
              fontFamily: Theme.of(context).textTheme.bodyLarge?.fontFamily,
            ),
            children: subtext != null
                ? [
                    TextSpan(
                      text: ' $subtext',
                      style: const TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w500,
                        color: AgriColors.textSecondary,
                      ),
                    )
                  ]
                : null,
          ),
        ),
      ],
    );
  }
}
