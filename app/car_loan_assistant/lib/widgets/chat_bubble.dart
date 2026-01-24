// Chat Bubble Widget

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../config/theme.dart';
import '../models/negotiation.dart';

class ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const ChatBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: EdgeInsets.only(
          top: 4,
          bottom: 4,
          left: isUser ? 50 : 0,
          right: isUser ? 0 : 50,
        ),
        child: Column(
          crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: isUser ? AppTheme.primaryColor : Colors.grey[200],
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(16),
                  topRight: const Radius.circular(16),
                  bottomLeft: isUser ? const Radius.circular(16) : Radius.zero,
                  bottomRight: isUser ? Radius.zero : const Radius.circular(16),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 5,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildMessageContent(context, isUser),
                ],
              ),
            ),
            if (!isUser) ...[
              const SizedBox(height: 4),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  InkWell(
                    onTap: () {
                      Clipboard.setData(ClipboardData(text: message.content));
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Copied to clipboard'),
                          duration: Duration(seconds: 1),
                        ),
                      );
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(4),
                      child: Icon(
                        Icons.copy,
                        size: 14,
                        color: Colors.grey[500],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildMessageContent(BuildContext context, bool isUser) {
    final content = message.content;
    
    // Parse markdown-like formatting
    final lines = content.split('\n');
    final widgets = <Widget>[];
    
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      
      // Headers (##)
      if (line.startsWith('**') && line.endsWith('**')) {
        widgets.add(Text(
          line.replaceAll('**', ''),
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: isUser ? Colors.white : AppTheme.textPrimary,
            fontSize: 16,
          ),
        ));
      }
      // Bullet points
      else if (line.startsWith('•') || line.startsWith('✅') || 
               line.startsWith('🎯') || line.startsWith('1️⃣') ||
               line.startsWith('2️⃣') || line.startsWith('3️⃣') ||
               line.startsWith('4️⃣') || line.startsWith('5️⃣')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(left: 8, top: 4),
          child: Text(
            line,
            style: TextStyle(
              color: isUser ? Colors.white : AppTheme.textPrimary,
            ),
          ),
        ));
      }
      // Divider line
      else if (line.startsWith('---')) {
        widgets.add(const Divider());
      }
      // Regular text
      else {
        widgets.add(Text(
          line,
          style: TextStyle(
            color: isUser ? Colors.white : AppTheme.textPrimary,
          ),
        ));
      }
      
      // Add spacing between lines
      if (i < lines.length - 1 && line.isNotEmpty) {
        widgets.add(const SizedBox(height: 4));
      }
    }
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: widgets,
    );
  }
}
