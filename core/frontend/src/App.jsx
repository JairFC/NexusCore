import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Scanner from './pages/Scanner'; // ✅ Nueva ruta
import AdvancedScanner from './pages/AdvancedScanner';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/scanner" element={<Scanner />} />
        <Route path="/scanner/advanced" element={<AdvancedScanner />} />
      </Routes>
    </Router>
  );
}

export default App;
