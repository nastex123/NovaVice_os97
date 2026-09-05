import { create } from "zustand";
import { get as idbGet, set as idbSet } from "idb-keyval";

const IDB_SETTINGS_KEY = "nova_admissions_user_settings";

interface SettingsData {
  crtEnabled: boolean;
  soundEnabled: boolean;
  bypassRetroA11y: boolean;
  fontSize: "normal" | "large";
  crtBrightness: number;
  crtCurvature: number;
  crtScanlineOpacity: number;
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
  setCrtBrightness: (brightness: number) => void;
  setCrtCurvature: (curvature: number) => void;
  setCrtScanlineOpacity: (opacity: number) => void;
  resetMonitorDefaults: () => void;
}

const updateCrtCssVars = (brightness: number, curvature: number, scanline: number) => {
  if (typeof document !== "undefined") {
    document.documentElement.style.setProperty("--crt-brightness", String(brightness));
    document.documentElement.style.setProperty("--crt-curvature-opacity", String(curvature));
    document.documentElement.style.setProperty("--crt-scanline-opacity", String(scanline));
  }
};

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
  crtBrightness: 0.98,
  crtCurvature: 0.18,
  crtScanlineOpacity: 0.12,
  isHydrated: false,

  initFromStorage: async () => {
    if (typeof window === "undefined") return;
    try {
      const saved = await idbGet<SettingsData>(IDB_SETTINGS_KEY);
      if (saved) {
        const brightness = saved.crtBrightness ?? 0.98;
        const curvature = saved.crtCurvature ?? 0.18;
        const scanline = saved.crtScanlineOpacity ?? 0.12;
        updateCrtCssVars(brightness, curvature, scanline);

        set({
          crtEnabled: saved.crtEnabled ?? true,
          soundEnabled: saved.soundEnabled ?? true,
          bypassRetroA11y: saved.bypassRetroA11y ?? false,
          fontSize: saved.fontSize ?? "normal",
          crtBrightness: brightness,
          crtCurvature: curvature,
          crtScanlineOpacity: scanline,
          isHydrated: true,
        });
      } else {
        updateCrtCssVars(0.98, 0.18, 0.12);
        set({ isHydrated: true });
      }
    } catch {
      updateCrtCssVars(0.98, 0.18, 0.12);
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

  setCrtBrightness: (crtBrightness) => {
    const { crtCurvature, crtScanlineOpacity } = get();
    updateCrtCssVars(crtBrightness, crtCurvature, crtScanlineOpacity);
    saveSettings({ crtBrightness }, get());
    set({ crtBrightness });
  },

  setCrtCurvature: (crtCurvature) => {
    const { crtBrightness, crtScanlineOpacity } = get();
    updateCrtCssVars(crtBrightness, crtCurvature, crtScanlineOpacity);
    saveSettings({ crtCurvature }, get());
    set({ crtCurvature });
  },

  setCrtScanlineOpacity: (crtScanlineOpacity) => {
    const { crtBrightness, crtCurvature } = get();
    updateCrtCssVars(crtBrightness, crtCurvature, crtScanlineOpacity);
    saveSettings({ crtScanlineOpacity }, get());
    set({ crtScanlineOpacity });
  },

  resetMonitorDefaults: () => {
    const defaults = {
      crtBrightness: 0.98,
      crtCurvature: 0.18,
      crtScanlineOpacity: 0.12,
    };
    updateCrtCssVars(defaults.crtBrightness, defaults.crtCurvature, defaults.crtScanlineOpacity);
    saveSettings(defaults, get());
    set(defaults);
  },
}));
