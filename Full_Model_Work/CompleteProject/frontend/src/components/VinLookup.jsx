import { useState } from "react";
import { FiSearch, FiTruck, FiAlertCircle } from "react-icons/fi";
import { api } from "../api/client";

const DEFAULT_VINS = [
  "1HGCM82633A004352",
  "1C4RJFBG5FC625797",
  "3VW4T7AJ5EM123456",
  "2T1BURHE5JC123456",
  "5NPE34AF7JH123456",
];

export default function VinLookup() {
  const [vin, setVin] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const lookupVin = async (v) => {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const res = await api.get(`/vin/${v}`);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "VIN lookup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 space-y-6 border">
      <h3 className="font-semibold text-lg flex items-center gap-2">
        <FiTruck className="text-indigo-600" /> VIN Lookup
      </h3>

      {/* Input & Button */}
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          placeholder="Enter VIN (17 characters)"
          value={vin}
          onChange={(e) => setVin(e.target.value.toUpperCase())}
          className="flex-1 border rounded-xl p-3 outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          onClick={() => lookupVin(vin)}
          disabled={vin.length !== 17 || loading}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl px-5 py-3 font-semibold flex items-center gap-2 justify-center"
        >
          {loading ? (
            "Searching..."
          ) : (
            <>
              <FiSearch /> Lookup
            </>
          )}
        </button>
      </div>

      {/* Result */}
      {error && (
        <div className="text-red-600 text-sm flex items-center gap-2">
          <FiAlertCircle /> {error}
        </div>
      )}

      {result && (
        <div className="bg-slate-50 rounded-xl p-4 text-sm space-y-2">
          {Object.entries(result).map(([key, value]) => (
            <div key={key} className="flex justify-between border-b py-1">
              <span className="font-medium capitalize">
                {key.replaceAll("_", " ")}
              </span>
              <span className="text-gray-700">{value || "—"}</span>
            </div>
          ))}
        </div>
      )}

      {/* Default VINs for testing */}
      <div className="mt-4">
        <h4 className="font-medium mb-2 text-sm text-gray-600">Test VINs:</h4>
        <div className="flex flex-wrap gap-2">
          {DEFAULT_VINS.map((v) => (
            <button
              key={v}
              onClick={() => {
                setVin(v);
                lookupVin(v);
              }}
              className="bg-indigo-100 hover:bg-indigo-200 text-indigo-800 px-3 py-1 rounded-xl text-sm transition"
            >
              {v}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
