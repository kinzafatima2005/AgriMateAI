/// AgriMate AI - Buyer Deals Tracker Tab
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../services/buyer_provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../widgets/buyer/deal_card.dart';
import '../../../../widgets/buyer/state_views.dart';
import '../deal_detail_screen.dart';

class BuyerDealsTab extends StatefulWidget {
  const BuyerDealsTab({super.key});

  @override
  State<BuyerDealsTab> createState() => _BuyerDealsTabState();
}

class _BuyerDealsTabState extends State<BuyerDealsTab> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final List<Map<String, String>> _statusTabs = [
    {'label': 'All', 'status': 'all'},
    {'label': 'Interested', 'status': 'interested'},
    {'label': 'Accepted', 'status': 'accepted'},
    {'label': 'In Progress', 'status': 'in_progress'},
    {'label': 'Completed', 'status': 'completed'},
    {'label': 'Rejected', 'status': 'rejected'},
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: _statusTabs.length, vsync: this);
    _tabController.addListener(() {
      if (!_tabController.indexIsChanging) {
        final status = _statusTabs[_tabController.index]['status']!;
        Provider.of<BuyerProvider>(context, listen: false).fetchDeals(status: status);
      }
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // Disclaimer Banner at top of deals screen (Mandatory project rule)
            const Padding(
              padding: EdgeInsets.symmetric(
                horizontal: AgriDimensions.screenPadding,
                vertical: 10.0,
              ),
              child: DecisionDisclaimerBanner(),
            ),

            // Tab Bar
            Container(
              decoration: const BoxDecoration(
                border: Border(bottom: BorderSide(color: AgriColors.cardBorder, width: 1)),
              ),
              child: TabBar(
                controller: _tabController,
                isScrollable: true,
                labelColor: AgriColors.primaryGreen,
                unselectedLabelColor: AgriColors.textSecondary,
                indicatorColor: AgriColors.primaryGreen,
                indicatorWeight: 3,
                labelStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13.5),
                unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.w500, fontSize: 13.5),
                tabs: _statusTabs.map((t) => Tab(text: t['label'])).toList(),
              ),
            ),

            // Tab View / Content
            Expanded(
              child: RefreshIndicator(
                color: AgriColors.primaryGreen,
                onRefresh: () => buyerProv.fetchDeals(),
                child: _buildDealsContent(buyerProv),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDealsContent(BuyerProvider provider) {
    if (provider.isLoadingDeals && provider.deals.isEmpty) {
      return const BuyerLoadingView(message: 'Loading trade deals...');
    }

    if (provider.dealsError != null && provider.deals.isEmpty) {
      return BuyerErrorView(
        error: provider.dealsError!,
        onRetry: () => provider.fetchDeals(),
      );
    }

    if (provider.deals.isEmpty) {
      return BuyerEmptyView(
        icon: Icons.handshake_outlined,
        title: 'No Deals in this Status',
        description: 'You have no deals under "${_statusTabs[_tabController.index]['label']}". Browse available produce listings to express purchase interest.',
      );
    }

    return ListView.builder(
      physics: const AlwaysScrollableScrollPhysics(parent: BouncingScrollPhysics()),
      padding: const EdgeInsets.symmetric(
        horizontal: AgriDimensions.screenPadding,
        vertical: 14,
      ),
      itemCount: provider.deals.length,
      itemBuilder: (context, index) {
        final deal = provider.deals[index];
        return DealCard(
          deal: deal,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => DealDetailScreen(dealId: deal.id),
              ),
            );
          },
        );
      },
    );
  }
}
