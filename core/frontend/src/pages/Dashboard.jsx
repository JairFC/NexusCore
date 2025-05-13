import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const irAlScanner = () => {
    navigate('/scanner'); // ✅ Redirige al módulo de escaneo
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-8">Bienvenido al Dashboard</h1>
      <button
        onClick={irAlScanner}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
      >
        Ir al Módulo de Scanner
      </button>
    </div>
  );
}

export default Dashboard;
