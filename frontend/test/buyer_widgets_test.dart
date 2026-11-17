/// AgriMate AI - Buyer Widget Tests
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:agrimate_ai/models/buyer_models.dart';
import 'package:agrimate_ai/theme/app_theme.dart';
import 'package:agrimate_ai/widgets/buyer/buyer_match_radar_card.dart';
import 'package:agrimate_ai/widgets/buyer/deal_card.dart';
import 'package:agrimate_ai/widgets/buyer/deal_timeline_widget.dart';
import 'package:agrimate_ai/widgets/buyer/express_interest_dialog.dart';
import 'package:agrimate_ai/widgets/buyer/listing_card.dart';
import 'package:agrimate_ai/widgets/buyer/state_views.dart';

void main() {
  group('Buyer Dashboard Widget Tests', () {
    testWidgets('ListingCard renders listing details and responds to tap', (WidgetTester tester) async {
      final sampleListing = ListingItem(
        id: 101,
        farmerId: 5,
        farmerName: 'Haji Ghulam Rasool',
        crop: 'Potato',
        grade: 'A',
        quantity: 8000.0,
        askingPrice: 2450.0,
        location: 'Okara Bypass Farm',
        distanceKm: 42.0,
        totalMatchScore: 94.0,
        status: 'active',
        createdAt: DateTime.now(),
        alreadyInterested: false,
      );

      bool tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: ListingCard(
              listing: sampleListing,
              onTap: () {
                tapped = true;
              },
            ),
          ),
        ),
      );

      // Verify content rendered
      expect(find.text('Potato'), findsOneWidget);
      expect(find.text('Grade A'), findsOneWidget);
      expect(find.text('Haji Ghulam Rasool'), findsOneWidget);
      expect(find.text('8000 kg'), findsOneWidget);
      expect(find.textContaining('PKR 2450'), findsOneWidget);
      expect(find.text('42 km'), findsOneWidget);
      expect(find.text('94% Match'), findsOneWidget);
      expect(find.text('Okara Bypass Farm'), findsOneWidget);

      // Verify tap callback
      await tester.tap(find.byType(ListingCard));
      await tester.pumpAndSettle();
      expect(tapped, isTrue);
    });

    testWidgets('ExpressInterestDialog validates inputs and submits', (WidgetTester tester) async {
      final sampleListing = ListingItem(
        id: 102,
        farmerId: 6,
        farmerName: 'Malik Riaz',
        crop: 'Tomato',
        grade: 'A',
        quantity: 3500.0,
        askingPrice: 2600.0,
        location: 'Multan Shujabad Farm',
        distanceKm: 95.0,
        totalMatchScore: 88.0,
        status: 'active',
        createdAt: DateTime.now(),
        alreadyInterested: false,
      );

      double? submittedPrice;
      double? submittedQty;
      String? submittedMsg;

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: Builder(
              builder: (context) => ElevatedButton(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (_) => ExpressInterestDialog(
                      listing: sampleListing,
                      onSubmit: ({
                        required double offeredPrice,
                        required double quantityWanted,
                        String? message,
                      }) async {
                        submittedPrice = offeredPrice;
                        submittedQty = quantityWanted;
                        submittedMsg = message;
                      },
                    ),
                  );
                },
                child: const Text('Open Modal'),
              ),
            ),
          ),
        ),
      );

      // Tap button to open dialog
      await tester.tap(find.text('Open Modal'));
      await tester.pumpAndSettle();

      // Verify modal content
      expect(find.text('Express Purchase Interest'), findsOneWidget);
      expect(find.textContaining('Tomato Grade A'), findsOneWidget);
      expect(find.text('Submit Interest'), findsOneWidget);

      // Tap Submit Interest
      await tester.tap(find.text('Submit Interest'));
      await tester.pumpAndSettle();

      // Verify callback was invoked with valid values
      expect(submittedPrice, isNotNull);
      expect(submittedPrice, greaterThan(0));
      expect(submittedQty, isNotNull);
      expect(submittedQty, greaterThan(0));
    });

    testWidgets('BuyerMatchRadarCard renders 5-part explainable breakdown', (WidgetTester tester) async {
      const breakdown = MatchScoreBreakdown(
        cropMatch: true,
        quantityScore: 23.5,
        distanceScore: 22.0,
        gradeScore: 25.0,
        priceScore: 24.5,
        totalScore: 95.0,
        distanceKm: 48.0,
        matchLevel: 'EXCELLENT',
        explanation: 'Excellent alignment across grade, price, distance and batch volume.',
      );

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: const Scaffold(
            body: SingleChildScrollView(
              child: BuyerMatchRadarCard(match: breakdown),
            ),
          ),
        ),
      );

      // Verify header and level
      expect(find.text('Match Affinity Score'), findsOneWidget);
      expect(find.text('95% • EXCELLENT'), findsOneWidget);

      // Verify mandatory crop gate
      expect(find.textContaining('Crop Match Passed'), findsOneWidget);

      // Verify 4 itemized factors
      expect(find.text('Quantity Fit (25%)'), findsOneWidget);
      expect(find.textContaining('Distance Fit (25%)'), findsOneWidget);
      expect(find.text('Grade Fit (25%)'), findsOneWidget);
      expect(find.text('Price Fit (25%)'), findsOneWidget);

      // Verify explanation
      expect(find.textContaining('Excellent alignment'), findsOneWidget);
    });

    testWidgets('DecisionDisclaimerBanner renders prototype notice', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: const Scaffold(
            body: DecisionDisclaimerBanner(),
          ),
        ),
      );

      expect(
        find.text('Decision-support prototype: no payments or legal contracts'),
        findsOneWidget,
      );
    });

    testWidgets('DealTimelineWidget renders audit history items', (WidgetTester tester) async {
      final history = [
        DealHistoryItem(
          id: 1,
          status: 'interested',
          notes: 'Purchase interest submitted by buyer.',
          changedAt: DateTime.now().subtract(const Duration(days: 2)),
        ),
        DealHistoryItem(
          id: 2,
          status: 'accepted',
          notes: 'Farmer accepted bid of PKR 2,400/maund.',
          changedAt: DateTime.now().subtract(const Duration(days: 1)),
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: SingleChildScrollView(
              child: DealTimelineWidget(history: history),
            ),
          ),
        ),
      );

      expect(find.text('Deal Lifecycle Audit Timeline'), findsOneWidget);
      expect(find.text('Interest Submitted'), findsOneWidget);
      expect(find.text('Offer Accepted by Farmer'), findsOneWidget);
      expect(find.text('Purchase interest submitted by buyer.'), findsOneWidget);
      expect(find.text('Farmer accepted bid of PKR 2,400/maund.'), findsOneWidget);
    });
  });
}
