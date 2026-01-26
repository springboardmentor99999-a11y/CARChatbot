import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../utils/session";

export default function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/signin" replace />;
  }

  return children;
}
