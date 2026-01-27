import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

import '../models/sla_model.dart';

class ApiService {
  /// Change ONLY if your FastAPI runs elsewhere
static const String baseUrl = 'http://localhost:8000';




  // ======================================================
  // FOR FLUTTER WEB (Chrome) — Uses Uint8List
  // ======================================================
  static Future<SlaModel> analyzeContractBytes(
    Uint8List fileBytes,
    String fileName,
  ) async {
    final uri = Uri.parse('$baseUrl/analyze');

    final request = http.MultipartRequest('POST', uri);

    request.files.add(
      http.MultipartFile.fromBytes(
        'file', // ⚠️ Must match FastAPI parameter name
        fileBytes,
        filename: fileName,
      ),
    );

    final streamedResponse = await request.send();

    if (streamedResponse.statusCode != 200) {
      throw Exception(
        'Failed to analyze contract (${streamedResponse.statusCode})',
      );
    }

    final responseBody =
        await streamedResponse.stream.bytesToString();

    final Map<String, dynamic> jsonData = jsonDecode(responseBody);

  // 🔑 Extract nested SLA object
  final Map<String, dynamic> slaJson = jsonData['sla'];

  return SlaModel.fromJson(slaJson);

  }

  // ======================================================
  // OPTIONAL: FOR MOBILE (Android / iOS)
  // You can ignore this for now
  // ======================================================
  static Future<SlaModel> analyzeContractFile(
    String filePath,
  ) async {
    final uri = Uri.parse('$baseUrl/analyze');

    final request = http.MultipartRequest('POST', uri);

    request.files.add(
      await http.MultipartFile.fromPath(
        'file',
        filePath,
      ),
    );

    final streamedResponse = await request.send();

    if (streamedResponse.statusCode != 200) {
      throw Exception(
        'Failed to analyze contract (${streamedResponse.statusCode})',
      );
    }

    final responseBody =
        await streamedResponse.stream.bytesToString();

    final Map<String, dynamic> jsonData =
        jsonDecode(responseBody);

    return SlaModel.fromJson(jsonData);
  }
}