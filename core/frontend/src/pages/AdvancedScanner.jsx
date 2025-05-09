import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AdvancedScanner = () => {
    const [umbral, setUmbral] = useState(-67);
    const [equipos, setEquipos] = useState([]);
    const [loading, setLoading] = useState(false);

    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    const fetchUmbral = async () => {
        try {
            const res = await axios.get(`${apiUrl}/scanner/umbral`);
            setUmbral(res.data.umbral);
        } catch (error) {
            console.error("❌ Error al obtener umbral:", error);
        }
    };

    const analizarSNMP = async () => {
        setLoading(true);
        try {
            const res = await axios.post(`${apiUrl}/scanner/analisis-avanzado`, { umbral });
            setEquipos(res.data.equipos || []);
        } catch (error) {
            console.error("❌ Error en análisis SNMP:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUmbral();
    }, []);

    useEffect(() => {
        analizarSNMP();
    }, [umbral]);

    return (
        <div className="p-6 bg-black text-white min-h-screen">
            <h1 className="text-3xl font-bold mb-6">Análisis Avanzado por SNMP</h1>

            <label className="block mb-2 text-sm font-medium">Umbral de señal (dBm)</label>
            <input
                type="range"
                min={-100}
                max={-40}
                value={umbral}
                onChange={(e) => setUmbral(parseInt(e.target.value))}
                className="w-full mb-4"
            />
            <p className="mb-4">Mostrando equipos con señal menor a <strong>{umbral} dBm</strong></p>

            {loading ? (
                <p>🔄 Analizando equipos...</p>
            ) : (
                <div className="space-y-2">
                    {equipos.length === 0 ? (
                        <p>No se encontraron equipos con señal bajo ese umbral.</p>
                    ) : (
                        equipos.map((eq, idx) => (
                            <div key={eq.ip || idx} className="bg-gray-800 rounded p-3">
                                <p><strong>{eq.nombre || 'Equipo sin nombre'}</strong> - IP: {eq.ip} - Señal: {eq.senal} dBm</p>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export default AdvancedScanner;
