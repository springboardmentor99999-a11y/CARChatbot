import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-indigo-700 via-purple-700 to-pink-600 text-white flex items-center justify-center px-6">
      {/* Animated background blobs */}
      <div className="absolute -top-32 -left-32 w-96 h-96 bg-pink-500/30 rounded-full blur-3xl animate-pulse" />
      <div className="absolute top-1/3 -right-40 w-96 h-96 bg-indigo-400/30 rounded-full blur-3xl animate-pulse delay-200" />

      {/* Glass Card */}
      <div className="relative z-10 max-w-5xl w-full bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-10 md:p-16 flex flex-col md:flex-row items-center gap-12">
        {/* LEFT SIDE */}
        <div className="flex-1 text-center md:text-left">
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-6">
            AutoLexis
          </h1>

          <p className="text-lg md:text-xl text-white/90 mb-8">
            AI-powered car lease & loan contract intelligence platform. Analyze
            fairness, detect risky clauses, compare offers, and understand every
            detail before signing.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <Link
              to="/signin"
              className="px-8 py-4 rounded-2xl bg-white text-indigo-700 font-semibold shadow-lg hover:scale-105 hover:shadow-xl transition-all duration-300"
            >
              Sign In
            </Link>

            <Link
              to="/signup"
              className="px-8 py-4 rounded-2xl border border-white/50 hover:bg-white/10 hover:scale-105 transition-all duration-300"
            >
              Create Account
            </Link>
          </div>
        </div>

        {/* RIGHT SIDE – LOGO */}
        <div className="flex-1 flex justify-center">
          <img
            src="/Logo.jpg"
            alt="AutoLexis Logo"
            className="w-64 md:w-80 lg:w-96 drop-shadow-2xl animate-float rounded-xl border border-secondary"
          />
        </div>
      </div>
    </div>
  );
}
