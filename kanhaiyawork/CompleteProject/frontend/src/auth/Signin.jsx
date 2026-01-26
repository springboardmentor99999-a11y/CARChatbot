// src/auth/Signin.jsx

import { useState } from "react";
import { FiMail, FiLock, FiEye, FiEyeOff } from "react-icons/fi";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { setSession } from "../utils/session";

export default function Signin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", { email, password });
      setSession(res.data.token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid credentials");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 via-slate-200 to-blue-100 px-4">
      <form
        onSubmit={submit}
        className="bg-white rounded-3xl shadow-xl p-10 w-full max-w-md animate-fade-in"
      >
        <h2 className="text-3xl font-bold mb-2 text-center">Welcome Back</h2>

        <p className="text-gray-500 text-center mb-8">Sign in to AutoLexis</p>

        {error && (
          <div className="bg-red-100 text-red-600 p-3 rounded-lg mb-4 text-sm">
            {error}
          </div>
        )}

        {/* EMAIL */}
        <div className="mb-4 relative">
          <FiMail className="absolute top-3.5 left-3 text-gray-400" />
          <input
            type="email"
            required
            placeholder="Email address"
            className="pl-10 w-full border rounded-xl py-3 focus:ring-2 focus:ring-indigo-500 outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        {/* PASSWORD */}
        <div className="mb-6 relative">
          <FiLock className="absolute top-3.5 left-3 text-gray-400" />

          <input
            type={show ? "text" : "password"}
            required
            placeholder="Password"
            className="pl-10 pr-10 w-full border rounded-xl py-3 focus:ring-2 focus:ring-indigo-500 outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            type="button"
            onClick={() => setShow(!show)}
            className="absolute top-3.5 right-3 text-gray-400"
          >
            {show ? <FiEyeOff /> : <FiEye />}
          </button>
        </div>

        <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-semibold transition">
          Sign In
        </button>

        <div className="text-center text-sm mt-6">
          <Link to="/reset" className="text-indigo-600 hover:underline">
            Forgot password?
          </Link>
        </div>

        <div className="text-center text-sm mt-2">
          Don’t have an account?{" "}
          <Link to="/signup" className="text-indigo-600 font-medium">
            Sign up
          </Link>
        </div>
      </form>
    </div>
  );
}
