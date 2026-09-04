import { create } from "zustand";

interface SettingsState {
  crtEnabled: boolean;
  soundEnabled: boolean;
  bypassRetroA11y: boolean;
  fontSize: "normal" | "large";

  // Actions
  setCrtEnabled: (enabled: boolean) => void;
  toggleCrt: () => void;
  setSoundEnabled: (enabled: boolean) => void;
  toggleSound: () => void;
  setBypassRetroA11y: (bypass: boolean) => void;
  toggleBypassRetroA11y: () => void;
  setFontSize: (size: "normal" | "large") => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  crtEnabled: true,
  soundEnabled: true,
  bypassRetroA11y: false,
  fontSize: "normal",

  setCrtEnabled: (crtEnabled) => set({ crtEnabled }),
  toggleCrt: () => set((state) => ({ crtEnabled: !state.crtEnabled })),

  setSoundEnabled: (soundEnabled) => set({ soundEnabled }),
  toggleSound: () => set((state) => ({ soundEnabled: !state.soundEnabled })),

  setBypassRetroA11y: (bypassRetroA11y) => set({ bypassRetroA11y }),
  toggleBypassRetroA11y: () => set((state) => ({ bypassRetroA11y: !state.bypassRetroA11y })),

  setFontSize: (fontSize) => set({ fontSize }),
}));
