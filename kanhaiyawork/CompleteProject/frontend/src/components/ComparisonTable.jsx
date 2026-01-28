// src/components/ComparisonTable.jsx

import {
  FiGitCommit,
  FiAlertTriangle,
  FiChevronDown,
  FiChevronRight,
} from "react-icons/fi";
import RiskBadge from "./RiskBadge";
import { useState } from "react";

/**
 * ComparisonTable Component
 * ------------------------
 * Compares multiple contracts and their SLA fields.
 * Handles nested fields like fees and penalties.
 * Shows a Risk column based on differences or missing values.
 *
 * Risk Column:
 * - high: values differ across contracts
 * - medium: some values are missing (null/undefined)
 * - low: all values identical and present
 */

export default function ComparisonTable({ data }) {
  const showEmpty = !data || data.length < 2;

  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 overflow-x-auto border">
      <h3 className="font-semibold mb-4 text-lg flex items-center gap-2">
        <FiGitCommit className="text-indigo-600" /> Contract Comparison
      </h3>

      {showEmpty ? (
        <div className="text-sm text-gray-500 py-16 text-center">
          📊 Select at least <b>two</b> contracts to compare.
        </div>
      ) : (
        <table className="min-w-full text-sm border-collapse">
          <thead className="bg-slate-100 sticky top-0 z-10">
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

              // Determine Risk:
              // high -> values differ across contracts
              // medium -> some values missing
              // low -> all values identical
              const risk =
                diff > 1 ? "high" : values.some((v) => !v) ? "medium" : "low";

              return (
                <Row key={clause} clause={clause} values={values} risk={risk} />
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

/* ---------------- Row Component ---------------- */

function Row({ clause, values, risk }) {
  const [open, setOpen] = useState(false);

  // Check if any value is an object (nested) to allow expandable view
  const hasNested = values.some(
    (v) => v && typeof v === "object" && !Array.isArray(v),
  );

  return (
    <>
      <tr className={`border-t hover:bg-slate-50 transition`}>
        <td
          className="p-3 font-medium capitalize cursor-pointer select-none"
          onClick={() => hasNested && setOpen(!open)}
        >
          <span className="flex items-center gap-1">
            {hasNested && (open ? <FiChevronDown /> : <FiChevronRight />)}
            {clause.replaceAll("_", " ")}
          </span>
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

      {open &&
        // Collect all unique subfields for this clause
        (() => {
          const subfields = new Set();
          values.forEach((v) => {
            if (v && typeof v === "object")
              Object.keys(v).forEach((k) => subfields.add(k));
          });
          return Array.from(subfields).map((subkey) => (
            <tr key={subkey} className="bg-gray-50 border-t">
              <td className="pl-8 py-2 font-medium text-gray-600 capitalize text-sm">
                {subkey.replaceAll("_", " ")}
              </td>
              {values.map((v, i) => (
                <td
                  key={i}
                  className="p-2 text-center break-words max-w-xs whitespace-pre-wrap text-sm"
                >
                  {v && typeof v === "object" ? (v[subkey] ?? "—") : "—"}
                </td>
              ))}
              <td className="p-2 text-center">
                <RiskBadge
                  level={
                    values.some(
                      (v) =>
                        v &&
                        typeof v === "object" &&
                        v[subkey] !== values[0]?.[subkey],
                    )
                      ? "high"
                      : "low"
                  }
                />
              </td>
            </tr>
          ));
        })()}
    </>
  );
}

/* ---------------- Helpers ---------------- */

function collectClauses(data) {
  const set = new Set();
  data.forEach((c) => Object.keys(c.sla || {}).forEach((k) => set.add(k)));
  return Array.from(set);
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") return "{...}"; // Show placeholder, expand on click
  return String(value);
}
