import { create } from "zustand";
import { get as idbGet, set as idbSet } from "idb-keyval";

const IDB_SETTINGS_KEY = "nova_admissions_user_settings";

interface SettingsData {
  crtEnabled: boolean;
  soundEnabled: boolean;
  bypassRetroA11y: boolean;
  fontSize: "normal" | "large";
}

interface SettingsState extends SettingsData {
  isHydrated: boolean;

  // Actions
  initFromStorage: () => Promise<void>;
  setCrtEnabled: (enabled: boolean) => void;
  toggleCrt: () => void;
  setSoundEnabled: (enabled: boolean) => void;
  toggleSound: () => void;
  setBypassRetroA11y: (bypass: boolean) => void;
  toggleBypassRetroA11y: () => void;
  setFontSize: (size: "normal" | "large") => void;
}

const saveSettings = (data: Partial<SettingsData>, current: SettingsData) => {
  if (typeof window !== "undefined") {
    idbSet(IDB_SETTINGS_KEY, { ...current, ...data }).catch(() => {});
  }
};

export const useSettingsStore = create<SettingsState>((set, get) => ({
  crtEnabled: true,
  soundEnabled: true,
  bypassRetroA11y: false,
  fontSize: "normal",
  isHydrated: false,

  initFromStorage: async () => {
    if (typeof window === "undefined") return;
    try {
      const saved = await idbGet<SettingsData>(IDB_SETTINGS_KEY);
      if (saved) {
        set({
          crtEnabled: saved.crtEnabled ?? true,
          soundEnabled: saved.soundEnabled ?? true,
          bypassRetroA11y: saved.bypassRetroA11y ?? false,
          fontSize: saved.fontSize ?? "normal",
          isHydrated: true,
        });
      } else {
        set({ isHydrated: true });
      }
    } catch {
      set({ isHydrated: true });
    }
  },

  setCrtEnabled: (crtEnabled) => {
    saveSettings({ crtEnabled }, get());
    set({ crtEnabled });
  },
  toggleCrt: () => {
    const next = !get().crtEnabled;
    saveSettings({ crtEnabled: next }, get());
    set({ crtEnabled: next });
  },

  setSoundEnabled: (soundEnabled) => {
    saveSettings({ soundEnabled }, get());
    set({ soundEnabled });
  },
  toggleSound: () => {
    const next = !get().soundEnabled;
    saveSettings({ soundEnabled: next }, get());
    set({ soundEnabled: next });
  },

  setBypassRetroA11y: (bypassRetroA11y) => {
    saveSettings({ bypassRetroA11y }, get());
    set({ bypassRetroA11y });
  },
  toggleBypassRetroA11y: () => {
    const next = !get().bypassRetroA11y;
    saveSettings({ bypassRetroA11y: next }, get());
    set({ bypassRetroA11y: next });
  },

  setFontSize: (fontSize) => {
    saveSettings({ fontSize }, get());
    set({ fontSize });
  },
}));
