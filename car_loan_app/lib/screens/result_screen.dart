import 'package:flutter/material.dart';
import '../models/sla_model.dart';

class ResultScreen extends StatelessWidget {
  final SlaModel sla;

  const ResultScreen({super.key, required this.sla});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Loan Analysis')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('APR: ${sla.aprPercent}%'),
            Text('Term: ${sla.termMonths} months'),
            Text('Monthly Payment: ₹${sla.monthlyPayment}'),
            Text('Fairness Score: ${sla.fairnessScore}/100'),
            const SizedBox(height: 12),
            const Text('Reasons:', style: TextStyle(fontWeight: FontWeight.bold)),
            ...sla.reasons.map((r) => Text('- $r')),
          ],
        ),
      ),
    );
  }
}
