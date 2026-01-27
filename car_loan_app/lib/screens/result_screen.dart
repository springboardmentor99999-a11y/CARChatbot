import 'package:flutter/material.dart';
import '../models/sla_model.dart';

class ResultScreen extends StatelessWidget {
  final SlaModel sla;

  const ResultScreen({super.key, required this.sla});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analysis Result')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            _item('Loan Type', sla.loanType),
            _item('APR (%)', sla.aprPercent.toString()),
            _item('Monthly Payment', sla.monthlyPayment.toString()),
            _item('Term (Months)', sla.termMonths.toString()),
            _item('Finance Amount', sla.financeAmount.toString()),
            _item('Fairness Score', sla.fairnessScore.toString()),
            const SizedBox(height: 16),
            const Text(
              'Reasons',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            ...sla.reasons.map(
              (r) => ListTile(
                leading: const Icon(Icons.check),
                title: Text(r),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _item(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          Expanded(
              child: Text(label,
                  style: const TextStyle(fontWeight: FontWeight.bold))),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}
