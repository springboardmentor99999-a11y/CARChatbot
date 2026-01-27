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

      aprPercent: (json['apr_percent'] is num)
          ? (json['apr_percent'] as num).toDouble()
          : 0.0,

      monthlyPayment: (json['monthly_payment'] is num)
          ? (json['monthly_payment'] as num).toDouble()
          : 0.0,

      termMonths: (json['term_months'] is num)
          ? (json['term_months'] as num).toInt()
          : 0,

      financeAmount: (json['finance_amount'] is num)
          ? (json['finance_amount'] as num).toDouble()
          : 0.0,

      fairnessScore: (json['fairness_score'] is num)
          ? (json['fairness_score'] as num).toInt()
          : 0,

      reasons: (json['reasons'] is List)
          ? List<String>.from(json['reasons'])
          : <String>[],
    );
  }
}
