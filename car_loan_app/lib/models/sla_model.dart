class SlaModel {
  final String loanType;
  final double aprPercent;
  final double monthlyPayment;
  final int termMonths;
  final double financeAmount;
  final int fairnessScore;
  final List<String> reasons;

  SlaModel({
    required this.loanType,
    required this.aprPercent,
    required this.monthlyPayment,
    required this.termMonths,
    required this.financeAmount,
    required this.fairnessScore,
    required this.reasons,
  });

  factory SlaModel.fromJson(Map<String, dynamic> json) {
  return SlaModel(
    loanType: json['loan_type']?.toString() ?? 'N/A',
    aprPercent: (json['apr_percent'] ?? 0).toDouble(),
    monthlyPayment: (json['monthly_payment'] ?? 0).toDouble(),
    termMonths: json['term_months'] ?? 0,
    financeAmount: (json['finance_amount'] ?? 0).toDouble(),
    fairnessScore: json['fairness_score'] ?? 0,
    // Backend ki 'red_flags' key ko model ke 'reasons' mein map kiya
    reasons: List<String>.from(json['red_flags'] ?? []), 
  );
}
}