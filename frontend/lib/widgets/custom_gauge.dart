import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SemicircularGauge extends StatelessWidget {
  final double progress; // 0.0 to 1.0
  final double size;

  const SemicircularGauge({
    super.key,
    this.progress = 0.72,
    this.size = 110.0,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size * 0.58),
      painter: _GaugePainter(progress: progress),
    );
  }
}

class _GaugePainter extends CustomPainter {
  final double progress;

  _GaugePainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height);
    final radius = size.width / 2 - 10;

    // Track background arc (subtle white opacity)
    final trackPaint = Paint()
      ..color = AgriColors.divider
      ..strokeWidth = 9.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    // Gauge active yellow arc (~#F4F23A)
    final activePaint = Paint()
      ..color = AgriColors.accentYellow
      ..strokeWidth = 9.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    // Semicircle from PI (left) to 2*PI (right)
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      math.pi,
      false,
      trackPaint,
    );

    // Active progress arc
    final sweepAngle = math.pi * progress.clamp(0.0, 1.0);
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      sweepAngle,
      false,
      activePaint,
    );

    // White Knob Indicator
    final knobAngle = math.pi + sweepAngle;
    final knobX = center.dx + radius * math.cos(knobAngle);
    final knobY = center.dy + radius * math.sin(knobAngle);

    final knobPaint = Paint()
      ..color = AgriColors.textWhite
      ..style = PaintingStyle.fill;

    final knobShadow = Paint()
      ..color = Colors.black26
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);

    canvas.drawCircle(Offset(knobX, knobY), 7.5, knobShadow);
    canvas.drawCircle(Offset(knobX, knobY), 6.5, knobPaint);
  }

  @override
  bool shouldRepaint(covariant _GaugePainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}

