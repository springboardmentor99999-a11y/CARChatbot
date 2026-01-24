import 'package:flutter/material.dart';
import '../screens/home/home_screen.dart';
import '../screens/upload/upload_contract_screen.dart';
import '../screens/review/contract_review_screen.dart';
import '../screens/negotiation/negotiation_screen.dart';
import '../screens/vin/vin_lookup_screen.dart';
import '../screens/comparison/comparison_screen.dart';
import '../screens/history/history_screen.dart';

class AppRoutes {
  static const String home = '/';
  static const String upload = '/upload';
  static const String review = '/review';
  static const String negotiation = '/negotiation';
  static const String vinLookup = '/vin-lookup';
  static const String comparison = '/comparison';
  static const String history = '/history';
  
  static Map<String, WidgetBuilder> get routes => {
    home: (context) => const HomeScreen(),
    upload: (context) => const UploadContractScreen(),
    review: (context) => const ContractReviewScreen(),
    negotiation: (context) => const NegotiationScreen(),
    vinLookup: (context) => const VinLookupScreen(),
    comparison: (context) => const ComparisonScreen(),
    history: (context) => const HistoryScreen(),
  };
}
