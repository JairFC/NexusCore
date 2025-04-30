import { useState } from 'react';
import axios from 'axios';

function Scanner() {
  const [pingResult, setPingResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTestPing = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/scanner/test`);
      setPingResult(response.data.resultado);
    } catch (error) {
      console.error('Error al hacer ping:', error);
      setPingResult(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Módulo Scanner de Red</h1>

      <button
        onClick={handleTestPing}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg"
        disabled={loading}
      >
        {loading ? 'Comprobando...' : 'Probar Ping'}
      </button>

      {pingResult !== null && (
        <p className="mt-4 text-xl">
          Resultado: <span className={pingResult ? "text-green-400" : "text-red-500"}>
            {pingResult ? 'Éxito' : 'Fallo'}
          </span>
        </p>
      )}
    </div>
  );
}

export default Scanner;
