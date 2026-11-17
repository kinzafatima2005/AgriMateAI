/// AgriMate AI - Buyer Main Screen (Persistent Bottom Navigation)
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../services/buyer_provider.dart';
import '../../../theme/app_theme.dart';
import '../../../widgets/agri_logo.dart';
import 'tabs/buyer_home_tab.dart';
import 'tabs/buyer_listings_tab.dart';
import 'tabs/buyer_deals_tab.dart';
import 'tabs/buyer_notifications_tab.dart';
import 'tabs/buyer_profile_tab.dart';

class BuyerMainScreen extends StatefulWidget {
  final int initialTabIndex;

  const BuyerMainScreen({
    super.key,
    this.initialTabIndex = 0,
  });

  @override
  State<BuyerMainScreen> createState() => _BuyerMainScreenState();
}

class _BuyerMainScreenState extends State<BuyerMainScreen> {
  late int _currentIndex;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialTabIndex;
  }

  void _onTabTapped(int index) {
    setState(() => _currentIndex = index);
  }

  String _getTabTitle(int index) {
    switch (index) {
      case 0:
        return 'Buyer Hub';
      case 1:
        return 'Browse Listings';
      case 2:
        return 'My Deals Tracker';
      case 3:
        return 'Notifications';
      case 4:
        return 'Trading Profile';
      default:
        return 'Buyer Hub';
    }
  }

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);
    final unreadCount = buyerProv.unreadNotificationsCount;

    final List<Widget> tabs = [
      BuyerHomeTab(
        onNavigateToListings: () => _onTabTapped(1),
        onNavigateToDeals: () => _onTabTapped(2),
      ),
      const BuyerListingsTab(),
      const BuyerDealsTab(),
      const BuyerNotificationsTab(),
      const BuyerProfileTab(),
    ];

    return Scaffold(
      backgroundColor: AgriColors.background,
      appBar: AppBar(
        backgroundColor: AgriColors.background,
        elevation: 0,
        surfaceTintColor: Colors.transparent,
        titleSpacing: AgriDimensions.screenPadding,
        title: Row(
          children: [
            const AgriLogo(size: 32, showText: false),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      'AgriMate AI',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontSize: 16,
                            fontWeight: FontWeight.w800,
                            color: AgriColors.textPrimary,
                          ),
                    ),
                    const SizedBox(width: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1.5),
                      decoration: BoxDecoration(
                        color: AgriColors.primaryGreen.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        'BUYER',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              fontSize: 9.5,
                              fontWeight: FontWeight.w800,
                              color: AgriColors.primaryGreen,
                            ),
                      ),
                    ),
                  ],
                ),
                Text(
                  _getTabTitle(_currentIndex),
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        fontSize: 11.5,
                        color: AgriColors.textSecondary,
                      ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: Stack(
              clipBehavior: Clip.none,
              children: [
                const Icon(Icons.notifications_none_rounded, color: AgriColors.textPrimary),
                if (unreadCount > 0)
                  Positioned(
                    right: -2,
                    top: -2,
                    child: Container(
                      padding: const EdgeInsets.all(4),
                      decoration: const BoxDecoration(
                        color: AgriColors.primaryGreen,
                        shape: BoxShape.circle,
                      ),
                      child: Text(
                        unreadCount > 9 ? '9+' : unreadCount.toString(),
                        style: const TextStyle(
                          color: AgriColors.textWhite,
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            onPressed: () => _onTabTapped(3),
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded, color: AgriColors.iconOutline),
            onPressed: () => buyerProv.refreshAll(),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: tabs,
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AgriColors.background,
          border: Border(top: BorderSide(color: AgriColors.cardBorder, width: 1)),
        ),
        child: NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: _onTabTapped,
          backgroundColor: AgriColors.background,
          indicatorColor: AgriColors.primaryGreen.withOpacity(0.12),
          destinations: [
            const NavigationDestination(
              icon: Icon(Icons.home_outlined, color: AgriColors.iconOutline),
              selectedIcon: Icon(Icons.home_rounded, color: AgriColors.primaryGreen),
              label: 'Home',
            ),
            const NavigationDestination(
              icon: Icon(Icons.inventory_2_outlined, color: AgriColors.iconOutline),
              selectedIcon: Icon(Icons.inventory_2_rounded, color: AgriColors.primaryGreen),
              label: 'Listings',
            ),
            const NavigationDestination(
              icon: Icon(Icons.handshake_outlined, color: AgriColors.iconOutline),
              selectedIcon: Icon(Icons.handshake_rounded, color: AgriColors.primaryGreen),
              label: 'My Deals',
            ),
            NavigationDestination(
              icon: Badge(
                isLabelVisible: unreadCount > 0,
                label: Text(unreadCount.toString()),
                child: const Icon(Icons.notifications_outlined, color: AgriColors.iconOutline),
              ),
              selectedIcon: Badge(
                isLabelVisible: unreadCount > 0,
                label: Text(unreadCount.toString()),
                child: const Icon(Icons.notifications_rounded, color: AgriColors.primaryGreen),
              ),
              label: 'Alerts',
            ),
            const NavigationDestination(
              icon: Icon(Icons.person_outline_rounded, color: AgriColors.iconOutline),
              selectedIcon: Icon(Icons.person_rounded, color: AgriColors.primaryGreen),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}
