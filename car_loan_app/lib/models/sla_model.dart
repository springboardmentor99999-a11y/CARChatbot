class SlaModel {
  final double aprPercent;
  final int termMonths;
  final double monthlyPayment;
  final int fairnessScore;
  final List<String> reasons;

  SlaModel({
    required this.aprPercent,
    required this.termMonths,
    required this.monthlyPayment,
    required this.fairnessScore,
    required this.reasons,
  });

  factory SlaModel.fromJson(Map<String, dynamic> json) {
    return SlaModel(
      aprPercent: (json['apr_percent'] ?? 0).toDouble(),
      termMonths: json['term_months'] ?? 0,
      monthlyPayment: (json['monthly_payment'] ?? 0).toDouble(),
      fairnessScore: json['fairness_score'] ?? 0,
      reasons: List<String>.from(json['reasons'] ?? []),
    );
  }
}
