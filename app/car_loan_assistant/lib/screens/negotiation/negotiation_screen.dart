// Negotiation Assistant Screen

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../../config/theme.dart';
import '../../providers/contract_provider.dart';
import '../../providers/negotiation_provider.dart';
import '../../models/negotiation.dart';
import '../../widgets/chat_bubble.dart';

class NegotiationScreen extends StatefulWidget {
  const NegotiationScreen({super.key});

  @override
  State<NegotiationScreen> createState() => _NegotiationScreenState();
}

class _NegotiationScreenState extends State<NegotiationScreen> with SingleTickerProviderStateMixin {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    
    // Initialize the negotiation provider with current contract
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final contractProvider = context.read<ContractProvider>();
      context.read<NegotiationProvider>().initialize(contractProvider.currentContract);
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Negotiation Assistant'),
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.white,
          tabs: const [
            Tab(icon: Icon(Icons.chat), text: 'Chat'),
            Tab(icon: Icon(Icons.lightbulb), text: 'Tips'),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<NegotiationProvider>().clearChat();
            },
          ),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildChatTab(),
          _buildTipsTab(),
        ],
      ),
    );
  }
  
  Widget _buildChatTab() {
    return Consumer<NegotiationProvider>(
      builder: (context, provider, child) {
        return Column(
          children: [
            // Quick Actions
            _buildQuickActions(),
            
            // Chat Messages
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(16),
                itemCount: provider.messages.length + (provider.isTyping ? 1 : 0),
                itemBuilder: (context, index) {
                  if (index == provider.messages.length && provider.isTyping) {
                    return const TypingIndicator();
                  }
                  return ChatBubble(message: provider.messages[index]);
                },
              ),
            ),
            
            // Input Area
            _buildInputArea(provider),
          ],
        );
      },
    );
  }
  
  Widget _buildQuickActions() {
    final actions = [
      ('📝 Interest Tips', 'Tell me about negotiating interest rates'),
      ('✉️ Draft Email', 'Write an email to the dealer'),
      ('❓ Questions', 'What questions should I ask?'),
    ];
    
    return Container(
      height: 50,
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemCount: actions.length,
        separatorBuilder: (_, __) => const SizedBox(width: 8),
        itemBuilder: (context, index) {
          return ActionChip(
            label: Text(actions[index].$1),
            onPressed: () {
              _sendQuickMessage(actions[index].$2);
            },
          );
        },
      ),
    );
  }
  
  Widget _buildInputArea(NegotiationProvider provider) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: _messageController,
                decoration: InputDecoration(
                  hintText: 'Ask about your contract...',
                  filled: true,
                  fillColor: Colors.grey[100],
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 12,
                  ),
                ),
                textInputAction: TextInputAction.send,
                onSubmitted: (_) => _sendMessage(),
              ),
            ),
            const SizedBox(width: 12),
            FloatingActionButton(
              onPressed: _sendMessage,
              mini: true,
              backgroundColor: AppTheme.primaryColor,
              child: const Icon(Icons.send, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildTipsTab() {
    return Consumer<NegotiationProvider>(
      builder: (context, provider, child) {
        if (provider.negotiationPoints.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  FontAwesomeIcons.lightbulb,
                  size: 64,
                  color: Colors.grey[400],
                ),
                const SizedBox(height: 16),
                const Text(
                  'No specific tips yet',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(
                  'Upload a contract to get personalized negotiation tips',
                  style: TextStyle(color: Colors.grey[600]),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          );
        }
        
        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: provider.negotiationPoints.length,
          itemBuilder: (context, index) {
            return _buildTipCard(provider.negotiationPoints[index]);
          },
        );
      },
    );
  }
  
  Widget _buildTipCard(NegotiationPoint point) {
    Color priorityColor;
    IconData priorityIcon;
    
    switch (point.priority) {
      case NegotiationPriority.high:
        priorityColor = AppTheme.errorColor;
        priorityIcon = Icons.priority_high;
        break;
      case NegotiationPriority.medium:
        priorityColor = AppTheme.warningColor;
        priorityIcon = Icons.remove;
        break;
      case NegotiationPriority.low:
        priorityColor = AppTheme.successColor;
        priorityIcon = Icons.keyboard_arrow_down;
        break;
    }
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: priorityColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(priorityIcon, color: priorityColor, size: 20),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    point.title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: priorityColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    point.priority.name.toUpperCase(),
                    style: TextStyle(
                      color: priorityColor,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              point.description,
              style: TextStyle(
                color: Colors.grey[700],
              ),
            ),
            if (point.suggestedAction != null) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: AppTheme.primaryColor.withOpacity(0.2),
                  ),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(
                      Icons.lightbulb_outline,
                      size: 18,
                      color: AppTheme.primaryColor,
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        point.suggestedAction!,
                        style: const TextStyle(
                          color: AppTheme.primaryColor,
                          fontSize: 13,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton.icon(
                  onPressed: () {
                    Clipboard.setData(ClipboardData(
                      text: '${point.title}\n${point.description}\n${point.suggestedAction ?? ''}',
                    ));
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Copied to clipboard')),
                    );
                  },
                  icon: const Icon(Icons.copy, size: 16),
                  label: const Text('Copy'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
  
  void _sendMessage() {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;
    
    context.read<NegotiationProvider>().sendMessage(text);
    _messageController.clear();
    
    // Scroll to bottom after message is added
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }
  
  void _sendQuickMessage(String message) {
    _messageController.text = message;
    _sendMessage();
  }
}

class TypingIndicator extends StatelessWidget {
  const TypingIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildDot(0),
            _buildDot(1),
            _buildDot(2),
          ],
        ),
      ),
    );
  }
  
  Widget _buildDot(int index) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: 1),
      duration: Duration(milliseconds: 600 + (index * 200)),
      builder: (context, value, child) {
        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 2),
          width: 8,
          height: 8,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.grey[500],
          ),
        );
      },
    );
  }
}
