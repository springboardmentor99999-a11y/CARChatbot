// Contract Review Screen - Display analyzed contract results

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:percent_indicator/circular_percent_indicator.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../../config/theme.dart';
import '../../config/routes.dart';
import '../../providers/contract_provider.dart';
import '../../models/sla_data.dart';
import '../../widgets/sla_term_card.dart';
import '../../widgets/red_flag_card.dart';

class ContractReviewScreen extends StatelessWidget {
  const ContractReviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ContractProvider>(
      builder: (context, provider, child) {
        final contract = provider.currentContract;
        
        if (contract == null) {
          return Scaffold(
            appBar: AppBar(title: const Text('Contract Review')),
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.description_outlined,
                    size: 80,
                    color: Colors.grey,
                  ),
                  const SizedBox(height: 16),
                  const Text('No contract analyzed yet'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => Navigator.pushNamed(context, AppRoutes.upload),
                    child: const Text('Upload Contract'),
                  ),
                ],
              ),
            ),
          );
        }
        
        final sla = contract.slaData;
        final fairnessScore = sla?.contractFairnessScore ?? 
            contract.fairnessScore?.score ?? 75;
        
        return Scaffold(
          appBar: AppBar(
            title: const Text('Contract Analysis'),
            actions: [
              IconButton(
                icon: const Icon(Icons.share),
                onPressed: () {
                  // TODO: Share functionality
                },
              ),
              PopupMenuButton(
                itemBuilder: (context) => [
                  const PopupMenuItem(
                    value: 'compare',
                    child: Row(
                      children: [
                        Icon(Icons.compare_arrows),
                        SizedBox(width: 8),
                        Text('Add to Compare'),
                      ],
                    ),
                  ),
                  const PopupMenuItem(
                    value: 'negotiate',
                    child: Row(
                      children: [
                        Icon(Icons.chat),
                        SizedBox(width: 8),
                        Text('Get Negotiation Tips'),
                      ],
                    ),
                  ),
                ],
                onSelected: (value) {
                  if (value == 'compare') {
                    provider.addToComparison(contract);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Added to comparison')),
                    );
                  } else if (value == 'negotiate') {
                    Navigator.pushNamed(context, AppRoutes.negotiation);
                  }
                },
              ),
            ],
          ),
          body: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Fairness Score Header
                _buildFairnessHeader(context, fairnessScore),
                
                // Quick Stats
                _buildQuickStats(context, sla),
                
                // Red Flags Section
                if (sla?.redFlags.isNotEmpty ?? false) ...[
                  _buildSectionHeader(context, 'Red Flags', Icons.warning, AppTheme.errorColor),
                  _buildRedFlags(context, sla!.redFlags),
                ],
                
                // Contract Details Section
                _buildSectionHeader(context, 'Contract Terms', Icons.description, AppTheme.primaryColor),
                _buildContractTerms(context, sla),
                
                // Vehicle Info Section
                if (contract.vehicleInfo != null) ...[
                  _buildSectionHeader(context, 'Vehicle Information', Icons.directions_car, AppTheme.infoColor),
                  _buildVehicleInfo(context, contract.vehicleInfo!),
                ],
                
                // Action Buttons
                _buildActionButtons(context),
                
                const SizedBox(height: 32),
              ],
            ),
          ),
        );
      },
    );
  }
  
  Widget _buildFairnessHeader(BuildContext context, int score) {
    final color = AppTheme.getFairnessColor(score);
    final rating = _getRating(score);
    
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppTheme.primaryColor,
            AppTheme.primaryLight,
          ],
        ),
      ),
      child: Row(
        children: [
          CircularPercentIndicator(
            radius: 60,
            lineWidth: 10,
            percent: score / 100,
            center: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  '$score',
                  style: const TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const Text(
                  '/100',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
            progressColor: color,
            backgroundColor: Colors.white30,
            circularStrokeCap: CircularStrokeCap.round,
          ),
          const SizedBox(width: 24),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Fairness Score',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  rating,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  _getRatingDescription(score),
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildQuickStats(BuildContext context, SlaData? sla) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Expanded(
            child: _buildStatCard(
              'APR',
              sla?.interestRateApr != null ? '${sla!.interestRateApr}%' : 'N/A',
              Icons.percent,
              AppTheme.infoColor,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: _buildStatCard(
              'Monthly',
              sla?.monthlyPayment != null ? '\$${sla!.monthlyPayment}' : 'N/A',
              Icons.calendar_month,
              AppTheme.successColor,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: _buildStatCard(
              'Term',
              sla?.leaseTermMonths != null ? '${sla!.leaseTermMonths} mo' : 'N/A',
              Icons.access_time,
              AppTheme.warningColor,
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildStatCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildSectionHeader(BuildContext context, String title, IconData icon, Color color) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(width: 12),
          Text(
            title,
            style: Theme.of(context).textTheme.titleLarge,
          ),
        ],
      ),
    );
  }
  
  Widget _buildRedFlags(BuildContext context, List<String> redFlags) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        children: redFlags.map((flag) => RedFlagCard(message: flag)).toList(),
      ),
    );
  }
  
  Widget _buildContractTerms(BuildContext context, SlaData? sla) {
    if (sla == null) {
      return const Padding(
        padding: EdgeInsets.all(16),
        child: Text('No contract terms extracted'),
      );
    }
    
    final terms = sla.allTerms.where((t) => t.hasValue).toList();
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        children: terms.map((term) => SlaTermCard(term: term)).toList(),
      ),
    );
  }
  
  Widget _buildVehicleInfo(BuildContext context, vehicleInfo) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(FontAwesomeIcons.car, color: AppTheme.primaryColor),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    vehicleInfo.displayName,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const Divider(height: 24),
            if (vehicleInfo.vin != null)
              _buildInfoRow('VIN', vehicleInfo.vin!),
            if (vehicleInfo.manufacturer != null)
              _buildInfoRow('Manufacturer', vehicleInfo.manufacturer!),
            if (vehicleInfo.engineInfo != null)
              _buildInfoRow('Engine', vehicleInfo.engineInfo!),
            if (vehicleInfo.fuelType != null)
              _buildInfoRow('Fuel Type', vehicleInfo.fuelType!),
            if (vehicleInfo.hasRecalls) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.warningColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppTheme.warningColor),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.warning, color: AppTheme.warningColor),
                    const SizedBox(width: 8),
                    Text(
                      '${vehicleInfo.recalls.length} active recall(s)',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: AppTheme.warningColor,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
  
  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: TextStyle(
                color: Colors.grey[600],
                fontSize: 14,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildActionButtons(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          ElevatedButton.icon(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.negotiation),
            icon: const Icon(Icons.chat, color: Colors.white),
            label: const Text('Get Negotiation Tips', style: TextStyle(color: Colors.white)),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.upload),
            icon: const Icon(Icons.upload_file),
            label: const Text('Analyze Another Contract'),
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
        ],
      ),
    );
  }
  
  String _getRating(int score) {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  }
  
  String _getRatingDescription(int score) {
    if (score >= 80) return 'This contract has favorable terms';
    if (score >= 60) return 'This contract is reasonable but has room for negotiation';
    if (score >= 40) return 'Consider negotiating several terms';
    return 'This contract needs significant negotiation';
  }
}
