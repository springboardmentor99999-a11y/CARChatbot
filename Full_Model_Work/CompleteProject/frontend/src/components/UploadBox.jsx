// src/components/UploadBox.jsx

import { useState } from "react";
import { FiUploadCloud } from "react-icons/fi";
import { api } from "../api/client";

export default function UploadBox({ onResult, loading, setLoading }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const upload = async () => {
    if (!file) {
      setError("Please upload a PDF contract.");
      return;
    }

    setError("");
    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await api.post("/analyze", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      onResult(res.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Contract analysis failed.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow p-6 space-y-5">
      <h3 className="font-semibold text-lg">Upload Contract PDF</h3>

      {/* Upload Area */}
      <label
        className="border-2 border-dashed rounded-2xl p-8 text-center
                         cursor-pointer hover:border-indigo-400 transition block"
      >
        <FiUploadCloud className="mx-auto text-4xl text-indigo-500 mb-3" />

        <p className="font-medium max-w-full truncate">
          {file ? file.name : "Click to select PDF file"}
        </p>

        <p className="text-xs text-gray-500 mt-1">PDF format only · Max 10MB</p>

        <input
          type="file"
          accept="application/pdf"
          hidden
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      {error && <p className="text-red-600 text-sm">{error}</p>}

      <button
        disabled={loading}
        onClick={upload}
        className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50
                   text-white py-3 rounded-xl font-semibold transition"
      >
        {loading ? "Analyzing..." : "Analyze Contract"}
      </button>
    </div>
  );
}
