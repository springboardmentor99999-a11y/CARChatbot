import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/sla_model.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000';

  static Future<SlaModel> analyzeLoan(File pdfFile) async {
    final uri = Uri.parse('$baseUrl/analyze');

    final request = http.MultipartRequest('POST', uri);
    request.files.add(
      await http.MultipartFile.fromPath(
        'file',
        pdfFile.path,
      ),
    );

    final streamedResponse = await request.send();

    if (streamedResponse.statusCode != 200) {
      throw Exception('Failed to analyze loan');
    }

    final responseBody = await streamedResponse.stream.bytesToString();
    final jsonData = jsonDecode(responseBody);

    return SlaModel.fromJson(jsonData);
  }
}
