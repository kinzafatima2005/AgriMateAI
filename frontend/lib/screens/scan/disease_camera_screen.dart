import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../widgets/decision_disclaimer_banner.dart';
import 'scan_result_screen.dart';

class DiseaseCameraScreen extends StatefulWidget {
  const DiseaseCameraScreen({super.key});

  @override
  State<DiseaseCameraScreen> createState() => _DiseaseCameraScreenState();
}

class _DiseaseCameraScreenState extends State<DiseaseCameraScreen> {
  bool _isAnalyzing = false;
  String _lightingStatus = 'Optimal';
  String _sharpnessStatus = 'Sharp Veins';
  bool _qualityPassed = true;
  String? _qualityWarning;

  // Phase 4: Multimodal crop & spoken/typed description state
  String _selectedCrop = 'Potato (آلو)';
  final TextEditingController _descController = TextEditingController(
    text: 'کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں',
  );

  @override
  void dispose() {
    _descController.dispose();
    super.dispose();
  }

  void _showSpeechToTextDialog() {
    final speechPrompts = [
      'کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں',
      'پتوں پر گول کالے دائرے اور دھبے ہیں',
      'پھول گر رہے ہیں اور ٹماٹر پر سنڈی ہے',
      'aaloo ke patte pe pachita jhalsao aur keera hai',
    ];

    showModalBottomSheet(
      context: context,
      backgroundColor: AgriColors.backgroundDark,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setSheetState) {
            return Padding(
              padding: EdgeInsets.only(
                left: 20,
                right: 20,
                top: 20,
                bottom: MediaQuery.of(ctx).viewInsets.bottom + 24,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: const [
                          Icon(Icons.mic_rounded, color: AgriColors.accentYellow, size: 24),
                          SizedBox(width: 8),
                          Text(
                            'Voice Description (بول کر بتائیں)',
                            style: TextStyle(
                              color: AgriColors.textWhite,
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close_rounded, color: AgriColors.textWhite),
                        onPressed: () => Navigator.pop(ctx),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Speech-to-Text: Urdu, English, Roman Urdu (Extensible to Punjabi, Pashto, Sindhi). Review and edit before submitting.',
                    style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                  ),
                  const SizedBox(height: 14),

                  // Editable transcript text field
                  TextField(
                    controller: _descController,
                    maxLines: 3,
                    style: const TextStyle(color: AgriColors.textWhite, fontSize: 14),
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AgriColors.surfaceGlass,
                      hintText: 'Edit transcript here...',
                      hintStyle: const TextStyle(color: AgriColors.textSecondary),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(16),
                        borderSide: const BorderSide(color: Colors.white24),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(16),
                        borderSide: const BorderSide(color: AgriColors.accentYellow, width: 2),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Quick Spoken Phrase Chips
                  const Text(
                    'Quick Farmer Phrases (ایک کلک پر منتخب کریں):',
                    style: TextStyle(color: AgriColors.textSecondary, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: speechPrompts.map((phrase) {
                      return ActionChip(
                        label: Text(phrase, style: const TextStyle(fontSize: 11, color: AgriColors.textWhite)),
                        backgroundColor: AgriColors.surfaceGlass,
                        side: const BorderSide(color: Colors.white24),
                        onPressed: () {
                          setSheetState(() {
                            _descController.text = phrase;
                          });
                          setState(() {});
                        },
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 18),

                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AgriColors.accentYellow,
                      foregroundColor: AgriColors.backgroundDark,
                      minimumSize: const Size.fromHeight(48),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                    ),
                    icon: const Icon(Icons.check_circle_rounded),
                    label: const Text('Confirm Description (تصدیق کریں)', style: TextStyle(fontWeight: FontWeight.bold)),
                    onPressed: () {
                      setState(() {});
                      Navigator.pop(ctx);
                    },
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  void _simulateCapture({bool lowConfidence = false, bool blurry = false}) async {
    if (blurry) {
      setState(() {
        _lightingStatus = 'Poor';
        _sharpnessStatus = 'Blurry';
        _qualityPassed = false;
        _qualityWarning = 'Image Blurry: Please hold camera steady to capture leaf veins.';
      });
      return;
    }

    setState(() {
      _isAnalyzing = true;
      _lightingStatus = 'Optimal';
      _sharpnessStatus = 'Sharp Veins';
      _qualityPassed = true;
      _qualityWarning = null;
    });

    await Future.delayed(const Duration(milliseconds: 600));

    if (!mounted) return;
    setState(() => _isAnalyzing = false);

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ScanResultScreen(
          isLowConfidenceDemo: lowConfidence,
          cropName: _selectedCrop,
          userDescription: _descController.text.trim(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Multimodal Leaf Scanner',
          style: textTheme.titleMedium?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        actions: [
          // Crop Selector Toggle (Potato vs Tomato)
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: DropdownButton<String>(
              value: _selectedCrop,
              dropdownColor: AgriColors.backgroundDark,
              underline: const SizedBox(),
              icon: const Icon(Icons.keyboard_arrow_down_rounded, color: AgriColors.accentYellow),
              style: const TextStyle(color: AgriColors.accentYellow, fontSize: 12, fontWeight: FontWeight.bold),
              items: const [
                DropdownMenuItem(value: 'Potato (آلو)', child: Text('🥔 Potato (آلو)')),
                DropdownMenuItem(value: 'Tomato (ٹماٹر)', child: Text('🍅 Tomato (ٹماٹر)')),
              ],
              onChanged: (val) {
                if (val != null) setState(() => _selectedCrop = val);
              },
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Quality Validation Status Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
              color: Colors.black.withOpacity(0.8),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(
                        _qualityPassed ? Icons.wb_sunny_rounded : Icons.warning_amber_rounded,
                        color: _qualityPassed ? AgriColors.accentYellow : AgriColors.error,
                        size: 16,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        'Lighting: $_lightingStatus',
                        style: TextStyle(
                          color: _qualityPassed ? Colors.white : AgriColors.error,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      Icon(
                        _qualityPassed ? Icons.center_focus_strong_rounded : Icons.blur_on_rounded,
                        color: _qualityPassed ? AgriColors.accentYellow : AgriColors.error,
                        size: 16,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        'Focus: $_sharpnessStatus',
                        style: TextStyle(
                          color: _qualityPassed ? Colors.white : AgriColors.error,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            if (_qualityWarning != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                color: AgriColors.error.withOpacity(0.9),
                child: Text(
                  _qualityWarning!,
                  style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
              ),

            // Viewfinder Area
            Expanded(
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Camera viewfinder gradient background
                  Container(
                    width: double.infinity,
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Color(0xFF1B2810), Color(0xFF334D1E), Color(0xFF4D6E2E)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                    ),
                  ),

                  // Simulated Leaf Graphic
                  CustomPaint(
                    size: const Size(220, 260),
                    painter: LeafSimulationPainter(isPotato: _selectedCrop.contains('Potato')),
                  ),

                  // Focus Target Reticle
                  Container(
                    width: 260,
                    height: 300,
                    decoration: BoxDecoration(
                      border: Border.all(color: AgriColors.accentYellow, width: 2),
                      borderRadius: BorderRadius.circular(28),
                    ),
                    child: Align(
                      alignment: Alignment.topCenter,
                      child: Container(
                        margin: const EdgeInsets.only(top: 10),
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.6),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          'Align $_selectedCrop leaf inside box',
                          style: const TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ),

                  if (_isAnalyzing)
                    Container(
                      color: Colors.black54,
                      child: Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: const [
                            CircularProgressIndicator(color: AgriColors.accentYellow),
                            SizedBox(height: 12),
                            Text(
                              'Running INT8 TFLite + Multimodal RAG...',
                              style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),
            ),

            // Phase 4: Farmer Spoken/Typed Description Bar with Mic Button
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              color: Colors.black.withOpacity(0.92),
              child: Row(
                children: [
                  Expanded(
                    child: GestureDetector(
                      onTap: _showSpeechToTextDialog,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.edit_note_rounded, color: AgriColors.accentYellow, size: 18),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                _descController.text.isEmpty
                                    ? 'Tap to speak/type symptom notes...'
                                    : _descController.text,
                                style: TextStyle(
                                  color: _descController.text.isEmpty ? Colors.white54 : Colors.white,
                                  fontSize: 12,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  // Mic Button (Urdu / English / Roman Urdu STT)
                  InkWell(
                    onTap: _showSpeechToTextDialog,
                    borderRadius: BorderRadius.circular(24),
                    child: Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        color: AgriColors.accentYellow,
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(color: AgriColors.accentYellow.withOpacity(0.4), blurRadius: 8, spreadRadius: 1),
                        ],
                      ),
                      child: const Icon(Icons.mic_rounded, color: AgriColors.backgroundDark, size: 24),
                    ),
                  ),
                ],
              ),
            ),

            // Shutter Controls Bottom Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
              color: Colors.black,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  // Test Option: Blurry / Poor Quality
                  IconButton(
                    icon: const Icon(Icons.blur_linear_rounded, color: Colors.white70),
                    tooltip: 'Test Blur Validation',
                    onPressed: () => _simulateCapture(blurry: true),
                  ),

                  // Main Shutter Button (Multimodal Scan)
                  GestureDetector(
                    onTap: () => _simulateCapture(lowConfidence: false),
                    child: Container(
                      width: 72,
                      height: 72,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: AgriColors.accentYellow,
                        border: Border.all(color: Colors.white, width: 4),
                        boxShadow: [
                          BoxShadow(
                            color: AgriColors.accentYellow.withOpacity(0.5),
                            blurRadius: 16,
                            spreadRadius: 2,
                          ),
                        ],
                      ),
                      child: const Icon(Icons.camera_alt_rounded, color: AgriColors.backgroundDark, size: 32),
                    ),
                  ),

                  // Test Option: Low Confidence (<75% Auto-Flag)
                  IconButton(
                    icon: const Icon(Icons.warning_amber_rounded, color: AgriColors.accentYellow),
                    tooltip: 'Test <75% Low Confidence Flag',
                    onPressed: () => _simulateCapture(lowConfidence: true),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class LeafSimulationPainter extends CustomPainter {
  final bool isPotato;
  LeafSimulationPainter({this.isPotato = true});

  @override
  void paint(Canvas canvas, Size size) {
    final leafPaint = Paint()
      ..color = const Color(0xFF476629)
      ..style = PaintingStyle.fill;

    final veinPaint = Paint()
      ..color = const Color(0xFFC4D64D)
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    final lesionPaint = Paint()
      ..color = const Color(0xFFB56A28)
      ..style = PaintingStyle.fill;

    final path = Path();
    path.moveTo(size.width * 0.5, size.height * 0.1);
    path.quadraticBezierTo(size.width * 0.9, size.height * 0.35, size.width * 0.5, size.height * 0.9);
    path.quadraticBezierTo(size.width * 0.1, size.height * 0.35, size.width * 0.5, size.height * 0.1);
    path.close();

    canvas.drawPath(path, leafPaint);

    // Main vein
    canvas.drawLine(
      Offset(size.width * 0.5, size.height * 0.1),
      Offset(size.width * 0.5, size.height * 0.9),
      veinPaint,
    );

    // Lateral veins
    canvas.drawLine(Offset(size.width * 0.5, size.height * 0.3), Offset(size.width * 0.75, size.height * 0.45), veinPaint);
    canvas.drawLine(Offset(size.width * 0.5, size.height * 0.3), Offset(size.width * 0.25, size.height * 0.45), veinPaint);
    canvas.drawLine(Offset(size.width * 0.5, size.height * 0.5), Offset(size.width * 0.8, size.height * 0.65), veinPaint);
    canvas.drawLine(Offset(size.width * 0.5, size.height * 0.5), Offset(size.width * 0.2, size.height * 0.65), veinPaint);

    // Blight lesion spots
    canvas.drawCircle(Offset(size.width * 0.4, size.height * 0.4), 18, lesionPaint);
    canvas.drawCircle(Offset(size.width * 0.65, size.height * 0.55), 14, lesionPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
