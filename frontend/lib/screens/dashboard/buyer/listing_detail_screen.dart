/// AgriMate AI - Buyer Listing Detail Screen
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../models/buyer_models.dart';
import '../../../services/buyer_api_service.dart';
import '../../../services/buyer_provider.dart';
import '../../../theme/app_theme.dart';
import '../../../widgets/buyer/buyer_match_radar_card.dart';
import '../../../widgets/buyer/express_interest_dialog.dart';
import '../../../widgets/buyer/state_views.dart';

class ListingDetailScreen extends StatefulWidget {
  final int listingId;

  const ListingDetailScreen({
    super.key,
    required this.listingId,
  });

  @override
  State<ListingDetailScreen> createState() => _ListingDetailScreenState();
}

class _ListingDetailScreenState extends State<ListingDetailScreen> {
  ListingDetail? _listing;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadDetail();
  }

  Future<void> _loadDetail() async {
    final buyerProv = Provider.of<BuyerProvider>(context, listen: false);
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final detail = await BuyerApiService.getListingDetail(buyerProv.token, widget.listingId);
      setState(() {
        _listing = detail;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  void _showExpressInterestModal() {
    if (_listing == null) return;
    final buyerProv = Provider.of<BuyerProvider>(context, listen: false);

    showDialog<bool>(
      context: context,
      builder: (_) => ExpressInterestDialog(
        listing: _listing!,
        onSubmit: ({
          required double offeredPrice,
          required double quantityWanted,
          String? message,
        }) async {
          await buyerProv.expressInterest(
            _listing!.id,
            offeredPrice: offeredPrice,
            quantityWanted: quantityWanted,
            message: message,
          );
        },
      ),
    ).then((success) {
      if (success == true) {
        _loadDetail();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Purchase interest submitted! Farmer has been notified.'),
            backgroundColor: AgriColors.primaryGreen,
          ),
        );
      }
    });
  }

  String _getCropEmoji(String crop) {
    final lower = crop.toLowerCase();
    if (lower.contains('potato')) return '🥔';
    if (lower.contains('tomato')) return '🍅';
    if (lower.contains('wheat')) return '🌾';
    return '🌱';
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        backgroundColor: AgriColors.background,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          leading: IconButton(
            icon: const Icon(Icons.arrow_back_ios_rounded, color: AgriColors.textPrimary),
            onPressed: () => Navigator.pop(context),
          ),
          title: Text('Produce Listing #${widget.listingId}', style: Theme.of(context).textTheme.headlineMedium),
        ),
        body: const BuyerLoadingView(message: 'Calculating affinity match score...'),
      );
    }

    if (_error != null || _listing == null) {
      return Scaffold(
        backgroundColor: AgriColors.background,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          leading: IconButton(
            icon: const Icon(Icons.arrow_back_ios_rounded, color: AgriColors.textPrimary),
            onPressed: () => Navigator.pop(context),
          ),
        ),
        body: BuyerErrorView(
          error: _error ?? 'Failed to load listing',
          onRetry: _loadDetail,
        ),
      );
    }

    final l = _listing!;

    return Scaffold(
      backgroundColor: AgriColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_rounded, color: AgriColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          '${l.crop} Lot #${l.id}',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontSize: 18),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 10),

              // Overview Hero Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(22),
                decoration: AppTheme.cardDecoration(),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 54,
                          height: 54,
                          decoration: const BoxDecoration(
                            color: AgriColors.cardSurfaceLight,
                            shape: BoxShape.circle,
                          ),
                          alignment: Alignment.center,
                          child: Text(_getCropEmoji(l.crop), style: const TextStyle(fontSize: 28)),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Text(
                                    l.crop,
                                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                                          fontSize: 22,
                                          fontWeight: FontWeight.w800,
                                        ),
                                  ),
                                  const SizedBox(width: 8),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                    decoration: BoxDecoration(
                                      color: AgriColors.cardSurfaceLight,
                                      borderRadius: BorderRadius.circular(6),
                                      border: Border.all(color: AgriColors.cardBorder, width: 1),
                                    ),
                                    child: Text(
                                      'Grade ${l.grade}',
                                      style: const TextStyle(
                                        color: AgriColors.primaryGreen,
                                        fontWeight: FontWeight.w700,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Posted by ${l.farmerName}',
                                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                      color: AgriColors.textSecondary,
                                      fontSize: 13,
                                    ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 18),

                    // Metrics Grid (Quantity, Asking Price, Location, Distance)
                    Row(
                      children: [
                        Expanded(
                          child: _buildMetricTile(
                            context,
                            label: 'Total Available',
                            value: '${l.quantity.toStringAsFixed(0)} kg',
                            icon: Icons.inventory_2_outlined,
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: _buildMetricTile(
                            context,
                            label: 'Asking Price',
                            value: 'PKR ${l.askingPrice.toStringAsFixed(0)}',
                            sublabel: '/ 40kg',
                            icon: Icons.sell_outlined,
                            highlightColor: AgriColors.primaryGreen,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Expanded(
                          child: _buildMetricTile(
                            context,
                            label: 'Farm Location',
                            value: l.location,
                            icon: Icons.location_on_outlined,
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: _buildMetricTile(
                            context,
                            label: 'Road Distance',
                            value: l.distanceKm != null ? '${l.distanceKm!.toStringAsFixed(0)} km away' : '-- km',
                            icon: Icons.near_me_outlined,
                          ),
                        ),
                      ],
                    ),

                    if (l.farmerContact != null) ...[
                      const SizedBox(height: 14),
                      Row(
                        children: [
                          const Icon(Icons.phone_outlined, size: 16, color: AgriColors.iconOutline),
                          const SizedBox(width: 6),
                          Text(
                            'Farmer Contact: ${l.farmerContact}',
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  color: AgriColors.textSecondary,
                                  fontSize: 12.5,
                                ),
                          ),
                        ],
                      ),
                    ],
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // Match Score Radar Breakdown
              if (l.matchBreakdown != null)
                BuyerMatchRadarCard(match: l.matchBreakdown!),

              const SizedBox(height: 20),

              // Prototype Disclaimer
              const DecisionDisclaimerBanner(),

              const SizedBox(height: 90), // Bottom padding for fixed action bar
            ],
          ),
        ),
      ),
      bottomSheet: Container(
        padding: const EdgeInsets.all(AgriDimensions.screenPadding),
        decoration: BoxDecoration(
          color: AgriColors.background,
          border: const Border(top: BorderSide(color: AgriColors.cardBorder, width: 1)),
        ),
        child: SafeArea(
          child: SizedBox(
            width: double.infinity,
            height: 52,
            child: ElevatedButton(
              onPressed: l.alreadyInterested ? null : _showExpressInterestModal,
              style: ElevatedButton.styleFrom(
                backgroundColor: l.alreadyInterested ? AgriColors.cardSurfaceLight : AgriColors.primaryGreen,
                foregroundColor: l.alreadyInterested ? AgriColors.textSecondary : AgriColors.textWhite,
              ),
              child: Text(
                l.alreadyInterested ? 'Interest Already Sent' : 'Express Purchase Interest',
                style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMetricTile(
    BuildContext context, {
    required String label,
    required String value,
    String? sublabel,
    required IconData icon,
    Color? highlightColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AgriColors.cardSurfaceLight,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 14, color: AgriColors.iconOutline),
              const SizedBox(width: 4),
              Text(
                label,
                style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11),
              ),
            ],
          ),
          const SizedBox(height: 4),
          RichText(
            text: TextSpan(
              text: value,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w700,
                color: highlightColor ?? AgriColors.textPrimary,
                fontFamily: Theme.of(context).textTheme.bodyLarge?.fontFamily,
              ),
              children: sublabel != null
                  ? [
                      TextSpan(
                        text: ' $sublabel',
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
      ),
    );
  }
}
