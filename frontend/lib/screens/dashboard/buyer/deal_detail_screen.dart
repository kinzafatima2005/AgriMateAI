/// AgriMate AI - Buyer Deal Detail Screen
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../models/buyer_models.dart';
import '../../../services/buyer_api_service.dart';
import '../../../services/buyer_provider.dart';
import '../../../theme/app_theme.dart';
import '../../../widgets/buyer/deal_timeline_widget.dart';
import '../../../widgets/buyer/state_views.dart';

class DealDetailScreen extends StatefulWidget {
  final int dealId;

  const DealDetailScreen({
    super.key,
    required this.dealId,
  });

  @override
  State<DealDetailScreen> createState() => _DealDetailScreenState();
}

class _DealDetailScreenState extends State<DealDetailScreen> {
  BuyerDeal? _deal;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadDeal();
  }

  Future<void> _loadDeal() async {
    final buyerProv = Provider.of<BuyerProvider>(context, listen: false);
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final d = await BuyerApiService.getDealDetail(buyerProv.token, widget.dealId);
      setState(() {
        _deal = d;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _isLoading = false;
      });
    }
  }

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
          title: Text('Deal #${widget.dealId}', style: Theme.of(context).textTheme.headlineMedium),
        ),
        body: const BuyerLoadingView(message: 'Loading deal timeline...'),
      );
    }

    if (_error != null || _deal == null) {
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
          error: _error ?? 'Failed to load deal',
          onRetry: _loadDeal,
        ),
      );
    }

    final d = _deal!;
    final statusColor = _getStatusColor(d.status);

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
          '${d.crop} Deal #${d.id}',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontSize: 18),
        ),
      ),
      body: SafeArea(
        child: RefreshIndicator(
          color: AgriColors.primaryGreen,
          onRefresh: _loadDeal,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(parent: BouncingScrollPhysics()),
            padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 10),

                // Deal Header Card
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  decoration: AppTheme.cardDecoration(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              Text(
                                d.crop,
                                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                                      fontSize: 20,
                                      fontWeight: FontWeight.w800,
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
                                  'Grade ${d.grade}',
                                  style: const TextStyle(
                                    color: AgriColors.primaryGreen,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 11.5,
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
                              _formatStatus(d.status),
                              style: TextStyle(
                                color: statusColor,
                                fontWeight: FontWeight.w800,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 16),

                      // Metrics
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                        decoration: BoxDecoration(
                          color: AgriColors.cardSurfaceLight,
                          borderRadius: BorderRadius.circular(14),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            Column(
                              children: [
                                Text('Quantity Wanted', style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11)),
                                const SizedBox(height: 3),
                                Text(
                                  '${d.quantityWanted.toStringAsFixed(0)} kg',
                                  style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14),
                                ),
                              ],
                            ),
                            Container(width: 1, height: 28, color: AgriColors.divider),
                            Column(
                              children: [
                                Text('Offered Price', style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11)),
                                const SizedBox(height: 3),
                                Text(
                                  'PKR ${d.offeredPrice.toStringAsFixed(0)}',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.w700,
                                    fontSize: 14,
                                    color: AgriColors.primaryGreen,
                                  ),
                                ),
                              ],
                            ),
                            Container(width: 1, height: 28, color: AgriColors.divider),
                            Column(
                              children: [
                                Text('Asking Price', style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11)),
                                const SizedBox(height: 3),
                                Text(
                                  'PKR ${d.askingPrice.toStringAsFixed(0)}',
                                  style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: AgriColors.textSecondary),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 14),

                      // Farmer & Location
                      Row(
                        children: [
                          const Icon(Icons.person_outline_rounded, size: 16, color: AgriColors.iconOutline),
                          const SizedBox(width: 6),
                          Text(
                            'Farmer: ${d.farmerName}',
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          const Icon(Icons.location_on_outlined, size: 16, color: AgriColors.iconOutline),
                          const SizedBox(width: 6),
                          Text(
                            d.farmerLocation,
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  fontSize: 12.5,
                                  color: AgriColors.textSecondary,
                                ),
                          ),
                        ],
                      ),

                      if (d.message != null && d.message!.isNotEmpty) ...[
                        const SizedBox(height: 10),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: AgriColors.cardSurfaceLight,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            'Note: ${d.message!}',
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  fontSize: 12,
                                  fontStyle: FontStyle.italic,
                                ),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),

                const SizedBox(height: 18),

                // Decision Disclaimer Notice
                const DecisionDisclaimerBanner(),

                const SizedBox(height: 18),

                // Audit Timeline
                DealTimelineWidget(history: d.history),

                const SizedBox(height: 30),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
