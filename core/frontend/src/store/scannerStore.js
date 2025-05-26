import { create } from 'zustand';

export const useScannerStore = create((set, get) => ({
    conectados: [], // Existing state - expected to be an array of IP STRINGS based on Scanner.jsx
    umbral: -67,    // Existing state
    
    // New state for advanced scan
    advancedScanResults: [],
    isAdvancedScanning: false,
    advancedScanError: null,

    setConectados: (lista) => set({ conectados: lista }),
    setUmbral: (valor) => set({ umbral: valor }),

    // New actions for advanced scan
    performAdvancedScan: async () => {
        const { conectados } = get(); // Get current connected devices (IP strings)
        if (!conectados || conectados.length === 0) { // Added !conectados check
            set({ advancedScanResults: [], advancedScanError: 'No connected devices to scan.', isAdvancedScanning: false });
            return;
        }
        set({ isAdvancedScanning: true, advancedScanError: null });
        try {
            // CORRECTED: 'conectados' is expected to be an array of IP strings.
            const response = await fetch('/api/scanner/advanced_scan', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ips: conectados }) 
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: "Unknown error structure" }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            set({ advancedScanResults: data.results || [], isAdvancedScanning: false });
        } catch (error) {
            console.error("Advanced scan error:", error);
            set({ advancedScanResults: [], advancedScanError: error.message, isAdvancedScanning: false });
        }
    },
    clearAdvancedScanResults: () => set({ advancedScanResults: [], advancedScanError: null, isAdvancedScanning: false }),
}));
