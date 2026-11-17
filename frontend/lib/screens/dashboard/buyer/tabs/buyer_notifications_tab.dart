/// AgriMate AI - Buyer Notifications Tab
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../services/buyer_provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../widgets/buyer/state_views.dart';

class BuyerNotificationsTab extends StatelessWidget {
  const BuyerNotificationsTab({super.key});

  Color _getTypeColor(String type) {
    switch (type.toUpperCase()) {
      case 'BUYER_MATCH':
        return AgriColors.primaryGreen;
      case 'DEAL_STATUS':
        return AgriColors.info;
      default:
        return AgriColors.accentYellow;
    }
  }

  IconData _getTypeIcon(String type) {
    switch (type.toUpperCase()) {
      case 'BUYER_MATCH':
        return Icons.auto_awesome_rounded;
      case 'DEAL_STATUS':
        return Icons.handshake_outlined;
      default:
        return Icons.notifications_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);

    if (buyerProv.isLoadingNotifications && buyerProv.notifications.isEmpty) {
      return const BuyerLoadingView(message: 'Loading notification feed...');
    }

    if (buyerProv.notificationsError != null && buyerProv.notifications.isEmpty) {
      return BuyerErrorView(
        error: buyerProv.notificationsError!,
        onRetry: () => buyerProv.fetchNotifications(),
      );
    }

    if (buyerProv.notifications.isEmpty) {
      return const BuyerEmptyView(
        icon: Icons.notifications_none_rounded,
        title: 'No Notifications Yet',
        description: 'You will receive in-app alerts and push notifications when new matching crop listings are posted or deal statuses change.',
      );
    }

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: RefreshIndicator(
          color: AgriColors.primaryGreen,
          onRefresh: () => buyerProv.fetchNotifications(),
          child: ListView.separated(
            physics: const AlwaysScrollableScrollPhysics(parent: BouncingScrollPhysics()),
            padding: const EdgeInsets.symmetric(
              horizontal: AgriDimensions.screenPadding,
              vertical: 14,
            ),
            itemCount: buyerProv.notifications.length,
            separatorBuilder: (_, __) => const SizedBox(height: 10),
            itemBuilder: (context, index) {
              final n = buyerProv.notifications[index];
              final typeColor = _getTypeColor(n.type);
              final typeIcon = _getTypeIcon(n.type);

              return Container(
                decoration: AppTheme.cardDecoration(),
                child: Material(
                  color: Colors.transparent,
                  borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
                    onTap: () {
                      if (!n.isRead) {
                        buyerProv.markNotificationAsRead(n.id);
                      }
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: typeColor.withOpacity(0.12),
                              shape: BoxShape.circle,
                            ),
                            child: Icon(typeIcon, size: 20, color: typeColor),
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Expanded(
                                      child: Text(
                                        n.title,
                                        style: TextStyle(
                                          fontWeight: n.isRead ? FontWeight.w600 : FontWeight.w800,
                                          fontSize: 14,
                                          color: AgriColors.textPrimary,
                                        ),
                                      ),
                                    ),
                                    if (!n.isRead)
                                      Container(
                                        width: 8,
                                        height: 8,
                                        margin: const EdgeInsets.only(left: 6),
                                        decoration: const BoxDecoration(
                                          color: AgriColors.primaryGreen,
                                          shape: BoxShape.circle,
                                        ),
                                      ),
                                  ],
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  n.body,
                                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                        fontSize: 12.5,
                                        color: AgriColors.textSecondary,
                                      ),
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  '${n.createdAt.day} ${_monthName(n.createdAt.month)} • ${n.createdAt.hour.toString().padLeft(2, '0')}:${n.createdAt.minute.toString().padLeft(2, '0')}',
                                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                        fontSize: 11,
                                        color: AgriColors.textMuted,
                                      ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }

  static String _monthName(int month) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months[(month - 1).clamp(0, 11)];
  }
}
