// src/components/ResultPanel.jsx

import {
  FiCheckCircle,
  FiAlertTriangle,
  FiChevronDown,
  FiChevronUp,
} from "react-icons/fi";
import { useState } from "react";

/* ---------------- Helpers ---------------- */

function prettyLabel(key) {
  return key.replaceAll("_", " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function ValueBadge({ value }) {
  if (typeof value === "number")
    return (
      <span className="px-2 py-0.5 rounded-lg bg-indigo-50 text-indigo-700 text-xs font-semibold">
        {value}
      </span>
    );

  if (typeof value === "string") return value;

  return null;
}

/* ---------- Recursive Renderer ---------- */

function NestedTable({ data }) {
  if (!data || typeof data !== "object") return null;

  return (
    <div className="space-y-3">
      {Object.entries(data).map(([key, value]) => {
        const label = prettyLabel(key);

        if (Array.isArray(value)) {
          return (
            <div key={key}>
              <p className="text-sm font-semibold text-slate-700 mb-1">
                {label}
              </p>

              <div className="flex flex-wrap gap-2">
                {value.length ? (
                  value.map((v, i) => (
                    <span
                      key={i}
                      className="bg-slate-100 text-slate-700 px-2 py-1 rounded-lg text-xs"
                    >
                      {v}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-gray-400">None</span>
                )}
              </div>
            </div>
          );
        }

        if (typeof value === "object" && value !== null) {
          return (
            <details key={key} className="bg-slate-50 border rounded-2xl p-3">
              <summary className="cursor-pointer font-semibold text-slate-700 flex justify-between">
                {label}
              </summary>

              <div className="mt-3 pl-2">
                <NestedTable data={value} />
              </div>
            </details>
          );
        }

        return (
          <div
            key={key}
            className="flex flex-col sm:flex-row sm:justify-between gap-2"
          >
            <span className="font-medium text-slate-600">{label}</span>
            <ValueBadge value={value ?? "Not specified"} />
          </div>
        );
      })}
    </div>
  );
}

/* ---------------- Component ---------------- */

export default function ResultPanel({ data, loading }) {
  const [open, setOpen] = useState(true);

  if (loading)
    return (
      <div className="bg-white rounded-3xl shadow p-6 animate-pulse">
        <p className="text-gray-500">Analyzing contract...</p>
      </div>
    );

  if (!data)
    return (
      <div className="bg-white rounded-3xl shadow p-6 text-gray-500">
        Upload a contract to see analysis results.
      </div>
    );

  const { sla, fairness, negotiation_points } = data;

  return (
    <div className="bg-white rounded-3xl shadow p-6 space-y-6">
      {/* HEADER */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <h3 className="font-semibold text-xl">Contract Analysis</h3>

        <button
          onClick={() => setOpen(!open)}
          className="text-sm text-indigo-600 hover:underline flex items-center gap-1"
        >
          {open ? (
            <>
              Collapse <FiChevronUp />
            </>
          ) : (
            <>
              Expand <FiChevronDown />
            </>
          )}
        </button>
      </div>

      {/* FAIRNESS */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3">
        {fairness?.fairness_score >= 70 ? (
          <FiCheckCircle className="text-green-500 text-2xl" />
        ) : (
          <FiAlertTriangle className="text-yellow-500 text-2xl" />
        )}

        <div>
          <p className="font-medium">
            Fairness Score:{" "}
            <span className="font-bold">{fairness?.fairness_score}/100</span>
          </p>

          {!!fairness?.reasons?.length && (
            <ul className="list-disc ml-5 text-sm text-slate-600">
              {fairness.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* SLA */}
      {open && (
        <div className="border rounded-2xl p-4 max-h-[520px] overflow-y-auto">
          <NestedTable data={sla} />
          <p className="font-bold border rounded p-2 max-h-[520px] overflow-y-auto mt-2">
            Negotiation Points:
            <p className="font-medium">{negotiation_points}</p>
          </p>
        </div>
      )}
    </div>
  );
}
