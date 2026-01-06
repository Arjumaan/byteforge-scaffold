import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Targets } from './pages/Targets';
import { Jobs } from './pages/Jobs';
import { Findings } from './pages/Findings';
import { Login } from './pages/Login';

function App() {
  const token = localStorage.getItem('token');

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
                <Route path="/targets" element={<Targets />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/findings" element={<Findings />} />
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