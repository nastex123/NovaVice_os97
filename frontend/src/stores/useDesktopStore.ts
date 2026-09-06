import { create } from "zustand";

interface WindowState {
  isOpen: boolean;
  isMinimized: boolean;
  isMaximized: boolean;
  zIndex: number;
}

interface DesktopState {
  activeWindowId: string | null;
  highestZIndex: number;
  isMetricsOpen: boolean;
  isChatOpen: boolean;
  isMonitorControlsOpen: boolean;
  windows: Record<string, WindowState>;

  // Actions
  setIsMetricsOpen: (isOpen: boolean) => void;
  setIsChatOpen: (isOpen: boolean) => void;
  setIsMonitorControlsOpen: (isOpen: boolean) => void;
  bringToFront: (windowId: string) => void;
  toggleWindow: (windowId: string) => void;
  closeWindow: (windowId: string) => void;
}

export const useDesktopStore = create<DesktopState>((set, get) => ({
  activeWindowId: "chat_window",
  highestZIndex: 10,
  isMetricsOpen: false,
  isChatOpen: true,
  isMonitorControlsOpen: false,
  windows: {
    chat_window: { isOpen: true, isMinimized: false, isMaximized: false, zIndex: 10 },
    metrics_window: { isOpen: false, isMinimized: false, isMaximized: false, zIndex: 9 },
  },

  setIsMetricsOpen: (isMetricsOpen) =>
    set((state) => ({
      isMetricsOpen,
      highestZIndex: isMetricsOpen ? state.highestZIndex + 1 : state.highestZIndex,
      windows: {
        ...state.windows,
        metrics_window: {
          ...state.windows.metrics_window,
          isOpen: isMetricsOpen,
          zIndex: isMetricsOpen ? state.highestZIndex + 1 : state.windows.metrics_window?.zIndex || 9,
        },
      },
    })),

  setIsChatOpen: (isChatOpen) =>
    set((state) => ({
      isChatOpen,
      windows: {
        ...state.windows,
        chat_window: {
          ...state.windows.chat_window,
          isOpen: isChatOpen,
        },
      },
    })),

  setIsMonitorControlsOpen: (isMonitorControlsOpen) =>
    set((state) => ({
      isMonitorControlsOpen,
      highestZIndex: isMonitorControlsOpen ? state.highestZIndex + 1 : state.highestZIndex,
    })),

  bringToFront: (windowId: string) =>
    set((state) => {
      const nextZ = state.highestZIndex + 1;
      return {
        activeWindowId: windowId,
        highestZIndex: nextZ,
        windows: {
          ...state.windows,
          [windowId]: {
            ...(state.windows[windowId] || { isMinimized: false, isMaximized: false }),
            isOpen: true,
            zIndex: nextZ,
          },
        },
      };
    }),

  toggleWindow: (windowId: string) =>
    set((state) => {
      const current = state.windows[windowId];
      const isOpen = !current?.isOpen;
      const nextZ = isOpen ? state.highestZIndex + 1 : state.highestZIndex;
      return {
        highestZIndex: nextZ,
        windows: {
          ...state.windows,
          [windowId]: {
            ...current,
            isOpen,
            zIndex: isOpen ? nextZ : current?.zIndex || 1,
          },
        },
      };
    }),

  closeWindow: (windowId: string) =>
    set((state) => ({
      windows: {
        ...state.windows,
        [windowId]: {
          ...state.windows[windowId],
          isOpen: false,
        },
      },
      isMetricsOpen: windowId === "metrics_window" ? false : state.isMetricsOpen,
      isChatOpen: windowId === "chat_window" ? false : state.isChatOpen,
    })),
}));
