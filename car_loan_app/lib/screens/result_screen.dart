import 'package:flutter/material.dart';
import '../models/sla_model.dart';

class ResultScreen extends StatelessWidget {
  final SlaModel sla;

  const ResultScreen({Key? key, required this.sla}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analysis Result'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Loan Type: ${sla.loanType}'),
            Text('APR: ${sla.aprPercent}%'),
            Text('Monthly Payment: ${sla.monthlyPayment}'),
            Text('Term (Months): ${sla.termMonths}'),
            Text('Finance Amount: ${sla.financeAmount}'),

            const SizedBox(height: 20),

            Text(
              'Fairness Score: ${sla.fairnessScore}',
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),
            const Text(
              'Reasons:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),

            ...sla.reasons.map(
              (r) => Text('• $r'),
            ),
          ],
        ),
      ),
    );
  }
}