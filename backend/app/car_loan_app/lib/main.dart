// main.dart
import 'package:flutter/material.dart';
import 'screens/upload_screen.dart';

void main() {
  runApp(const CarLoanApp());
}

class CarLoanApp extends StatelessWidget {
  const CarLoanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Car Loan Bot',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        useMaterial3: true,
      ),
      home: UploadScreen(),
    );
  }
}