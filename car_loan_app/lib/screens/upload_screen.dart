import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

import '../services/api_service.dart';
import 'result_screen.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({Key? key}) : super(key: key);

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  File? selectedFile;
  bool loading = false;

  Future<void> pickPdf() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null && result.files.single.path != null) {
      setState(() {
        selectedFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> analyzeLoan() async {
    if (selectedFile == null) return;

    setState(() => loading = true);

    try {
      final sla = await ApiService.analyzeLoan(selectedFile!);

      setState(() => loading = false);

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultScreen(sla: sla),
        ),
      );
    } catch (e) {
      setState(() => loading = false);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Car Loan Bot')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.description, size: 80, color: Colors.indigo),
            const SizedBox(height: 20),

            ElevatedButton.icon(
              icon: const Icon(Icons.upload_file),
              label: const Text('Select PDF'),
              onPressed: pickPdf,
            ),

            const SizedBox(height: 20),

            if (selectedFile != null)
              Text(
                'Selected: ${selectedFile!.path.split('/').last}',
                style: const TextStyle(color: Colors.green),
              ),

            const SizedBox(height: 30),

            ElevatedButton(
              onPressed: selectedFile == null || loading ? null : analyzeLoan,
              child: loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Analyze Loan'),
            ),
          ],
        ),
      ),
    );
  }
}
