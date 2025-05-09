import { create } from 'zustand';

export const useScannerStore = create((set) => ({
    conectados: [],
    umbral: -67, // Valor por defecto

    setConectados: (lista) => set({ conectados: lista }),
    setUmbral: (valor) => set({ umbral: valor }),
}));
