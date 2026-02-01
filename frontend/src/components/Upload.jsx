import React, { useState } from "react";
import { uploadPdf } from "../services/api";

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!selectedFile) return setError("Please select a PDF");

    setLoading(true);
    setError("");
    try {
      const data = await uploadPdf(selectedFile);
      setResult(data);
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to upload PDF"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 flex flex-col items-center w-full">
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="border-2 border-gray-300 rounded-md p-2 w-full mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload PDF"}
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
      {result && (
        <div className="mt-4 p-4 border rounded w-full bg-gray-50">
          <h3 className="font-bold text-lg mb-2">Result:</h3>
          <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
