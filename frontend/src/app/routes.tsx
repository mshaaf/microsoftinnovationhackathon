import { Navigate, Route, Routes } from "react-router";
import { FeaturePage } from "./FeaturePage";
import { ApplyPage } from "../features/apply";
import { HelpHerePage } from "../features/help-here/HelpHerePage";
import { LetterPage } from "../features/letter/LetterPage";
import { StatusPage } from "../features/status/StatusPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HelpHerePage />} />
      <Route path="/help-here" element={<HelpHerePage />} />
      <Route path="/apply" element={<ApplyPage />} />
      <Route path="/letter" element={<LetterPage />} />
      <Route path="/deadline" element={<FeaturePage feature="deadline" next="/programs" />} />
      <Route path="/programs" element={<FeaturePage feature="programs" />} />
      <Route path="/status" element={<StatusPage />} />
      <Route path="/about" element={<FeaturePage feature="about" />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
