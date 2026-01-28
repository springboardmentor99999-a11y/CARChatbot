// src/components/Navbar.jsx

import { FiUser, FiLogOut } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

function getUserFromToken() {
  const token = sessionStorage.getItem("auth_token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload?.name || payload?.sub || "User";
  } catch {
    return "User";
  }
}

export default function Navbar() {
  const navigate = useNavigate();

  const userName = getUserFromToken();

  const logout = () => {
    sessionStorage.clear();
    navigate("/signin");
  };

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <img
            src="/Logo.jpg"
            alt="AutoLexis Logo"
            className="h-20 w-20 rounded-lg object-contain"
          />
          <span className="font-bold text-xl tracking-tight text-slate-800">
            AutoLexis
          </span>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* USER NAME */}
          <div className="hidden md:flex items-center gap-2 text-slate-600 text-sm font-medium">
            <FiUser />
            <span>{userName}</span>
          </div>

          {/* LOGOUT */}
          <button
            onClick={logout}
            className="flex items-center gap-2 px-4 py-2 rounded-xl
                       bg-red-50 text-red-600 hover:bg-red-100
                       transition font-medium"
          >
            <FiLogOut />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
