/// AgriMate AI - Buyer Browse Listings Tab
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../services/buyer_provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../widgets/buyer/filter_bottom_sheet.dart';
import '../../../../widgets/buyer/listing_card.dart';
import '../../../../widgets/buyer/state_views.dart';
import '../listing_detail_screen.dart';

class BuyerListingsTab extends StatefulWidget {
  const BuyerListingsTab({super.key});

  @override
  State<BuyerListingsTab> createState() => _BuyerListingsTabState();
}

class _BuyerListingsTabState extends State<BuyerListingsTab> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _openFilterBottomSheet(BuyerProvider provider) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => FilterBottomSheet(
        currentCrop: provider.selectedCrop,
        currentGrade: provider.selectedGrade,
        currentMinQty: provider.minQty,
        currentMaxDistanceKm: provider.maxDistanceKm,
        currentSort: provider.selectedSort,
        onApply: ({
          required String crop,
          required String grade,
          required double? minQty,
          required double? maxDistanceKm,
          required String sort,
        }) {
          provider.setFilters(
            crop: crop,
            grade: grade,
            minQty: minQty,
            maxDistanceKm: maxDistanceKm,
            sort: sort,
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final buyerProv = Provider.of<BuyerProvider>(context);

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // Search & Filter Header
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: AgriDimensions.screenPadding,
                vertical: 12.0,
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _searchController,
                      onChanged: (val) => buyerProv.setSearchQuery(val),
                      decoration: InputDecoration(
                        hintText: 'Search crop or location...',
                        prefixIcon: const Icon(Icons.search_rounded, color: AgriColors.iconOutline),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(Icons.clear_rounded, size: 18),
                                onPressed: () {
                                  _searchController.clear();
                                  buyerProv.setSearchQuery('');
                                },
                              )
                            : null,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Container(
                    decoration: BoxDecoration(
                      color: AgriColors.cardSurfaceLight,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AgriColors.cardBorder, width: 1),
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.tune_rounded, color: AgriColors.primaryGreen),
                      onPressed: () => _openFilterBottomSheet(buyerProv),
                    ),
                  ),
                ],
              ),
            ),

            // Active Filters Chip Row
            if (buyerProv.selectedCrop != 'All' ||
                buyerProv.selectedGrade != 'All' ||
                buyerProv.minQty != null ||
                buyerProv.maxDistanceKm != null)
              Container(
                height: 38,
                padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
                margin: const EdgeInsets.only(bottom: 8),
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  children: [
                    if (buyerProv.selectedCrop != 'All')
                      _buildFilterChip('Crop: ${buyerProv.selectedCrop}', () {
                        buyerProv.setFilters(crop: 'All');
                      }),
                    if (buyerProv.selectedGrade != 'All')
                      _buildFilterChip('Grade ${buyerProv.selectedGrade}', () {
                        buyerProv.setFilters(grade: 'All');
                      }),
                    if (buyerProv.minQty != null)
                      _buildFilterChip('≥ ${buyerProv.minQty!.toStringAsFixed(0)} kg', () {
                        buyerProv.setFilters(minQty: 0.0);
                      }),
                    if (buyerProv.maxDistanceKm != null)
                      _buildFilterChip('≤ ${buyerProv.maxDistanceKm!.toStringAsFixed(0)} km', () {
                        buyerProv.setFilters(maxDistanceKm: null);
                      }),
                  ],
                ),
              ),

            // Listings List or States
            Expanded(
              child: RefreshIndicator(
                color: AgriColors.primaryGreen,
                onRefresh: () => buyerProv.fetchListings(),
                child: _buildListContent(buyerProv),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterChip(String label, VoidCallback onRemove) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: AgriColors.primaryGreen.withOpacity(0.08),
        borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
        border: Border.all(color: AgriColors.primaryGreen, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: AgriColors.primaryGreen,
            ),
          ),
          const SizedBox(width: 4),
          InkWell(
            onTap: onRemove,
            child: const Icon(Icons.close_rounded, size: 14, color: AgriColors.primaryGreen),
          ),
        ],
      ),
    );
  }

  Widget _buildListContent(BuyerProvider provider) {
    if (provider.isLoadingListings && provider.listings.isEmpty) {
      return const BuyerLoadingView(message: 'Searching available harvests...');
    }

    if (provider.listingsError != null && provider.listings.isEmpty) {
      return BuyerErrorView(
        error: provider.listingsError!,
        onRetry: () => provider.fetchListings(),
      );
    }

    if (provider.listings.isEmpty) {
      return BuyerEmptyView(
        icon: Icons.inventory_2_outlined,
        title: 'No Listings Found',
        description: 'No active farmer listings match your current filters. Try relaxing the search or distance range.',
        actionLabel: 'Reset Filters',
        onAction: () => provider.setFilters(crop: 'All', grade: 'All', minQty: 0.0, maxDistanceKm: null),
      );
    }

    return ListView.builder(
      physics: const AlwaysScrollableScrollPhysics(parent: BouncingScrollPhysics()),
      padding: const EdgeInsets.symmetric(
        horizontal: AgriDimensions.screenPadding,
        vertical: 8,
      ),
      itemCount: provider.listings.length,
      itemBuilder: (context, index) {
        final item = provider.listings[index];
        return ListingCard(
          listing: item,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ListingDetailScreen(listingId: item.id),
              ),
            );
          },
        );
      },
    );
  }
}
