// Negotiation Provider - State management for negotiation assistant

import 'package:flutter/material.dart';
import '../models/contract.dart';
import '../models/negotiation.dart';
import '../models/sla_data.dart';
import '../services/api_service.dart';

class NegotiationProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  // Chat messages
  List<ChatMessage> _messages = [];
  List<ChatMessage> get messages => _messages;
  
  // Negotiation points
  List<NegotiationPoint> _negotiationPoints = [];
  List<NegotiationPoint> get negotiationPoints => _negotiationPoints;
  
  // Backend negotiation points
  List<String> _backendPoints = [];
  List<String> get backendPoints => _backendPoints;
  
  // Loading state
  bool _isTyping = false;
  bool get isTyping => _isTyping;
  
  // Current contract context
  Contract? _currentContract;
  
  // Initialize with welcome message
  void initialize(Contract? contract) {
    _currentContract = contract;
    _messages = [
      ChatMessage.assistant(
        "👋 Hello! I'm your Car Loan Negotiation Assistant.\n\n"
        "I can help you:\n"
        "• Understand your contract terms\n"
        "• Identify negotiation opportunities\n"
        "• Generate emails to dealers\n"
        "• Suggest questions to ask\n\n"
        "What would you like help with today?"
      ),
    ];
    
    // Generate negotiation points from contract
    if (contract?.slaData != null) {
      _generateNegotiationPoints(contract!.slaData!);
      _fetchBackendNegotiationPoints(contract);
    }
    
    notifyListeners();
  }
  
  // Fetch negotiation points from backend
  Future<void> _fetchBackendNegotiationPoints(Contract contract) async {
    if (contract.slaData == null) return;
    
    try {
      final response = await _apiService.getNegotiationPoints(
        contract.slaData!,
        contract.fairnessScore?.toJson(),
      );
      
      if (response.isSuccess && response.data != null) {
        _backendPoints = response.data!;
        
        // Add backend points to negotiation points
        for (var point in _backendPoints) {
          _negotiationPoints.add(NegotiationPoint(
            title: 'Recommendation',
            description: point,
            priority: NegotiationPriority.medium,
          ));
        }
        notifyListeners();
      }
    } catch (e) {
      // Silently fail - we have local points as fallback
    }
  }
  
  // Send a message
  Future<void> sendMessage(String content) async {
    // Add user message
    _messages.add(ChatMessage.user(content));
    notifyListeners();
    
    // Simulate AI typing
    _isTyping = true;
    notifyListeners();
    
    await Future.delayed(const Duration(milliseconds: 1500));
    
    // Generate response based on content
    final response = _generateResponse(content);
    _messages.add(ChatMessage.assistant(response));
    
    _isTyping = false;
    notifyListeners();
  }
  
  // Generate negotiation points from SLA
  void _generateNegotiationPoints(SlaData sla) {
    _negotiationPoints.clear();
    
    // Check APR
    final apr = double.tryParse(sla.interestRateApr ?? '');
    if (apr != null && apr > 8) {
      _negotiationPoints.add(NegotiationPoint(
        title: 'High Interest Rate',
        description: 'Your APR of ${apr}% is above average. Current market rates are around 5-7% for good credit.',
        priority: NegotiationPriority.high,
        suggestedAction: 'Ask for rate reduction or shop around with other lenders.',
      ));
    }
    
    // Check early termination
    if (sla.earlyTerminationClause != null && 
        !sla.earlyTerminationClause!.toLowerCase().contains('no penalty')) {
      _negotiationPoints.add(NegotiationPoint(
        title: 'Early Termination Penalty',
        description: 'Contract includes early termination fees. This limits your flexibility.',
        priority: NegotiationPriority.medium,
        suggestedAction: 'Negotiate a lower penalty or grace period for early payoff.',
      ));
    }
    
    // Check mileage limits for leases
    final mileage = int.tryParse(sla.mileageAllowance?.replaceAll(RegExp(r'[^0-9]'), '') ?? '');
    if (mileage != null && mileage < 12000) {
      _negotiationPoints.add(NegotiationPoint(
        title: 'Low Mileage Allowance',
        description: 'Annual mileage of $mileage miles may be insufficient for average drivers.',
        priority: NegotiationPriority.medium,
        suggestedAction: 'Request higher mileage limit or negotiate lower overage charges.',
      ));
    }
    
    // Check red flags
    for (var flag in sla.redFlags) {
      _negotiationPoints.add(NegotiationPoint(
        title: 'Red Flag Detected',
        description: flag,
        priority: NegotiationPriority.high,
      ));
    }
    
    notifyListeners();
  }
  
  // Generate AI response
  String _generateResponse(String userMessage) {
    final lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.contains('interest') || lowerMessage.contains('apr') || lowerMessage.contains('rate')) {
      return _getInterestAdvice();
    }
    
    if (lowerMessage.contains('email') || lowerMessage.contains('write') || lowerMessage.contains('message')) {
      return _generateEmailDraft();
    }
    
    if (lowerMessage.contains('question') || lowerMessage.contains('ask')) {
      return _getSuggestedQuestions();
    }
    
    if (lowerMessage.contains('negotiate') || lowerMessage.contains('deal') || lowerMessage.contains('better')) {
      return _getNegotiationTips();
    }
    
    if (lowerMessage.contains('mileage') || lowerMessage.contains('miles')) {
      return _getMileageAdvice();
    }
    
    if (lowerMessage.contains('down payment') || lowerMessage.contains('downpayment')) {
      return _getDownPaymentAdvice();
    }
    
    // Default response
    return "I understand you're looking for help with your car loan. Here are some things I can assist with:\n\n"
        "📝 **Contract Analysis** - Ask me about specific terms\n"
        "💰 **Rate Negotiation** - Tips to get better rates\n"
        "✉️ **Email Drafts** - I can write emails to dealers\n"
        "❓ **Questions to Ask** - Get a list of important questions\n\n"
        "What would you like me to help you with?";
  }
  
  String _getInterestAdvice() {
    final apr = _currentContract?.slaData?.interestRateApr;
    return "📊 **Interest Rate Analysis**\n\n"
        "${apr != null ? 'Your current APR: $apr%\n\n' : ''}"
        "**Tips for negotiating a better rate:**\n\n"
        "1️⃣ Check your credit score before negotiating\n"
        "2️⃣ Get pre-approved from banks/credit unions first\n"
        "3️⃣ Use competing offers as leverage\n"
        "4️⃣ Ask about special promotions or loyalty discounts\n"
        "5️⃣ Consider a shorter loan term for lower rates\n\n"
        "Would you like me to draft an email to request a rate reduction?";
  }
  
  String _generateEmailDraft() {
    return "✉️ **Draft Email to Dealer**\n\n"
        "---\n"
        "Subject: Request for Rate Review - Loan Application\n\n"
        "Dear [Dealer/Finance Manager],\n\n"
        "Thank you for the loan offer for [Vehicle]. After reviewing the terms, "
        "I would like to discuss the interest rate.\n\n"
        "I have been pre-approved by [Bank Name] at a lower rate of [X]%, "
        "and I would appreciate if you could match or improve upon this offer.\n\n"
        "I am a serious buyer and ready to finalize the deal if we can agree on better terms.\n\n"
        "Please let me know your thoughts.\n\n"
        "Best regards,\n"
        "[Your Name]\n"
        "[Phone Number]\n"
        "---\n\n"
        "Feel free to customize this email before sending!";
  }
  
  String _getSuggestedQuestions() {
    return "❓ **Questions to Ask the Dealer:**\n\n"
        "**About Pricing:**\n"
        "• What is the out-the-door price including all fees?\n"
        "• Are there any dealer add-ons I can remove?\n"
        "• Is there room for negotiation on the price?\n\n"
        "**About Financing:**\n"
        "• What APR am I approved for?\n"
        "• Can you match a rate from my bank/credit union?\n"
        "• Are there any financing promotions available?\n\n"
        "**About the Loan:**\n"
        "• Is there a prepayment penalty?\n"
        "• Can I pay extra towards principal?\n"
        "• What happens if I want to refinance later?\n\n"
        "Would you like more questions about any specific topic?";
  }
  
  String _getNegotiationTips() {
    return "💪 **Negotiation Tips:**\n\n"
        "**Before Going to Dealer:**\n"
        "✅ Research fair market value (KBB, Edmunds)\n"
        "✅ Get pre-approved financing\n"
        "✅ Check for manufacturer incentives\n"
        "✅ Know your trade-in value\n\n"
        "**At the Dealer:**\n"
        "✅ Negotiate price before discussing financing\n"
        "✅ Don't reveal your monthly payment target\n"
        "✅ Be prepared to walk away\n"
        "✅ Ask for itemized breakdown of all fees\n\n"
        "**Power Moves:**\n"
        "🎯 Shop at end of month/quarter\n"
        "🎯 Get quotes from multiple dealers\n"
        "🎯 Mention competing offers\n"
        "🎯 Ask for dealer holdback discount\n\n"
        "Want me to analyze your specific contract for negotiation opportunities?";
  }
  
  String _getMileageAdvice() {
    return "🚗 **Mileage Allowance Tips:**\n\n"
        "The average American drives 12,000-15,000 miles per year.\n\n"
        "**If your allowance is too low:**\n"
        "• Negotiate higher mileage upfront (cheaper than overage)\n"
        "• Ask about mileage rollover options\n"
        "• Request lower per-mile overage charges\n\n"
        "**Overage Charges:**\n"
        "Typical range: \$0.15 - \$0.30 per mile\n"
        "Negotiate to the lower end if possible.\n\n"
        "Would you like to calculate potential overage costs?";
  }
  
  String _getDownPaymentAdvice() {
    return "💵 **Down Payment Strategy:**\n\n"
        "**For Loans:**\n"
        "• 20% down is ideal to avoid negative equity\n"
        "• Larger down payment = lower monthly payments\n"
        "• Some lenders offer better rates with more down\n\n"
        "**For Leases:**\n"
        "• Consider minimal down payment\n"
        "• If car is totaled, you lose your down payment\n"
        "• Multiple Security Deposits (MSD) may lower rate\n\n"
        "**Negotiation Tip:**\n"
        "Don't discuss down payment until price is settled!\n\n"
        "What's your current down payment situation?";
  }
  
  // Clear chat
  void clearChat() {
    _messages.clear();
    initialize(_currentContract);
  }
}
