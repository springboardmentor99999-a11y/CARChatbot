// Negotiation Model

class NegotiationPoint {
  final String title;
  final String description;
  final NegotiationPriority priority;
  final String? suggestedAction;

  NegotiationPoint({
    required this.title,
    required this.description,
    this.priority = NegotiationPriority.medium,
    this.suggestedAction,
  });

  factory NegotiationPoint.fromJson(Map<String, dynamic> json) {
    return NegotiationPoint(
      title: json['title'] ?? '',
      description: json['description'] ?? json['point'] ?? '',
      priority: NegotiationPriority.fromString(json['priority']),
      suggestedAction: json['suggested_action']?.toString(),
    );
  }

  factory NegotiationPoint.fromString(String point) {
    return NegotiationPoint(
      title: 'Negotiation Point',
      description: point,
    );
  }
}

enum NegotiationPriority {
  high,
  medium,
  low;

  static NegotiationPriority fromString(String? value) {
    switch (value?.toLowerCase()) {
      case 'high':
        return NegotiationPriority.high;
      case 'low':
        return NegotiationPriority.low;
      default:
        return NegotiationPriority.medium;
    }
  }
}

class ChatMessage {
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final MessageType type;

  ChatMessage({
    required this.content,
    required this.isUser,
    DateTime? timestamp,
    this.type = MessageType.text,
  }) : timestamp = timestamp ?? DateTime.now();

  factory ChatMessage.user(String content) {
    return ChatMessage(content: content, isUser: true);
  }

  factory ChatMessage.assistant(String content) {
    return ChatMessage(content: content, isUser: false);
  }
}

enum MessageType {
  text,
  suggestion,
  emailDraft,
  tip,
}

class NegotiationEmail {
  final String subject;
  final String body;
  final String recipientType; // dealer, bank, etc.

  NegotiationEmail({
    required this.subject,
    required this.body,
    required this.recipientType,
  });

  factory NegotiationEmail.fromJson(Map<String, dynamic> json) {
    return NegotiationEmail(
      subject: json['subject'] ?? '',
      body: json['body'] ?? '',
      recipientType: json['recipient_type'] ?? 'dealer',
    );
  }
}
