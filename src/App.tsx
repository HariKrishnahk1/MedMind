import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { ModelLab } from './pages/ModelLab';
import { Experiments } from './pages/Experiments';
import { ModelMonitoring } from './pages/ModelMonitoring';
import { Simulation } from './pages/Simulation';
import { PatientProfile } from './pages/PatientProfile';
import { PatientList } from './pages/PatientList';
import { Monitoring } from './pages/Monitoring';
import { AIExplainability } from './pages/AIExplainability';
import { AlertCenter } from './pages/AlertCenter';
import { Handover } from './pages/Handover';
import { Settings } from './pages/Settings';
import { PatientTimeline } from './pages/PatientTimeline';
import { ResearchAnalytics } from './pages/ResearchAnalytics';
import { Login } from './pages/Login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login onLogin={() => setIsAuthenticated(true)} />
        } />
        
        {/* Protected Routes */}
        <Route path="/" element={
          isAuthenticated ? <Layout /> : <Navigate to="/login" replace />
        }>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="model-lab" element={<ModelLab />} />
          <Route path="experiments" element={<Experiments />} />
          <Route path="model-monitoring" element={<ModelMonitoring />} />
          <Route path="simulation" element={<Simulation />} />
          <Route path="patients" element={<PatientList />} />
          <Route path="patients/:id" element={<PatientProfile />} />
          <Route path="monitoring" element={<Monitoring />} />
          <Route path="ai-explain" element={<AIExplainability />} />
          <Route path="alerts" element={<AlertCenter />} />
          <Route path="handover" element={<Handover />} />
          <Route path="timeline" element={<PatientTimeline />} />
          <Route path="research" element={<ResearchAnalytics />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
