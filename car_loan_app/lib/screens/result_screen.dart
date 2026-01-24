import 'package:flutter/material.dart';
import '../models/sla_model.dart';

class ResultScreen extends StatelessWidget {
  final SlaModel result;

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Result")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("APR: ${result.aprPercent}%"),
            Text("Tenure: ${result.termMonths} months"),
            Text("Monthly EMI: ₹${result.monthlyPayment}"),
            Text("Fairness Score: ${result.fairnessScore}/100"),
            const SizedBox(height: 10),
            const Text("Reasons:", style: TextStyle(fontWeight: FontWeight.bold)),
            ...result.reasons.map((r) => Text("• $r")),
          ],
        ),
      ),
    );
  }
}
