// Car Loan Assistant - Main Entry Point

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'config/theme.dart';
import 'config/routes.dart';
import 'providers/contract_provider.dart';
import 'providers/negotiation_provider.dart';
import 'services/storage_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize storage service
  await StorageService.init();
  
  // Set system UI overlay style
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  
  // Set preferred orientations
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  
  runApp(const CarLoanAssistantApp());
}

class CarLoanAssistantApp extends StatelessWidget {
  const CarLoanAssistantApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ContractProvider()),
        ChangeNotifierProvider(create: (_) => NegotiationProvider()),
      ],
      child: MaterialApp(
        title: 'Car Loan Assistant',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        initialRoute: AppRoutes.home,
        routes: AppRoutes.routes,
        builder: (context, child) {
          return MediaQuery(
            data: MediaQuery.of(context).copyWith(
              textScaler: const TextScaler.linear(1.0),
            ),
            child: child!,
          );
        },
      ),
    );
  }
}

