import 'package:flutter/material.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({Key? key}) : super(key: key);

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Car Loan Bot'),
      ),
      body: const Center(
        child: Text(
          'Upload Screen Loaded',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}