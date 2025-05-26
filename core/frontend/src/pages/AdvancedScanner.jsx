import React from 'react';
import { useScannerStore } from '../store/scannerStore'; // Adjust path if needed based on actual project structure
import { Link } from 'react-router-dom'; // For a back button

function AdvancedScanner() {
    const { advancedScanResults, isAdvancedScanning, advancedScanError, clearAdvancedScanResults } = useScannerStore(state => ({
        advancedScanResults: state.advancedScanResults,
        isAdvancedScanning: state.isAdvancedScanning,
        advancedScanError: state.advancedScanError,
        clearAdvancedScanResults: state.clearAdvancedScanResults,
    }));

    if (isAdvancedScanning) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center p-10">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
                <p className="mt-4 text-xl">Realizando análisis avanzado...</p>
                <p className="text-sm text-gray-400">Esto puede tardar unos momentos.</p>
            </div>
        );
    }

    if (advancedScanError) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center text-center p-10">
                <div className="bg-red-800 border border-red-700 p-6 rounded-lg shadow-xl">
                    <h2 className="text-2xl font-bold mb-3 text-red-300">Error en el Análisis</h2>
                    <p className="text-red-400 mb-4">{advancedScanError}</p>
                    <Link 
                        to="/scanner" 
                        onClick={clearAdvancedScanResults}
                        className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg transition"
                    >
                        Volver al Scanner
                    </Link>
                </div>
            </div>
        );
    }

    if (!advancedScanResults || advancedScanResults.length === 0) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center text-center p-10">
                <div className="bg-gray-800 border border-gray-700 p-6 rounded-lg shadow-xl">
                    <h2 className="text-2xl font-bold mb-3 text-gray-300">Sin Resultados</h2>
                    <p className="text-gray-400 mb-4">No hay resultados de análisis avanzado disponibles. Por favor, inicie un análisis desde la página de Scanner.</p>
                    <Link 
                        to="/scanner" 
                        className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg transition"
                    >
                        Ir al Scanner
                    </Link>
                </div>
            </div>
        );
    }

    // Determine all unique keys for headers, excluding 'ip' and 'error' which have fixed positions/handling
    // Also excluding brand, model, sysDescr as they have dedicated columns
    const allKeys = advancedScanResults.reduce((keys, result) => {
        Object.keys(result).forEach(key => {
            if (!keys.includes(key) && key !== 'ip' && key !== 'error' && key !== 'sysDescr' && key !== 'brand' && key !== 'model') {
                keys.push(key);
            }
        });
        return keys;
    }, []);


    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-4 sm:p-6 md:p-10">
            <div className="container mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-3xl font-bold text-gray-200">Resultados del Análisis Avanzado</h1>
                    <Link 
                        to="/scanner" 
                        onClick={clearAdvancedScanResults} // Clear results when going back
                        className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition"
                    >
                        Volver al Scanner
                    </Link>
                </div>
                
                <div className="overflow-x-auto shadow-2xl rounded-lg">
                    <table className="min-w-full bg-gray-800 border border-gray-700">
                        <thead className="bg-gray-700">
                            <tr>
                                <th className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">IP</th>
                                <th className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Marca</th>
                                <th className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Modelo</th>
                                <th className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">sysDescr</th>
                                {allKeys.map(key => (
                                    <th key={key} className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">
                                        {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                    </th>
                                ))}
                                <th className="py-3 px-4 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Error</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-700">
                            {advancedScanResults.map((result, index) => (
                                <tr key={result.ip || index} className={`hover:bg-gray-750 transition-colors duration-150 ${result.error ? 'bg-red-900 bg-opacity-30' : ''}`}>
                                    <td className="py-3 px-4 whitespace-nowrap">{result.ip}</td>
                                    <td className="py-3 px-4 whitespace-nowrap">{result.brand || 'N/A'}</td>
                                    <td className="py-3 px-4 whitespace-nowrap">
                                        {result.error ? <span className="text-red-400">{String(result.model)}</span> : (result.model || 'N/A')}
                                    </td>
                                    <td className="py-3 px-4 text-xs text-gray-400 max-w-xs truncate" title={result.sysDescr}>{result.sysDescr || 'N/A'}</td>
                                    {allKeys.map(key => (
                                        <td key={key} className="py-3 px-4 whitespace-nowrap">{result[key] || 'N/A'}</td>
                                    ))}
                                    <td className="py-3 px-4 whitespace-nowrap">
                                        {result.error ? <span className="text-red-400 font-semibold">Sí</span> : 'No'}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                {advancedScanResults.length > 0 && (
                     <p className="mt-6 text-sm text-gray-500 text-center">
                        Total de dispositivos analizados: {advancedScanResults.length}
                    </p>
                )}
            </div>
        </div>
    );
}

export default AdvancedScanner;
