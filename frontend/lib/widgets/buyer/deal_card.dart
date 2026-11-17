/// AgriMate AI - Buyer Deal Card
import 'package:flutter/material.dart';
import '../../models/buyer_models.dart';
import '../../theme/app_theme.dart';

class DealCard extends StatelessWidget {
  final BuyerDeal deal;
  final VoidCallback onTap;

  const DealCard({
    super.key,
    required this.deal,
    required this.onTap,
  });

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'accepted':
      case 'completed':
        return AgriColors.primaryGreen;
      case 'in_progress':
        return AgriColors.info;
      case 'interested':
        return AgriColors.accentYellow;
      case 'rejected':
        return AgriColors.error;
      default:
        return AgriColors.textSecondary;
    }
  }

  String _formatStatus(String status) {
    switch (status.toLowerCase()) {
      case 'in_progress':
        return 'In Progress';
      case 'interested':
        return 'Interested';
      case 'accepted':
        return 'Accepted';
      case 'completed':
        return 'Completed';
      case 'rejected':
        return 'Rejected';
      default:
        return status;
    }
  }

  @override
  Widget build(BuildContext context) {
    final statusColor = _getStatusColor(deal.status);

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
                // Top row: Crop + Grade & Status Badge
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Text(
                          deal.crop,
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
                            'Grade ${deal.grade}',
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w700,
                                  color: AgriColors.primaryGreen,
                                ),
                          ),
                        ),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                        border: Border.all(color: statusColor, width: 1),
                      ),
                      child: Text(
                        _formatStatus(deal.status),
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: statusColor,
                              fontWeight: FontWeight.w800,
                              fontSize: 11.5,
                            ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 12),

                // Metrics row: Offered Price vs Asking Price, Quantity Wanted
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Column(
                        children: [
                          Text(
                            'Quantity Wanted',
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                  fontSize: 11,
                                  color: AgriColors.textSecondary,
                                ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            '${deal.quantityWanted.toStringAsFixed(0)} kg',
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w700,
                              color: AgriColors.textPrimary,
                            ),
                          ),
                        ],
                      ),
                      Container(width: 1, height: 28, color: AgriColors.divider),
                      Column(
                        children: [
                          Text(
                            'Offered Price',
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                  fontSize: 11,
                                  color: AgriColors.textSecondary,
                                ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            'PKR ${deal.offeredPrice.toStringAsFixed(0)}',
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w700,
                              color: AgriColors.primaryGreen,
                            ),
                          ),
                        ],
                      ),
                      Container(width: 1, height: 28, color: AgriColors.divider),
                      Column(
                        children: [
                          Text(
                            'Asking Price',
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                  fontSize: 11,
                                  color: AgriColors.textSecondary,
                                ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            'PKR ${deal.askingPrice.toStringAsFixed(0)}',
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w700,
                              color: AgriColors.textSecondary,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                // Farmer info and last updated date
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        const Icon(
                          Icons.person_outline_rounded,
                          size: 16,
                          color: AgriColors.iconOutline,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          '${deal.farmerName} • ${deal.farmerLocation}',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                fontSize: 12.5,
                                color: AgriColors.textSecondary,
                              ),
                        ),
                      ],
                    ),
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
}
