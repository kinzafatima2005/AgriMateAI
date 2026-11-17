import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../widgets/decision_disclaimer_banner.dart';
import '../../services/scan_history_service.dart';

class ScanResultScreen extends StatefulWidget {
  final bool isLowConfidenceDemo;
  final String cropName;
  final String userDescription;

  const ScanResultScreen({
    super.key,
    this.isLowConfidenceDemo = false,
    this.cropName = 'Potato (آلو)',
    this.userDescription = 'کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں',
  });

  @override
  State<ScanResultScreen> createState() => _ScanResultScreenState();
}

class _ScanResultScreenState extends State<ScanResultScreen> {
  bool _showGradCam = true;
  double _overlayOpacity = 0.65;
  bool _isPlayingAudio = false;

  late String _diseaseName;
  late String _urduName;
  late double _confidence;
  late String _citationManual;
  late String _adviceText;

  @override
  void initState() {
    super.initState();
    _confidence = widget.isLowConfidenceDemo ? 0.635 : 0.938;

    if (widget.cropName.contains('Tomato')) {
      _diseaseName = 'Tomato Early Blight';
      _urduName = 'ٹماٹر کا اگیتا جھلساؤ';
      _citationManual = 'Punjab_Agri_Tomato_Production_and_Pathology_Manual_2024.pdf (p.1)';
      _adviceText = (
        '1. Blight Action: Spray Chlorothalonil 75 WP @ 500g/acre or Difenoconazole @ 125ml/acre.\n'
        '2. Farmer Symptom Action ("${widget.userDescription}"): Spray Emamectin Benzoate 1.9 EC @ 200ml/acre to control fruit borer caterpillars, and prune lower dried foliage.'
      );
    } else {
      _diseaseName = 'Potato Late Blight (Pachita Jhalsao)';
      _urduName = 'آلو کا پچھیتا جھلساؤ';
      _citationManual = 'NARC_Potato_Production_and_Blight_Guide_2024.pdf (p.1 & p.2)';
      _adviceText = (
        '1. Blight Action: Apply Metalaxyl + Mancozeb (Ridomil Gold) @ 250g/100L water or Mandipropamid (Revus) @ 200ml/acre.\n'
        '2. Farmer Symptom Action ("${widget.userDescription}"): For aphid/cutworm keera attack, add Flonicamid @ 60g/acre. Ensure lower foliage drenched.'
      );
    }

    _saveConsolidatedRecord();
  }

  void _saveConsolidatedRecord() {
    final item = LocalScanItem(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      crop: widget.cropName,
      diseaseName: _diseaseName,
      urduName: _urduName,
      confidence: _confidence,
      severity: widget.isLowConfidenceDemo ? 'PENDING_REVIEW' : 'CRITICAL',
      timestamp: DateTime.now().toLocal().toString().split('.')[0],
      isSynced: true,
      needsReview: widget.isLowConfidenceDemo,
    );
    ScanHistoryService().saveScan(item);
  }

