import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Scanner from './pages/Scanner'; // ✅ Nueva ruta


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/scanner" element={<Scanner />} />
      </Routes>
    </Router>
  );
}

export default App;
