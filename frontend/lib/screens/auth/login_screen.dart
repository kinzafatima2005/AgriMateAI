import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/auth_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/agri_logo.dart';
import '../../widgets/decision_disclaimer_banner.dart';
import '../dashboard/farmer_home_screen.dart';
import '../dashboard/buyer_home_screen.dart';
import '../dashboard/expert_home_screen.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneOrEmailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _phoneOrEmailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _fillDemoAccount(String phoneOrEmail, String password) {
    setState(() {
      _phoneOrEmailController.text = phoneOrEmail;
      _passwordController.text = password;
    });
  }

  Future<void> _submitLogin() async {
    if (!_formKey.currentState!.validate()) return;

    final auth = Provider.of<AuthProvider>(context, listen: false);
    final success = await auth.login(
      _phoneOrEmailController.text.trim(),
      _passwordController.text,
    );

    if (!mounted) return;

    if (success && auth.currentUser != null) {
      final role = auth.currentUser!.role;
      Widget target;
      if (role == 'Buyer') {
        target = const BuyerHomeScreen();
      } else if (role == 'Expert/Admin') {
        target = const ExpertHomeScreen();
      } else {
        target = const FarmerHomeScreen();
      }
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => target),
        (route) => false,
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(auth.errorMessage ?? 'Invalid login credentials'),
          backgroundColor: AgriColors.error,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: AgriColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 36),
                const Center(child: AgriLogo(size: 80)),
                const SizedBox(height: 32),

                Text(
                  'Welcome Back',
                  style: textTheme.displayMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: AgriColors.textDark,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Sign in to access your farm intelligence & advisory',
                  style: textTheme.bodyMedium?.copyWith(color: AgriColors.textSecondary),
                ),

                const SizedBox(height: 28),

                // Phone or Email
                TextFormField(
                  controller: _phoneOrEmailController,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: const InputDecoration(
                    labelText: 'Phone or Email',
                    prefixIcon: Icon(Icons.account_circle_outlined, color: AgriColors.primaryGreen),
                    hintText: '03001234567 or email',
                  ),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Please enter your phone or email';
                    return null;
                  },
                ),

                const SizedBox(height: 16),

                // Password
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: InputDecoration(
                    labelText: 'Password',
                    prefixIcon: const Icon(Icons.lock_outline_rounded, color: AgriColors.primaryGreen),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                        color: AgriColors.textSecondary,
                      ),
                      onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                    ),
                  ),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Please enter your password';
                    return null;
                  },
                ),

                const SizedBox(height: 24),

                // Sign In Button
                SizedBox(
                  width: double.infinity,
                  height: 56,
                  child: ElevatedButton(
                    onPressed: auth.isLoading ? null : _submitLogin,
                    child: auth.isLoading
                        ? const SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(
                              strokeWidth: 2.5,
                              valueColor: AlwaysStoppedAnimation<Color>(AgriColors.darkGreenText),
                            ),
                          )
                        : Text(
                            'Sign In',
                            style: textTheme.titleMedium?.copyWith(
                              color: AgriColors.darkGreenText,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                  ),
                ),

                const SizedBox(height: 28),

                // Quick Demo Accounts Selector (Effortless 1-Tap Fill)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: AppTheme.cardBoxDecoration(color: AgriColors.cardSurface),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.bolt_rounded, color: AgriColors.accentYellow, size: 18),
                          const SizedBox(width: 6),
                          Text(
                            '1-Tap Demo Accounts (Seeded)',
                            style: textTheme.labelSmall?.copyWith(
                              color: AgriColors.accentYellow,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          ActionChip(
                            label: const Text('Farmer (Multan)'),
                            backgroundColor: AgriColors.cardSurfaceLight,
                            labelStyle: const TextStyle(color: AgriColors.textDark, fontSize: 12, fontWeight: FontWeight.w600),
                            onPressed: () => _fillDemoAccount('03001234567', 'Password123!'),
                          ),
                          ActionChip(
                            label: const Text('Buyer (Faisalabad)'),
                            backgroundColor: AgriColors.cardSurfaceLight,
                            labelStyle: const TextStyle(color: AgriColors.textDark, fontSize: 12, fontWeight: FontWeight.w600),
                            onPressed: () => _fillDemoAccount('03219876543', 'Password123!'),
                          ),
                          ActionChip(
                            label: const Text('Agronomist Expert'),
                            backgroundColor: AgriColors.cardSurfaceLight,
                            labelStyle: const TextStyle(color: AgriColors.textDark, fontSize: 12, fontWeight: FontWeight.w600),
                            onPressed: () => _fillDemoAccount('expert.farooq@agrimate.pk', 'Password123!'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // Decision Support Disclaimer
                const DecisionDisclaimerBanner(compact: true),

                const SizedBox(height: 24),

                // Switch to Register
                Center(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text("Don't have an account? ", style: textTheme.bodyMedium),
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const RegisterScreen()),
                          );
                        },
                        child: Text(
                          'Register Now',
                          style: textTheme.bodyMedium?.copyWith(
                            color: AgriColors.accentYellow,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

