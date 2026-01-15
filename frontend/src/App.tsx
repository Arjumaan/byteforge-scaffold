import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Targets } from './pages/Targets';
import { Jobs } from './pages/Jobs';
import { Findings } from './pages/Findings';
import { Evidence } from './pages/Evidence';
import { Reports } from './pages/Reports';
import { Settings } from './pages/Settings';
import { NetworkMap } from './pages/NetworkMap';
import { AIAssistant } from './pages/AIAssistant';
import { Login } from './pages/Login';

import { useState, useEffect } from 'react';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  useEffect(() => {
    const handleStorage = () => setToken(localStorage.getItem('token'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/*"
        element={
          token ? (
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/ai" element={<AIAssistant />} />
                <Route path="/targets" element={<Targets />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/findings" element={<Findings />} />
                <Route path="/evidence" element={<Evidence />} />
                <Route path="/network" element={<NetworkMap />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="*" element={<Navigate to="/" />} />
              </Routes>
            </Layout>
          ) : (
            <Navigate to="/login" />
          )
        }
      />
    </Routes>
  );
}

export default App;