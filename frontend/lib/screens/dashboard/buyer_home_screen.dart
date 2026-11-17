/// AgriMate AI - Buyer Home Screen Wrapper
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/auth_provider.dart';
import '../../services/buyer_provider.dart';
import 'buyer/buyer_main_screen.dart';

class BuyerHomeScreen extends StatelessWidget {
  const BuyerHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final token = auth.currentUser?.token ?? '';

    return ChangeNotifierProvider(
      create: (_) => BuyerProvider(token: token),
      child: const BuyerMainScreen(),
    );
  }
}
