// src/components/ContractsTable.jsx

import { FiFileText, FiClock, FiCheckSquare } from "react-icons/fi";

export default function ContractsTable({ rows, selected, onToggle }) {
  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 border">
      <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
        <FiFileText className="text-indigo-600" />
        Uploaded Contracts
      </h3>

      {rows.length === 0 ? (
        <div className="text-sm text-gray-500 py-12 text-center">
          📄 No contracts uploaded yet.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-2xl border">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-100 sticky top-0 z-10">
              <tr>
                <th className="px-3 py-3">#</th>

                <th className="px-3 py-3 text-left">
                  <span className="flex items-center gap-1">
                    <FiFileText /> File
                  </span>
                </th>

                <th className="px-3 py-3 text-left">
                  <span className="flex items-center gap-1">
                    <FiClock /> Created
                  </span>
                </th>

                <th className="px-3 py-3 text-center">
                  <FiCheckSquare />
                </th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {rows.map((row, idx) => {
                const isSelected = selected.includes(row.id);

                return (
                  <tr
                    key={row.id}
                    className={`hover:bg-indigo-50 transition ${
                      isSelected ? "bg-indigo-50/60" : ""
                    }`}
                  >
                    <td className="px-3 py-3 font-medium">{idx + 1}</td>

                    <td
                      className="px-3 py-3 max-w-xs truncate font-semibold"
                      title={row.file_name}
                    >
                      {row.file_name}
                    </td>

                    <td className="px-3 py-3 text-gray-500">
                      {row.created_at}
                    </td>

                    <td className="px-3 py-3 text-center">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => onToggle(row.id)}
                        className="accent-indigo-600 scale-125 cursor-pointer"
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
