/// AgriMate AI - Deal Status Audit Timeline Widget
import 'package:flutter/material.dart';
import '../../models/buyer_models.dart';
import '../../theme/app_theme.dart';

class DealTimelineWidget extends StatelessWidget {
  final List<DealHistoryItem> history;

  const DealTimelineWidget({
    super.key,
    required this.history,
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

  String _formatStatusTitle(String status) {
    switch (status.toLowerCase()) {
      case 'interested':
        return 'Interest Submitted';
      case 'accepted':
        return 'Offer Accepted by Farmer';
      case 'in_progress':
        return 'Deal In-Progress (Logistics & Inspection)';
      case 'completed':
        return 'Deal Completed & Verified';
      case 'rejected':
        return 'Offer Declined';
      default:
        return status;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (history.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: AppTheme.cardDecoration(),
        child: Text(
          'No history logged yet.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
      );
    }

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: AppTheme.cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.timeline_rounded,
                size: 20,
                color: AgriColors.primaryGreen,
              ),
              const SizedBox(width: 8),
              Text(
                'Deal Lifecycle Audit Timeline',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: history.length,
            itemBuilder: (context, index) {
              final item = history[index];
              final isLast = index == history.length - 1;
              final color = _getStatusColor(item.status);

              return IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Dot and vertical connecting line
                    Column(
                      children: [
                        Container(
                          width: 14,
                          height: 14,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                            border: Border.all(
                              color: AgriColors.cardSurface,
                              width: 2,
                            ),
                          ),
                        ),
                        if (!isLast)
                          Expanded(
                            child: Container(
                              width: 2,
                              color: AgriColors.divider,
                              margin: const EdgeInsets.symmetric(vertical: 4),
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(width: 14),
                    // Content
                    Expanded(
                      child: Padding(
                        padding: EdgeInsets.only(bottom: isLast ? 0 : 20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _formatStatusTitle(item.status),
                              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                                    fontWeight: FontWeight.w700,
                                    fontSize: 14,
                                    color: AgriColors.textPrimary,
                                  ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              '${item.changedAt.day} ${_monthName(item.changedAt.month)} ${item.changedAt.year} • ${item.changedAt.hour.toString().padLeft(2, '0')}:${item.changedAt.minute.toString().padLeft(2, '0')}',
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    fontSize: 11.5,
                                    color: AgriColors.textSecondary,
                                  ),
                            ),
                            if (item.notes != null && item.notes!.isNotEmpty) ...[
                              const SizedBox(height: 6),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                decoration: BoxDecoration(
                                  color: AgriColors.cardSurfaceLight,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  item.notes!,
                                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                        fontSize: 12.5,
                                        color: AgriColors.textPrimary,
                                      ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  String _monthName(int month) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months[(month - 1).clamp(0, 11)];
  }
}
