import React, { useState, useRef, useEffect } from "react";
import Upload from "./Upload";
import { getCarDetailsByVin } from "../services/api";

function Dashboard() {
  const [vin, setVin] = useState("");
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  // Scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleVinSubmit = async () => {
    if (!vin.trim()) return;

    setMessages(prev => [...prev, { type: "user", text: vin }]);
    setVin("");

    try {
      const data = await getCarDetailsByVin(vin);
      setMessages(prev => [...prev, { type: "bot", text: JSON.stringify(data, null, 2) }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: "bot", text: "Error fetching VIN details" }]);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-100 flex flex-col items-center p-6">
      
      {/* Main Card */}
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl p-8 flex flex-col md:flex-row gap-8">
        
        {/* Left side: VIN Input */}
        <div className="flex-1 flex flex-col gap-6 justify-center">
          <h1 className="text-4xl font-extrabold text-gray-800 text-center md:text-left">
            Car Loan Bot
          </h1>
          <p className="text-gray-500 text-center md:text-left">
            Enter your car VIN or upload PDF documents to analyze.
          </p>
          <input
            type="text"
            placeholder="Enter VIN number..."
            className="w-full p-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-lg shadow-sm"
            value={vin}
            onChange={e => setVin(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleVinSubmit()}
          />
          <button
            onClick={handleVinSubmit}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition-all text-lg shadow"
          >
            Submit VIN
          </button>
        </div>

        {/* Right side: PDF Upload */}
        <div className="flex-1 flex flex-col justify-center items-center border-dashed border-2 border-gray-300 rounded-xl p-6 hover:border-indigo-400 transition-all cursor-pointer">
          <Upload setMessages={setMessages} />
        </div>
      </div>

      {/* Chat Area */}
      <div className="mt-10 w-full max-w-4xl flex-1 overflow-y-auto p-4 flex flex-col gap-3">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-md p-4 rounded-xl shadow-md break-words ${
              msg.type === "user"
                ? "bg-indigo-100 self-end text-gray-800"
                : "bg-white self-start text-gray-900"
            }`}
          >
            <pre className="whitespace-pre-wrap">{msg.text}</pre>
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>
    </div>
  );
}

export default Dashboard;
