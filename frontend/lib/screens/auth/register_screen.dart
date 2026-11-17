import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/auth_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/agri_logo.dart';
import '../../widgets/decision_disclaimer_banner.dart';
import '../dashboard/farmer_home_screen.dart';
import '../dashboard/buyer_home_screen.dart';
import '../dashboard/expert_home_screen.dart';
import 'login_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();

  // STRICT minimal 5 fields only
  final _nameController = TextEditingController();
  final _phoneOrEmailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _locationController = TextEditingController();
  String _selectedRole = 'Farmer'; // Farmer, Buyer, Expert/Admin
  bool _obscurePassword = true;

  final List<String> _availableRoles = ['Farmer', 'Buyer', 'Expert/Admin'];

  @override
  void dispose() {
    _nameController.dispose();
    _phoneOrEmailController.dispose();
    _passwordController.dispose();
    _locationController.dispose();
    super.dispose();
  }

  Future<void> _submitRegister() async {
    if (!_formKey.currentState!.validate()) return;

    final auth = Provider.of<AuthProvider>(context, listen: false);
    final success = await auth.register(
      name: _nameController.text.trim(),
      phoneOrEmail: _phoneOrEmailController.text.trim(),
      password: _passwordController.text,
      role: _selectedRole,
      location: _locationController.text.trim(),
    );

    if (!mounted) return;

    if (success) {
      Widget target;
      if (_selectedRole == 'Buyer') {
        target = const BuyerHomeScreen();
      } else if (_selectedRole == 'Expert/Admin') {
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
          content: Text(auth.errorMessage ?? 'Registration failed'),
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
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AgriColors.textDark, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AgriDimensions.screenPadding),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Center(child: AgriLogo(size: 70, showText: false)),
                const SizedBox(height: 18),

                Text(
                  'Create Account',
                  style: textTheme.displayMedium?.copyWith(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: AgriColors.textDark,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Join the AgriMate decision-support agricultural network',
                  style: textTheme.bodyMedium?.copyWith(color: AgriColors.textSecondary),
                ),

                const SizedBox(height: 24),

                // 1. Role Selector Pill Chips
                Text('Select Role', style: textTheme.labelSmall?.copyWith(color: AgriColors.textSecondary)),
                const SizedBox(height: 8),
                Row(
                  children: _availableRoles.map((role) {
                    final isSelected = _selectedRole == role;
                    return Expanded(
                      child: GestureDetector(
                        onTap: () => setState(() => _selectedRole = role),
                        child: Container(
                          margin: const EdgeInsets.symmetric(horizontal: 4),
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: AppTheme.pillChipDecoration(isActive: isSelected),
                          alignment: Alignment.center,
                          child: Text(
                            role,
                            style: textTheme.labelSmall?.copyWith(
                              color: isSelected ? AgriColors.textWhite : AgriColors.textDark,
                              fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                              fontSize: 13,
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),

                const SizedBox(height: 18),

                // 2. Full Name
                TextFormField(
                  controller: _nameController,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: const InputDecoration(
                    labelText: 'Full Name',
                    prefixIcon: Icon(Icons.person_outline_rounded, color: AgriColors.primaryGreen),
                    hintText: 'e.g. Muhammad Tariq',
                  ),
                  validator: (v) {
                    if (v == null || v.trim().length < 2) return 'Please enter your full name';
                    return null;
                  },
                ),

                const SizedBox(height: 14),

                // 3. Phone or Email
                TextFormField(
                  controller: _phoneOrEmailController,
                  keyboardType: TextInputType.emailAddress,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: const InputDecoration(
                    labelText: 'Pakistani Phone or Email',
                    prefixIcon: Icon(Icons.phone_iphone_rounded, color: AgriColors.primaryGreen),
                    hintText: '03001234567 or farmer@agrimate.pk',
                  ),
                  validator: (v) {
                    if (v == null || v.trim().length < 5) {
                      return 'Enter a valid phone number (03XXXXXXXXX) or email';
                    }
                    return null;
                  },
                ),

                const SizedBox(height: 14),

                // 4. Password
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: InputDecoration(
                    labelText: 'Password',
                    prefixIcon: const Icon(Icons.lock_outline_rounded, color: AgriColors.primaryGreen),
                    hintText: 'Minimum 6 characters',
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                        color: AgriColors.textSecondary,
                      ),
                      onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                    ),
                  ),
                  validator: (v) {
                    if (v == null || v.length < 6) return 'Password must be at least 6 characters';
                    return null;
                  },
                ),

                const SizedBox(height: 14),

                // 5. Location
                TextFormField(
                  controller: _locationController,
                  style: const TextStyle(color: AgriColors.textDark),
                  decoration: const InputDecoration(
                    labelText: 'Location (District, Province)',
                    prefixIcon: Icon(Icons.location_on_outlined, color: AgriColors.primaryGreen),
                    hintText: 'e.g. Multan, Punjab or Sukkur, Sindh',
                  ),
                  validator: (v) {
                    if (v == null || v.trim().length < 3) return 'Please enter your district and province';
                    return null;
                  },
                ),

                const SizedBox(height: 22),

                // Submit Button
                SizedBox(
                  width: double.infinity,
                  height: 56,
                  child: ElevatedButton(
                    onPressed: auth.isLoading ? null : _submitRegister,
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
                            'Register as $_selectedRole',
                            style: textTheme.titleMedium?.copyWith(
                              color: AgriColors.darkGreenText,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                  ),
                ),

                const SizedBox(height: 20),

                // Legal Decision-Support Disclaimer Banner
                const DecisionDisclaimerBanner(),

                const SizedBox(height: 24),

                // Switch to Login
                Center(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('Already registered? ', style: textTheme.bodyMedium),
                      GestureDetector(
                        onTap: () {
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(builder: (_) => const LoginScreen()),
                          );
                        },
                        child: Text(
                          'Sign In',
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

