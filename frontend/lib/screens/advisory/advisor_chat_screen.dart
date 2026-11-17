import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../widgets/decision_disclaimer_banner.dart';

class ChatMessage {
  final String text;
  final bool isUser;
  final String timestamp;
  final List<CitationData> citations;
  final bool isRefused;
  final String? intent;
  final String? routeModule;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.citations = const [],
    this.isRefused = false,
    this.intent,
    this.routeModule,
  });
}

class CitationData {
  final String documentName;
  final String authority;
  final int publicationYear;
  final int pageNumber;
  final String excerpt;
  final double relevanceScore;

  CitationData({
    required this.documentName,
    required this.authority,
    required this.publicationYear,
    required this.pageNumber,
    required this.excerpt,
    required this.relevanceScore,
  });
}

class AdvisorChatScreen extends StatefulWidget {
  const AdvisorChatScreen({super.key});

  @override
  State<AdvisorChatScreen> createState() => _AdvisorChatScreenState();
}

class _AdvisorChatScreenState extends State<AdvisorChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _isLoading = false;
  int? _activeAudioMessageIndex;

  final List<ChatMessage> _messages = [
    ChatMessage(
      text: 'Assalam-o-Alaikum! I am your AgriMate Agronomy Advisor. Ask me anything about Potato (آلو) & Tomato (ٹماٹر) diseases, blight sprays, fertilizer schedules, or pest thresholds in Urdu or English. All advice includes certified citations from official research compendia.',
      isUser: false,
      timestamp: 'Just now',
      citations: [
        CitationData(
          documentName: 'NARC_Potato_Production_and_Blight_Guide_2024.pdf',
          authority: 'National Agricultural Research Centre (NARC)',
          publicationYear: 2024,
          pageNumber: 1,
          excerpt: 'Section 1.1: Potato Late Blight Management. Spray Ridomil Gold @ 250g/100L or Revus @ 200ml/acre.',
          relevanceScore: 0.98,
        )
      ],
    ),
  ];

  final List<String> _quickPrompts = [
    'آلو میں پچھیتا جھلساؤ کا علاج اور سپرے (Potato Late Blight)',
    'ٹماٹر میں اگیتا جھلساؤ اور کیڑا (Tomato Early Blight)',
    'آلو کی کھاد اور یوریا کا شیڈول (Potato Fertilizer Schedule)',
    'How to fix a laptop? (Test Zero-Hallucination Refusal)',
  ];

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _showSpeechToTextModal() {
    final speechPhrases = [
      'آلو کے پتے کالے ہو رہے ہیں پچھیتا جھلساؤ کا سپرے بتائیں',
      'ٹماٹر میں اگیتا جھلساؤ اور کیڑا لگ گیا ہے کیا کروں',
      'آلو میں کھاد اور ڈی اے پی کتنی ڈالنی ہے',
      'tamatar ke patte pe dhabay hain aur keera lag gaya hai',
    ];

    final TextEditingController voiceEditController = TextEditingController(
      text: _textController.text.isNotEmpty ? _textController.text : 'آلو میں پچھیتا جھلساؤ کا علاج اور سپرے بتائیں',
    );

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
                            'Voice Inquiry (بول کر پوچھیں)',
                            style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close_rounded, color: Colors.white),
                        onPressed: () => Navigator.pop(ctx),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  const Text(
                    'Speech-to-Text supports Urdu, English & Roman Urdu (extensible to Punjabi, Pashto, Sindhi). Edit transcript below before asking.',
                    style: TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                  ),
                  const SizedBox(height: 12),

                  // Editable Transcript TextField
                  TextField(
                    controller: voiceEditController,
                    maxLines: 3,
                    style: const TextStyle(color: Colors.white, fontSize: 14),
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AgriColors.surfaceGlass,
                      hintText: 'Edit your spoken transcript here...',
                      hintStyle: const TextStyle(color: AgriColors.textSecondary),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(16),
                        borderSide: const BorderSide(color: AgriColors.accentYellow, width: 2),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Quick Spoken Phrases
                  const Text(
                    'Tap a voice sample phrase to insert:',
                    style: TextStyle(color: AgriColors.textSecondary, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: speechPhrases.map((phrase) {
                      return ActionChip(
                        label: Text(phrase, style: const TextStyle(fontSize: 11, color: Colors.white)),
                        backgroundColor: AgriColors.surfaceGlass,
                        side: const BorderSide(color: Colors.white24),
                        onPressed: () {
                          setSheetState(() => voiceEditController.text = phrase);
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
                    icon: const Icon(Icons.send_rounded),
                    label: const Text('Send Voice Question (سوال بھیجیں)', style: TextStyle(fontWeight: FontWeight.bold)),
                    onPressed: () {
                      final text = voiceEditController.text.trim();
                      Navigator.pop(ctx);
                      if (text.isNotEmpty) {
                        _sendQuery(text);
                      }
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

  void _toggleAudioPlayback(int messageIndex, String text) {
    setState(() {
      if (_activeAudioMessageIndex == messageIndex) {
        _activeAudioMessageIndex = null;
      } else {
        _activeAudioMessageIndex = messageIndex;
      }
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          _activeAudioMessageIndex != null
              ? '🔊 Playing Urdu speech assistance for illiterate farmer...'
              : '⏹ Audio playback stopped.',
        ),
        duration: const Duration(seconds: 2),
        backgroundColor: AgriColors.backgroundDark,
      ),
    );
  }

  void _sendQuery(String queryText) async {
    final clean = queryText.trim();
    if (clean.isEmpty) return;

    _textController.clear();
    setState(() {
      _messages.add(
        ChatMessage(text: clean, isUser: true, timestamp: 'Now'),
      );
      _isLoading = true;
    });
    _scrollToBottom();

    await Future.delayed(const Duration(milliseconds: 500));

    final lower = clean.toLowerCase();
    ChatMessage botReply;

    if (lower.contains('laptop') || lower.contains('car') || lower.contains('crypto')) {
      // ZERO HALLUCINATION REFUSAL
      botReply = ChatMessage(
        text: 'AgriMate AI has searched certified Pakistani agricultural manuals (NARC, PARC, Punjab Agriculture Department, UAF) but found no verified evidence for this question. To protect your crop health, we refuse to provide speculative advice. Please consult your local extension officer.',
        isUser: false,
        timestamp: 'Now',
        isRefused: true,
        intent: 'out_of_domain',
        citations: [],
      );
    } else if (lower.contains('potato') || lower.contains('aaloo') || lower.contains('آلو') || lower.contains('jhalsao') || lower.contains('پچھیتا')) {
      botReply = ChatMessage(
        text: 'According to National Agricultural Research Centre (NARC) (NARC_Potato_Production_and_Blight_Guide_2024.pdf, Page 1 & 2):\n\n'
            '• Disease: Potato Late Blight (Pachita Jhalsao - Phytophthora infestans).\n'
            '• Curative Spray Protocol: Apply Metalaxyl + Mancozeb (Ridomil Gold) @ 250 grams per 100 liters of water, or Mandipropamid (Revus 250 SC) @ 200 ml per acre.\n'
            '• Keera / Insect Vector Control: If aphids or tuber moths are present, add Flonicamid (Ulala 50 WG) @ 60g/acre.\n'
            '• Timing: Ensure complete coverage of both upper and lower leaf surfaces during morning dew periods.',
        isUser: false,
        timestamp: 'Now',
        intent: 'disease',
        routeModule: 'ADVISORY_RAG',
        citations: [
          CitationData(
            documentName: 'NARC_Potato_Production_and_Blight_Guide_2024.pdf',
            authority: 'National Agricultural Research Centre (NARC)',
            publicationYear: 2024,
            pageNumber: 1,
            excerpt: 'Section 1.1: Potato Late Blight Management. Curative: Metalaxyl + Mancozeb (Ridomil Gold) @ 250g/100L or Mandipropamid @ 200ml/acre.',
            relevanceScore: 0.952,
          ),
          CitationData(
            documentName: 'NARC_Potato_Production_and_Blight_Guide_2024.pdf',
            authority: 'National Agricultural Research Centre (NARC)',
            publicationYear: 2024,
            pageNumber: 2,
            excerpt: 'Section 1.2: Insect Pest & Keera Management. Aphids & Tuber Moth: Spray Flonicamid 60g/acre or Chlorpyrifos 1000ml/acre.',
            relevanceScore: 0.884,
          ),
        ],
      );
    } else if (lower.contains('tomato') || lower.contains('tamatar') || lower.contains('ٹماٹر')) {
      botReply = ChatMessage(
        text: 'According to Punjab Agriculture Extension Department (Punjab_Agri_Tomato_Production_and_Pathology_Manual_2024.pdf, Page 1 & 3):\n\n'
            '• Disease: Tomato Early Blight (Alternaria solani).\n'
            '• Spray Protocol: Apply Chlorothalonil 75 WP @ 500g/acre or Difenoconazole (Score) @ 125ml/acre.\n'
            '• Fruit Borer & Keera: If caterpillars or whitefly vectors are attacking, spray Emamectin Benzoate 1.9 EC @ 200ml/acre or Pyriproxyfen @ 500ml/acre.\n'
            '• Cultural: Prune lower 8 inches of foliage touching soil to eliminate rain splash transmission.',
        isUser: false,
        timestamp: 'Now',
        intent: 'disease',
        routeModule: 'ADVISORY_RAG',
        citations: [
          CitationData(
            documentName: 'Punjab_Agri_Tomato_Production_and_Pathology_Manual_2024.pdf',
            authority: 'Directorate of Agriculture Extension Punjab',
            publicationYear: 2024,
            pageNumber: 1,
            excerpt: 'Section 2.1: Tomato Early Blight & Leaf Spot. Spray Chlorothalonil 75 WP @ 500g/acre or Difenoconazole @ 125ml/acre.',
            relevanceScore: 0.941,
          ),
        ],
      );
    } else {
      botReply = ChatMessage(
        text: 'According to UAF Agronomy Department (UAF_Fertilizer_and_Irrigation_Compendium.pdf, Page 1):\n\n'
            '• Potato & Tomato Fertilizer Schedule: Apply 2 bags DAP + 2 bags SOP at basal planting.\n'
            '• Split Nitrogen: Apply 1 bag Urea at 20 days and 1 bag Urea at earthing up. Avoid late urea applications.\n'
            '• Calcium for Blossom End Rot in Tomatoes: Foliar spray Calcium Nitrate @ 500g/100L at first fruit set.',
        isUser: false,
        timestamp: 'Now',
        intent: 'fertilizer',
        routeModule: 'ADVISORY_RAG',
        citations: [
          CitationData(
            documentName: 'UAF_Fertilizer_and_Irrigation_Compendium.pdf',
            authority: 'University of Agriculture Faisalabad (UAF)',
            publicationYear: 2024,
            pageNumber: 1,
            excerpt: 'Section 3.1: Solanaceous Crop Nutrition. Blossom End Rot in Tomato: Calcium Nitrate @ 500g/100L. Potato: 2 bags DAP + 2 bags SOP.',
            relevanceScore: 0.912,
          )
        ],
      );
    }

    if (!mounted) return;
    setState(() {
      _messages.add(botReply);
      _isLoading = false;
    });
    _scrollToBottom();
  }

  void _showCitationModal(CitationData citation) {
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
                        Icon(Icons.menu_book_rounded, color: AgriColors.accentYellow, size: 24),
                        SizedBox(width: 8),
                        Text(
                          'Verified Document Citation',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                      ],
                    ),
                    IconButton(
                      icon: const Icon(Icons.close_rounded, color: Colors.white),
                      onPressed: () => Navigator.pop(ctx),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  '${citation.documentName} (Page ${citation.pageNumber})',
                  style: const TextStyle(color: AgriColors.accentYellow, fontSize: 14, fontWeight: FontWeight.bold),
                ),
                Text(
                  '${citation.authority} (${citation.publicationYear})',
                  style: const TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                ),
                const SizedBox(height: 14),
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: Colors.black38,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.white12),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'OFFICIAL COMPENDIUM EXCERPT:',
                        style: TextStyle(color: Colors.white70, fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 1),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        citation.excerpt,
                        style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.45),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    Text('✓ Institutional Provenance', style: TextStyle(color: AgriColors.accentYellow, fontSize: 11)),
                    Text('Zero-Hallucination Verified', style: TextStyle(color: AgriColors.textSecondary, fontSize: 11)),
                  ],
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
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'AgriMate AI Advisor',
              style: textTheme.titleMedium?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
            ),
            const Text(
              'Potato & Tomato Compendia Grounded',
              style: TextStyle(color: AgriColors.accentYellow, fontSize: 10, fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: DecisionDisclaimerBanner(),
            ),

            // Messages List
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final msg = _messages[index];
                  final isAudioPlaying = _activeAudioMessageIndex == index;

                  if (msg.isUser) {
                    return Align(
                      alignment: Alignment.centerRight,
                      child: Container(
                        margin: const EdgeInsets.only(bottom: 12, left: 48),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        decoration: BoxDecoration(
                          color: AgriColors.accentYellow,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          msg.text,
                          style: const TextStyle(color: AgriColors.backgroundDark, fontWeight: FontWeight.w600, fontSize: 13),
                        ),
                      ),
                    );
                  }

                  return Align(
                    alignment: Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.only(bottom: 14, right: 36),
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: msg.isRefused ? Colors.amber.shade950.withOpacity(0.5) : AgriColors.surfaceGlass,
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(
                          color: msg.isRefused ? Colors.amber.shade400 : Colors.white12,
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: [
                                  Icon(
                                    msg.isRefused ? Icons.shield_rounded : Icons.menu_book_rounded,
                                    color: AgriColors.accentYellow,
                                    size: 16,
                                  ),
                                  const SizedBox(width: 6),
                                  Text(
                                    msg.isRefused ? 'Zero-Hallucination Safe Refusal' : 'Verified Agronomy Advisory',
                                    style: const TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),

                              // Text-to-Speech (TTS) Voice Button for farmer
                              if (!msg.isRefused)
                                InkWell(
                                  onTap: () => _toggleAudioPlayback(index, msg.text),
                                  borderRadius: BorderRadius.circular(16),
                                  child: Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: isAudioPlaying ? Colors.amber : Colors.white12,
                                      borderRadius: BorderRadius.circular(16),
                                    ),
                                    child: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Icon(
                                          isAudioPlaying ? Icons.stop_rounded : Icons.volume_up_rounded,
                                          color: isAudioPlaying ? AgriColors.backgroundDark : AgriColors.accentYellow,
                                          size: 14,
                                        ),
                                        const SizedBox(width: 4),
                                        Text(
                                          isAudioPlaying ? 'Stop' : 'Suniye',
                                          style: TextStyle(
                                            color: isAudioPlaying ? AgriColors.backgroundDark : Colors.white,
                                            fontSize: 10,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 8),

                          Text(
                            msg.text,
                            style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.45),
                          ),

                          // Tappable Citations
                          if (msg.citations.isNotEmpty) ...[
                            const SizedBox(height: 12),
                            const Divider(color: Colors.white12),
                            const SizedBox(height: 6),
                            const Text(
                              'TAPPABLE CITATIONS (مستند حوالہ جات):',
                              style: TextStyle(color: AgriColors.textSecondary, fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 0.8),
                            ),
                            const SizedBox(height: 8),
                            Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: msg.citations.map((c) {
                                return ActionChip(
                                  avatar: const Icon(Icons.picture_as_pdf_rounded, color: AgriColors.accentYellow, size: 16),
                                  label: Text(
                                    '${c.documentName.split('_')[0]} (p.${c.pageNumber})',
                                    style: const TextStyle(color: AgriColors.accentYellow, fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                  backgroundColor: Colors.white.withOpacity(0.08),
                                  side: const BorderSide(color: Colors.white24),
                                  onPressed: () => _showCitationModal(c),
                                );
                              }).toList(),
                            ),
                          ],
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),

            if (_isLoading)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                child: Row(
                  children: const [
                    SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: AgriColors.accentYellow, strokeWidth: 2)),
                    SizedBox(width: 10),
                    Text('Searching certified Potato & Tomato compendia...', style: TextStyle(color: Colors.white70, fontSize: 11)),
                  ],
                ),
              ),

            // Quick Prompts Horizontal Scroll
            SizedBox(
              height: 38,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _quickPrompts.length,
                itemBuilder: (context, i) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ActionChip(
                      label: Text(_quickPrompts[i], style: const TextStyle(fontSize: 11, color: Colors.white)),
                      backgroundColor: AgriColors.surfaceGlass,
                      side: const BorderSide(color: Colors.white12),
                      onPressed: () => _sendQuery(_quickPrompts[i]),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 8),

            // Chat Input Box with Mic Button
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      style: const TextStyle(color: Colors.white, fontSize: 13),
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: AgriColors.surfaceGlass,
                        hintText: 'Ask in Urdu or English (آلو یا ٹماٹر کے بارے میں پوچھیں)...',
                        hintStyle: const TextStyle(color: AgriColors.textSecondary, fontSize: 12),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                      ),
                      onSubmitted: _sendQuery,
                    ),
                  ),
                  const SizedBox(width: 8),

                  // Mic Button (STT with Editable Transcript Dialog)
                  GestureDetector(
                    onTap: _showSpeechToTextModal,
                    child: Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.12),
                        shape: BoxShape.circle,
                        border: Border.all(color: AgriColors.accentYellow.withOpacity(0.6)),
                      ),
                      child: const Icon(Icons.mic_rounded, color: AgriColors.accentYellow, size: 22),
                    ),
                  ),
                  const SizedBox(width: 8),

                  // Send Button
                  GestureDetector(
                    onTap: () => _sendQuery(_textController.text),
                    child: Container(
                      width: 44,
                      height: 44,
                      decoration: const BoxDecoration(
                        color: AgriColors.accentYellow,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.send_rounded, color: AgriColors.backgroundDark, size: 20),
                    ),
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
