import { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useScannerStore } from '../store/scannerStore';

function Scanner() {
  const [network, setNetwork] = useState('');
  const [results, setResults] = useState({ conectados: [], desconectados: [] });
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const setConectados = useScannerStore(state => state.setConectados);

  const handleScan = async () => {
    setLoading(true);
    setResults({ conectados: [], desconectados: [] });
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/scanner/scan`, {
        params: { network }
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error al escanear:', error);
      setResults({ conectados: [], desconectados: [] });
    } finally {
      setLoading(false);
    }
  };

  const copiarAlPortapapeles = () => {
    const texto = results.conectados.join('\n');
    navigator.clipboard.writeText(texto);
  };

  const iniciarEtapa2 = () => {
    setConectados(results.conectados);
    navigate('/scanner/advanced');
  };

  const cardVariant = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 via-gray-900 to-black text-white p-10">
      <h1 className="text-4xl font-bold mb-8 text-center">Módulo Scanner de Red</h1>

      <div className="mb-6 flex justify-center gap-2">
        <input
          type="text"
          value={network}
          onChange={(e) => setNetwork(e.target.value)}
          placeholder="Red CIDR (ej: 192.168.99.0/24)"
          className="p-4 rounded-lg bg-gray-700 text-white w-96 shadow-lg focus:outline-none"
        />

        <button
          onClick={handleScan}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-6 rounded-lg shadow-lg transition"
          disabled={loading}
        >
          {loading ? 'Escaneando...' : 'Iniciar Escaneo'}
        </button>
      </div>

      {loading && (
        <div className="text-center my-4">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
            className="border-4 border-blue-500 border-t-transparent w-10 h-10 mx-auto rounded-full"
          />
        </div>
      )}

      <div className="flex justify-center gap-10">
        <AnimatePresence>
          {results.conectados.filter(Boolean).length > 0 && (
            <motion.div
              initial="hidden"
              animate="visible"
              variants={cardVariant}
              className="bg-green-700 rounded-lg shadow-xl p-6 w-80 hover:scale-105 transition-transform"
            >
              <h2 className="text-2xl font-semibold mb-4">Conectados ({results.conectados.length})</h2>
              <ul className="overflow-auto h-60">
                {results.conectados.filter(Boolean).map(ip => <li key={ip}>{ip}</li>)}
              </ul>
              <div className="mt-4 flex gap-2">
                <button onClick={copiarAlPortapapeles} className="bg-gray-700 px-3 py-2 rounded">Copiar</button>
                <button onClick={iniciarEtapa2} className="bg-green-600 px-3 py-2 rounded">Análisis Avanzado</button>
              </div>
            </motion.div>
          )}

          {results.desconectados.filter(Boolean).length > 0 && (
            <motion.div
              initial="hidden"
              animate="visible"
              variants={cardVariant}
              className="bg-red-700 rounded-lg shadow-xl p-6 w-80 hover:scale-105 transition-transform"
            >
              <h2 className="text-2xl font-semibold mb-4">Desconectados ({results.desconectados.length})</h2>
              <ul className="overflow-auto h-60">
                {results.desconectados.filter(Boolean).map(ip => <li key={ip}>{ip}</li>)}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default Scanner;
