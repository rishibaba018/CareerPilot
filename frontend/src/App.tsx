import { Route, Routes } from "react-router-dom";
import Layout from "@/components/Layout";
import ProtectedRoute from "@/components/ProtectedRoute";
import Dashboard from "@/pages/Dashboard";
import JobDetail from "@/pages/JobDetail";
import Jobs from "@/pages/Jobs";
import Landing from "@/pages/Landing";
import Login from "@/pages/Login";
import Onboarding from "@/pages/Onboarding";
import Register from "@/pages/Register";
import ResumeStudio from "@/pages/ResumeStudio";
import Roadmap from "@/pages/Roadmap";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/jobs/:id" element={<JobDetail />} />
          <Route path="/jobs/:id/studio" element={<ResumeStudio />} />
          <Route path="/roadmap" element={<Roadmap />} />
        </Route>
      </Route>
    </Routes>
  );
}
