/// AgriMate AI - Buyer Home Tab
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../services/buyer_provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../widgets/buyer/state_views.dart';

class BuyerHomeTab extends StatelessWidget {
  final VoidCallback onNavigateToListings;
  final VoidCallback onNavigateToDeals;

  const BuyerHomeTab({
    super.key,
    required this.onNavigateToListings,
    required this.onNavigateToDeals,
  });

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);

    if (buyerProv.isLoadingSummary && buyerProv.summary == null) {
      return const BuyerLoadingView(message: 'Loading procurement hub...');
    }

    if (buyerProv.summaryError != null && buyerProv.summary == null) {
      return BuyerErrorView(
        error: buyerProv.summaryError!,
        onRetry: () => buyerProv.fetchSummary(),
      );
    }

    final summary = buyerProv.summary;
    final buyerName = summary?.buyerName ?? 'Verified Buyer';
    final buyerLocation = summary?.buyerLocation ?? 'Mandi Hub';

    return RefreshIndicator(
      color: AgriColors.primaryGreen,
      onRefresh: () => buyerProv.refreshAll(),
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(parent: BouncingScrollPhysics()),
        padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 14),

            // Welcome Header Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: AppTheme.cardDecoration(),
              child: Row(
                children: [
                  Container(
                    width: 52,
                    height: 52,
                    decoration: const BoxDecoration(
                      color: AgriColors.cardSurfaceLight,
                      shape: BoxShape.circle,
                    ),
                    alignment: Alignment.center,
                    child: const Icon(
                      Icons.storefront_rounded,
                      color: AgriColors.primaryGreen,
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Welcome back,',
                          style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                color: AgriColors.textSecondary,
                                fontSize: 12,
                              ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          buyerName,
                          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                                fontSize: 18,
                                fontWeight: FontWeight.w700,
                              ),
                        ),
                        const SizedBox(height: 2),
                        Row(
                          children: [
                            const Icon(
                              Icons.location_on_outlined,
                              size: 14,
                              color: AgriColors.primaryGreen,
                            ),
                            const SizedBox(width: 4),
                            Expanded(
                              child: Text(
                                buyerLocation,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                      fontSize: 12,
                                      color: AgriColors.textSecondary,
                                    ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // 3 KPI Summary Cards
            Row(
              children: [
                Expanded(
                  child: _buildKpiCard(
                    context,
                    title: 'Active Listings',
                    value: (summary?.activeListingsCount ?? 0).toString(),
                    icon: Icons.inventory_2_outlined,
                    color: AgriColors.primaryGreen,
                    onTap: onNavigateToListings,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildKpiCard(
                    context,
                    title: 'My Interests',
                    value: (summary?.myInterestsCount ?? 0).toString(),
                    icon: Icons.favorite_border_rounded,
                    color: AgriColors.accentYellow,
                    onTap: onNavigateToDeals,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildKpiCard(
                    context,
                    title: 'Deals Active',
                    value: (summary?.dealsInProgressCount ?? 0).toString(),
                    icon: Icons.handshake_outlined,
                    color: AgriColors.info,
                    onTap: onNavigateToDeals,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 22),

            // Mandi Price Ticker Section
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Dated Mandi Price Ticker',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontSize: 17,
                        fontWeight: FontWeight.w700,
                      ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    'Read-Only',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          fontSize: 11,
                          color: AgriColors.textSecondary,
                        ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),

            // Horizontal Ticker List
            if (summary != null && summary.priceTicker.isNotEmpty)
              SizedBox(
                height: 110,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  physics: const BouncingScrollPhysics(),
                  itemCount: summary.priceTicker.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 12),
                  itemBuilder: (context, index) {
                    final item = summary.priceTicker[index];
                    final isUp = item.trend == 'up';
                    final trendColor = isUp ? AgriColors.primaryGreen : (item.trend == 'down' ? AgriColors.error : AgriColors.textSecondary);

                    return Container(
                      width: 175,
                      padding: const EdgeInsets.all(14),
                      decoration: AppTheme.cardDecoration(),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                item.crop,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w700,
                                  fontSize: 14,
                                  color: AgriColors.textPrimary,
                                ),
                              ),
                              Icon(
                                isUp ? Icons.trending_up_rounded : (item.trend == 'down' ? Icons.trending_down_rounded : Icons.trending_flat_rounded),
                                size: 18,
                                color: trendColor,
                              ),
                            ],
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'PKR ${item.rate.toStringAsFixed(0)}',
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.w800,
                                  color: trendColor,
                                ),
                              ),
                              Text(
                                '${item.mandi} • ${item.date}',
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                  fontSize: 10.5,
                                  color: AgriColors.textSecondary,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    );
                  },
                ),
              )
            else
              Container(
                padding: const EdgeInsets.all(16),
                decoration: AppTheme.cardDecoration(),
                child: const Text('No recent mandi prices recorded.'),
              ),

            const SizedBox(height: 22),

            // Recent Notifications Preview
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Recent Updates & Matches',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontSize: 17,
                        fontWeight: FontWeight.w700,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 10),

            if (summary != null && summary.recentNotifications.isNotEmpty)
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: summary.recentNotifications.length.clamp(0, 3),
                separatorBuilder: (_, __) => const SizedBox(height: 10),
                itemBuilder: (context, index) {
                  final notif = summary.recentNotifications[index];
                  final isMatch = notif.type == 'BUYER_MATCH';

                  return Container(
                    padding: const EdgeInsets.all(14),
                    decoration: AppTheme.cardDecoration(),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: isMatch ? AgriColors.primaryGreen.withOpacity(0.1) : AgriColors.accentYellow.withOpacity(0.1),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(
                            isMatch ? Icons.auto_awesome_rounded : Icons.notifications_none_rounded,
                            size: 18,
                            color: isMatch ? AgriColors.primaryGreen : AgriColors.accentYellow,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                notif.title,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w700,
                                  fontSize: 13.5,
                                  color: AgriColors.textPrimary,
                                ),
                              ),
                              const SizedBox(height: 3),
                              Text(
                                notif.body,
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: AgriColors.textSecondary,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                },
              )
            else
              Container(
                padding: const EdgeInsets.all(16),
                decoration: AppTheme.cardDecoration(),
                child: const Text('No recent notifications.'),
              ),

            const SizedBox(height: 20),

            // Prototype Disclaimer Notice
            const DecisionDisclaimerBanner(),

            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildKpiCard(
    BuildContext context, {
    required String title,
    required String value,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Container(
      decoration: AppTheme.cardDecoration(),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
        child: InkWell(
          borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(icon, size: 20, color: color),
                const SizedBox(height: 10),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w800,
                    color: AgriColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  title,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        fontSize: 11,
                        color: AgriColors.textSecondary,
                      ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
