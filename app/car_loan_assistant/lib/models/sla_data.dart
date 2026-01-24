// SLA Model - Represents extracted contract terms

class SlaData {
  final String? contractType;
  final String? interestRateApr;
  final String? leaseTermMonths;
  final String? monthlyPayment;
  final String? downPayment;
  final String? residualValue;
  final String? mileageAllowance;
  final String? overageChargePerMile;
  final String? earlyTerminationClause;
  final String? purchaseOptionPrice;
  final String? maintenanceResponsibility;
  final String? warrantyCoverage;
  final String? insuranceRequirements;
  final String? latePaymentPenalty;
  final List<String> redFlags;
  final int? contractFairnessScore;

  SlaData({
    this.contractType,
    this.interestRateApr,
    this.leaseTermMonths,
    this.monthlyPayment,
    this.downPayment,
    this.residualValue,
    this.mileageAllowance,
    this.overageChargePerMile,
    this.earlyTerminationClause,
    this.purchaseOptionPrice,
    this.maintenanceResponsibility,
    this.warrantyCoverage,
    this.insuranceRequirements,
    this.latePaymentPenalty,
    this.redFlags = const [],
    this.contractFairnessScore,
  });

  factory SlaData.fromJson(Map<String, dynamic> json) {
    return SlaData(
      contractType: json['contract_type']?.toString(),
      interestRateApr: json['interest_rate_apr']?.toString() ?? json['apr_percent']?.toString(),
      leaseTermMonths: json['lease_term_months']?.toString() ?? json['term_months']?.toString(),
      monthlyPayment: json['monthly_payment']?.toString(),
      downPayment: json['down_payment']?.toString(),
      residualValue: json['residual_value']?.toString(),
      mileageAllowance: json['mileage_allowance']?.toString(),
      overageChargePerMile: json['overage_charge_per_mile']?.toString(),
      earlyTerminationClause: json['early_termination_clause']?.toString(),
      purchaseOptionPrice: json['purchase_option_price']?.toString(),
      maintenanceResponsibility: json['maintenance_responsibility']?.toString(),
      warrantyCoverage: json['warranty_coverage']?.toString(),
      insuranceRequirements: json['insurance_requirements']?.toString(),
      latePaymentPenalty: json['late_payment_penalty']?.toString(),
      redFlags: (json['red_flags'] as List<dynamic>?)
          ?.map((e) => e.toString())
          .toList() ?? [],
      contractFairnessScore: json['contract_fairness_score'] != null 
          ? int.tryParse(json['contract_fairness_score'].toString())
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'contract_type': contractType,
      'interest_rate_apr': interestRateApr,
      'lease_term_months': leaseTermMonths,
      'monthly_payment': monthlyPayment,
      'down_payment': downPayment,
      'residual_value': residualValue,
      'mileage_allowance': mileageAllowance,
      'overage_charge_per_mile': overageChargePerMile,
      'early_termination_clause': earlyTerminationClause,
      'purchase_option_price': purchaseOptionPrice,
      'maintenance_responsibility': maintenanceResponsibility,
      'warranty_coverage': warrantyCoverage,
      'insurance_requirements': insuranceRequirements,
      'late_payment_penalty': latePaymentPenalty,
      'red_flags': redFlags,
      'contract_fairness_score': contractFairnessScore,
    };
  }

  // Get all terms as a list for display
  List<SlaTermItem> get allTerms {
    return [
      SlaTermItem('Contract Type', contractType, 'document'),
      SlaTermItem('Interest Rate (APR)', interestRateApr != null ? '$interestRateApr%' : null, 'percent'),
      SlaTermItem('Lease Term', leaseTermMonths != null ? '$leaseTermMonths months' : null, 'calendar'),
      SlaTermItem('Monthly Payment', monthlyPayment != null ? '\$$monthlyPayment' : null, 'dollar'),
      SlaTermItem('Down Payment', downPayment != null ? '\$$downPayment' : null, 'dollar'),
      SlaTermItem('Residual Value', residualValue != null ? '\$$residualValue' : null, 'dollar'),
      SlaTermItem('Mileage Allowance', mileageAllowance != null ? '$mileageAllowance miles' : null, 'car'),
      SlaTermItem('Overage Charge', overageChargePerMile != null ? '\$$overageChargePerMile/mile' : null, 'warning'),
      SlaTermItem('Early Termination', earlyTerminationClause, 'alert'),
      SlaTermItem('Purchase Option', purchaseOptionPrice != null ? '\$$purchaseOptionPrice' : null, 'shopping'),
      SlaTermItem('Maintenance', maintenanceResponsibility, 'tools'),
      SlaTermItem('Warranty', warrantyCoverage, 'shield'),
      SlaTermItem('Insurance', insuranceRequirements, 'insurance'),
      SlaTermItem('Late Payment Penalty', latePaymentPenalty, 'warning'),
    ];
  }
}

class SlaTermItem {
  final String label;
  final String? value;
  final String iconType;

  SlaTermItem(this.label, this.value, this.iconType);

  bool get hasValue => value != null && value!.isNotEmpty && value != 'null';
}
