// src/dashboard/Dashboard.jsx

import { useState, useEffect, useCallback } from "react";
import { api } from "../api/client";

import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import ResultPanel from "../components/ResultPanel";
import ContractsTable from "../components/ContractsTable";
import ComparisonTable from "../components/ComparisonTable";
import VinLookup from "../components/VinLookup";

export default function Dashboard() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const [contracts, setContracts] = useState([]);

  const [selectedIds, setSelectedIds] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);

  /* ---------------- API Calls ---------------- */

  const fetchContracts = useCallback(async () => {
    try {
      const res = await api.get("/contracts");
      setContracts(res.data);
    } catch {
      console.error("Failed to load contracts");
    }
  }, []);

  const loadComparison = useCallback(async () => {
    if (selectedIds.length < 2) {
      setComparisonData([]);
      return;
    }

    try {
      const res = await api.get("/compare", {
        params: { ids: selectedIds.join(",") },
      });

      setComparisonData(res.data);
    } catch {
      console.error("Comparison failed");
    }
  }, [selectedIds]);

  /* ---------------- Effects ---------------- */

  // Load contracts once
  useEffect(() => {
    fetchContracts();
  }, [fetchContracts]);

  // Reload comparison whenever selection changes
  useEffect(() => {
    loadComparison();
  }, [loadComparison]);

  /* ---------------- UI Logic ---------------- */

  const handleResult = (data) => {
    setAnalysis(data);
    fetchContracts();
  };

  const toggleContract = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    );
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />

      <main className="max-w-7xl mx-auto p-6 space-y-8">
        {/* ROW 1 */}
        <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
          <div className="xl:col-span-2">
            <UploadBox
              onResult={handleResult}
              setLoading={setLoading}
              loading={loading}
            />
          </div>

          <div className="xl:col-span-3">
            <ResultPanel data={analysis} loading={loading} />
          </div>
        </div>

        {/* ROW 2: VIN Lookup */}
        <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
          <div className="xl:col-span-5">
            <VinLookup />
          </div>
        </div>

        {/* ROW 3: */}
        <ContractsTable
          rows={contracts}
          selected={selectedIds}
          onToggle={toggleContract}
        />

        {/* ROW 4: */}
        <ComparisonTable data={comparisonData} />
      </main>
    </div>
  );
}
