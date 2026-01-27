import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

import '../services/api_service.dart';
import '../models/sla_model.dart';
import 'result_screen.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({Key? key}) : super(key: key);

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  Uint8List? fileBytes;
  String? fileName;
  bool isLoading = false;

  // Pick PDF (WEB compatible)
  Future<void> pickPdf() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
      withData: true, // 🔑 REQUIRED FOR WEB
    );

    if (result != null && result.files.single.bytes != null) {
      setState(() {
        fileBytes = result.files.single.bytes;
        fileName = result.files.single.name;
      });
    }
  }

  // Call backend API
  Future<void> analyzeLoan() async {
    if (fileBytes == null || fileName == null) return;

    setState(() => isLoading = true);

    try {
      SlaModel sla =
          await ApiService.analyzeContractBytes(fileBytes!, fileName!);

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultScreen(sla: sla),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Car Loan Bot'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.description,
              size: 80,
              color: Colors.indigo,
            ),
            const SizedBox(height: 20),

            // Select PDF
            ElevatedButton.icon(
              icon: const Icon(Icons.upload_file),
              label: const Text('Select PDF'),
              onPressed: pickPdf,
            ),

            // Show file name
            if (fileName != null)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text(
                  'Selected: $fileName',
                  style: const TextStyle(
                    color: Colors.green,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

            const SizedBox(height: 30),

            // Analyze or Loader
            isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: fileBytes == null ? null : analyzeLoan,
                    child: const Text('Analyze Loan'),
                  ),
          ],
        ),
      ),
    );
  }
}