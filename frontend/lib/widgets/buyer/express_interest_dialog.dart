/// AgriMate AI - Express Purchase Interest Dialog
import 'package:flutter/material.dart';
import '../../models/buyer_models.dart';
import '../../theme/app_theme.dart';

class ExpressInterestDialog extends StatefulWidget {
  final ListingItem listing;
  final Function({
    required double offeredPrice,
    required double quantityWanted,
    String? message,
  }) onSubmit;

  const ExpressInterestDialog({
    super.key,
    required this.listing,
    required this.onSubmit,
  });

  @override
  State<ExpressInterestDialog> createState() => _ExpressInterestDialogState();
}

class _ExpressInterestDialogState extends State<ExpressInterestDialog> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _priceController;
  late TextEditingController _qtyController;
  late TextEditingController _messageController;
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _priceController = TextEditingController(text: widget.listing.askingPrice.toStringAsFixed(0));
    _qtyController = TextEditingController(
      text: (widget.listing.quantity * 0.5).clamp(1000.0, widget.listing.quantity).toStringAsFixed(0),
    );
    _messageController = TextEditingController(
      text: 'Interested in purchasing this lot. Please confirm pickup schedule.',
    );
  }

  @override
  void dispose() {
    _priceController.dispose();
    _qtyController.dispose();
    _messageController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final price = double.tryParse(_priceController.text.trim()) ?? 0.0;
    final qty = double.tryParse(_qtyController.text.trim()) ?? 0.0;
    final msg = _messageController.text.trim();

    setState(() => _isSubmitting = true);
    try {
      await widget.onSubmit(
        offeredPrice: price,
        quantityWanted: qty,
        message: msg.isEmpty ? null : msg,
      );
      if (mounted) Navigator.pop(context, true);
    } catch (e) {
      if (mounted) {
        setState(() => _isSubmitting = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(e.toString().replaceFirst('Exception: ', '')),
            backgroundColor: AgriColors.error,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: AgriColors.background,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AgriDimensions.cardRadius),
      ),
      insetPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
      child: Padding(
        padding: const EdgeInsets.all(22),
        child: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Express Purchase Interest',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                          ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close_rounded, size: 20, color: AgriColors.iconOutline),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ],
                ),
                const SizedBox(height: 8),

                // Listing summary badge
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.inventory_2_outlined, size: 20, color: AgriColors.primaryGreen),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          '${widget.listing.crop} Grade ${widget.listing.grade} • Asking PKR ${widget.listing.askingPrice.toStringAsFixed(0)}/40kg',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                                color: AgriColors.textPrimary,
                                fontSize: 13,
                              ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 18),

                // Offered Price Field
                Text(
                  'Offered Bid Price (PKR / 40kg maund)',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                const SizedBox(height: 6),
                TextFormField(
                  controller: _priceController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.sell_outlined, size: 18, color: AgriColors.iconOutline),
                    hintText: 'e.g. 2400',
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Enter offered price';
                    final num = double.tryParse(val);
                    if (num == null || num <= 0) return 'Enter a valid positive price';
                    return null;
                  },
                ),

                const SizedBox(height: 16),

                // Quantity Wanted Field
                Text(
                  'Quantity Wanted (kg)',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                const SizedBox(height: 6),
                TextFormField(
                  controller: _qtyController,
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    prefixIcon: const Icon(Icons.scale_outlined, size: 18, color: AgriColors.iconOutline),
                    hintText: 'e.g. 5000',
                    helperText: 'Max available: ${widget.listing.quantity.toStringAsFixed(0)} kg',
                    helperStyle: const TextStyle(color: AgriColors.textSecondary, fontSize: 11),
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Enter quantity wanted';
                    final num = double.tryParse(val);
                    if (num == null || num <= 0) return 'Enter a valid quantity';
                    if (num > widget.listing.quantity) {
                      return 'Cannot exceed available ${widget.listing.quantity.toStringAsFixed(0)} kg';
                    }
                    return null;
                  },
                ),

                const SizedBox(height: 16),

                // Optional Message
                Text(
                  'Message to Farmer (Optional)',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AgriColors.textPrimary,
                      ),
                ),
                const SizedBox(height: 6),
                TextFormField(
                  controller: _messageController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    hintText: 'Add transport, packing or pickup notes...',
                  ),
                ),

                const SizedBox(height: 18),

                // Decision support notice
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                  decoration: BoxDecoration(
                    color: AgriColors.cardSurfaceLight,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.info_outline, size: 14, color: AgriColors.accentYellow),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          'Decision-support prototype: no legal contracts or payments.',
                          style: Theme.of(context).textTheme.labelSmall?.copyWith(fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 22),

                // Action Buttons
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: _isSubmitting ? null : () => Navigator.pop(context),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: AgriColors.cardBorder),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(AgriDimensions.pillRadius),
                          ),
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        child: const Text('Cancel', style: TextStyle(color: AgriColors.textSecondary)),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      flex: 2,
                      child: ElevatedButton(
                        onPressed: _isSubmitting ? null : _submit,
                        child: _isSubmitting
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(AgriColors.textWhite),
                                ),
                              )
                            : const Text('Submit Interest'),
                      ),
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
