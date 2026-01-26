// src/components/ComparisonTable.jsx

import { FiGitCommit, FiAlertTriangle } from "react-icons/fi";
import RiskBadge from "./RiskBadge";

export default function ComparisonTable({ data }) {
  const showEmpty = !data || data.length < 2;

  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 overflow-x-auto border">
      <h3 className="font-semibold mb-4 text-lg flex items-center gap-2">
        <FiGitCommit className="text-indigo-600" />
        Contract Comparison
      </h3>

      {showEmpty ? (
        <div className="text-sm text-gray-500 py-16 text-center">
          📊 Select at least <b>two</b> contracts from above to compare.
        </div>
      ) : (
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 sticky top-0">
            <tr>
              <th className="p-3 text-left">Clause</th>

              {data.map((c) => (
                <th key={c.id} className="p-3 text-center font-semibold">
                  {c.file_name}
                </th>
              ))}

              <th className="p-3 text-center">
                <span className="flex justify-center items-center gap-1">
                  <FiAlertTriangle /> Risk
                </span>
              </th>
            </tr>
          </thead>

          <tbody>
            {collectClauses(data).map((clause) => {
              const values = data.map((c) => c.sla?.[clause]);

              const diff = new Set(values.map((v) => JSON.stringify(v))).size;

              const risk =
                diff > 1 ? "high" : values.some((v) => !v) ? "medium" : "low";

              return (
                <tr
                  key={clause}
                  className={`border-t hover:bg-slate-50 transition`}
                >
                  <td className="p-3 font-medium capitalize">
                    {clause.replaceAll("_", " ")}
                  </td>

                  {values.map((v, i) => (
                    <td
                      key={i}
                      className="p-3 text-center break-words max-w-xs whitespace-pre-wrap text-sm"
                    >
                      {formatValue(v)}
                    </td>
                  ))}

                  <td className="p-3 text-center">
                    <RiskBadge level={risk} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

/* ---------------- helper ---------------- */

function collectClauses(data) {
  const set = new Set();
  data.forEach((c) => Object.keys(c.sla || {}).forEach((k) => set.add(k)));
  return Array.from(set);
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") return JSON.stringify(value, null, 2);
  return String(value);
}