  void _toggleAudioPlayback() {
    setState(() {
      _isPlayingAudio = !_isPlayingAudio;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          _isPlayingAudio
              ? '🔊 Playing Urdu voice advice for illiterate farmer...'
              : '⏹ Audio playback stopped.',
        ),
        duration: const Duration(seconds: 2),
        backgroundColor: AgriColors.backgroundDark,
      ),
    );
  }

  void _showWhyThisResultSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: AgriColors.backgroundDark,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.psychology_rounded, color: AgriColors.accentYellow, size: 24),
                        SizedBox(width: 8),
                        Text(
                          'Grad-CAM Explainability',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AgriColors.textWhite,
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
                const SizedBox(height: 12),
                Text(
                  'How AgriMate Made This Multimodal Prediction:',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: AgriColors.accentYellow,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '1. Red/Orange Focal Zones: The MobileNetV2 final convolutional layer isolated concentric necrotic lesions on the ${widget.cropName} leaf blade.\n'
                  '2. Farmer Context Integration: The farmer\'s observation ("${widget.userDescription}") confirmed simultaneous insect pest activity and foliage drying.\n'
                  '3. Grounded Verification: Fused visual + textual parameters queried certified compendia ($ _citationManual).',
                  style: const TextStyle(color: AgriColors.textSecondary, fontSize: 13, height: 1.45),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AgriColors.accentYellow,
                    foregroundColor: AgriColors.backgroundDark,
                    minimumSize: const Size.fromHeight(44),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  ),
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('Understood (سمجھ آ گئی)', style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      backgroundColor: AgriColors.backgroundDark,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Multimodal Diagnostic Report',
          style: textTheme.titleMedium?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Low-Confidence Warning Banner (<75%)
            if (widget.isLowConfidenceDemo)
              Container(
                margin: const EdgeInsets.only(bottom: 16),
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: Colors.amber.shade900.withOpacity(0.4),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.amber.shade400, width: 1.2),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.assignment_late_rounded, color: Colors.amber, size: 24),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text(
                            'Low Confidence Auto-Flagged (<75%)',
                            style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 13),
                          ),
                          SizedBox(height: 3),
                          Text(
                            'Confidence is 63.5%. This multimodal scan has been automatically dispatched to the Punjab Agricultural Extension Expert Queue for agronomist verification.',
                            style: TextStyle(color: Colors.white70, fontSize: 11.5, height: 1.35),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

            // Leaf Heatmap Canvas Card
            Container(
              height: 240,
              width: double.infinity,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(28),
                color: const Color(0xFF233814),
                border: Border.all(color: Colors.white12),
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Base Leaf Graphic
                  CustomPaint(
                    size: const Size(200, 220),
                    painter: LeafHeatmapPainter(showHeatmap: _showGradCam, opacity: _overlayOpacity),
                  ),

                  // Grad-CAM Controls Overlay
                  Positioned(
                    top: 12,
                    right: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black54,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Text('Grad-CAM', style: TextStyle(color: Colors.white, fontSize: 11)),
                          const SizedBox(width: 4),
                          Switch(
                            value: _showGradCam,
                            activeColor: AgriColors.accentYellow,
                            materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                            onChanged: (val) => setState(() => _showGradCam = val),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Diagnostic Summary Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AgriColors.surfaceGlass,
                borderRadius: BorderRadius.circular(28),
                border: Border.all(color: Colors.white12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        widget.cropName.toUpperCase(),
                        style: const TextStyle(color: AgriColors.textSecondary, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: widget.isLowConfidenceDemo ? Colors.amber.shade400 : AgriColors.accentYellow,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Text(
                          '${(_confidence * 100).toStringAsFixed(1)}% Confidence',
                          style: const TextStyle(color: AgriColors.backgroundDark, fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(
                    _diseaseName,
                    style: textTheme.headlineSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    _urduName,
                    style: const TextStyle(color: AgriColors.accentYellow, fontSize: 15, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 14),

                  // Farmer Spoken/Typed Observation Display
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.black26,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.white12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: const [
                            Icon(Icons.record_voice_over_rounded, color: AgriColors.accentYellow, size: 16),
                            SizedBox(width: 6),
                            Text(
                              'Farmer Spoken Note (کسان کی آواز):',
                              style: TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 4),
                        Text(
                          '"${widget.userDescription}"',
                          style: const TextStyle(color: Colors.white, fontSize: 13, fontStyle: FontStyle.italic),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Fused RAG Advisory
                  const Text(
                    'Multimodal Integrated Treatment (متحدہ زرعی مشورہ):',
                    style: TextStyle(color: AgriColors.textWhite, fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    _adviceText,
                    style: const TextStyle(color: AgriColors.textSecondary, fontSize: 12.5, height: 1.4),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      const Icon(Icons.menu_book_rounded, color: AgriColors.accentYellow, size: 14),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          'Citation: $_citationManual',
                          style: const TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.w600),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Audio Playback Button (TTS) & Why This Result Button
                  Row(
                    children: [
                      // Text-to-Speech Button
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: _isPlayingAudio ? Colors.amber : AgriColors.accentYellow,
                            foregroundColor: AgriColors.backgroundDark,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                          ),
                          icon: Icon(_isPlayingAudio ? Icons.stop_rounded : Icons.volume_up_rounded),
                          label: Text(
                            _isPlayingAudio ? 'Stop Voice' : 'Suniye (آواز سنیں)',
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                          ),
                          onPressed: _toggleAudioPlayback,
                        ),
                      ),
                      const SizedBox(width: 8),
                      // Explainability Modal Button
                      OutlinedButton.icon(
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Colors.white24),
                          padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 14),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                        ),
                        icon: const Icon(Icons.help_outline_rounded, size: 16),
                        label: const Text('Explain', style: TextStyle(fontSize: 12)),
                        onPressed: _showWhyThisResultSheet,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // Consolidated Record Saved Badge
            Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Text(
                  '✓ Photo, voice text, prediction and advice saved as 1 record',
                  style: TextStyle(color: AgriColors.textSecondary, fontSize: 11),
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Regulatory Decision-Support Disclaimer
            const DecisionDisclaimerBanner(),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}

class LeafHeatmapPainter extends CustomPainter {
  final bool showHeatmap;
  final double opacity;
  LeafHeatmapPainter({required this.showHeatmap, required this.opacity});

  @override
  void paint(Canvas canvas, Size size) {
    final leafPaint = Paint()
      ..color = const Color(0xFF476629)
      ..style = PaintingStyle.fill;

    final veinPaint = Paint()
      ..color = const Color(0xFF88A84B)
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke;

    final path = Path();
    path.moveTo(size.width * 0.5, size.height * 0.08);
    path.quadraticBezierTo(size.width * 0.9, size.height * 0.35, size.width * 0.5, size.height * 0.92);
    path.quadraticBezierTo(size.width * 0.1, size.height * 0.35, size.width * 0.5, size.height * 0.08);
    path.close();

    canvas.drawPath(path, leafPaint);
    canvas.drawLine(Offset(size.width * 0.5, size.height * 0.08), Offset(size.width * 0.5, size.height * 0.92), veinPaint);

    if (showHeatmap) {
      // Draw Grad-CAM thermal heatmap circle
      final gradPaint = Paint()
        ..shader = RadialGradient(
          colors: [
            Colors.red.withOpacity(opacity),
            Colors.orange.withOpacity(opacity * 0.8),
            Colors.yellow.withOpacity(opacity * 0.5),
            Colors.transparent,
          ],
          stops: const [0.0, 0.4, 0.7, 1.0],
        ).createShader(Rect.fromCircle(center: Offset(size.width * 0.45, size.height * 0.42), radius: 55));

      canvas.drawCircle(Offset(size.width * 0.45, size.height * 0.42), 55, gradPaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
