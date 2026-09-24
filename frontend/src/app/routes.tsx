import { Navigate, Route, Routes } from "react-router";
import { FeaturePage } from "./FeaturePage";
import { StatusPage } from "../features/status/StatusPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<FeaturePage feature="help-here" next="/apply" />} />
      <Route
        path="/help-here"
        element={<FeaturePage feature="help-here" next="/apply" />}
      />
      <Route path="/apply" element={<FeaturePage feature="apply" next="/letter" />} />
      <Route path="/letter" element={<FeaturePage feature="letter" next="/deadline" />} />
      <Route path="/deadline" element={<FeaturePage feature="deadline" next="/programs" />} />
      <Route path="/programs" element={<FeaturePage feature="programs" />} />
      <Route path="/status" element={<StatusPage />} />
      <Route path="/about" element={<FeaturePage feature="about" />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
