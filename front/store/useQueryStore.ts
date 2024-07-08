import { create } from "zustand";

interface QueryStore {
  searchParams: URLSearchParams;
  setSearchParams: (params: URLSearchParams) => void;
}

export const useQueryStore = create<QueryStore>((set) => ({
  searchParams: new URLSearchParams(),
  setSearchParams: (params: URLSearchParams) => set({ searchParams: params }),
}));
