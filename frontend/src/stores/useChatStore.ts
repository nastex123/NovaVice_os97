import { create } from "zustand";
import { ChatMessage, TelemetryMetrics, ServerHealth } from "../lib/types";
import { sendChatMessage, fetchTelemetryMetrics, fetchServerHealth } from "../lib/api";

export const INITIAL_WELCOME_MESSAGE: ChatMessage = {
  id: "msg_welcome",
  sender: "bot",
  text: `### 🎓 ¡Bienvenido a Nova Idiomas Colombia!

Soy tu asistente virtual de admisiones, programas y servicios académicos. Puedes hacer clic en cualquiera de nuestras áreas o escribir tu pregunta con total libertad:

- **1. Cursos & Certificaciones:** Programas de Inglés, Francés, Alemán, Italiano, Portugués, MCER (A1-C2), IELTS, DELF, TOEFL y Cambridge.

- **2. Horarios & Modalidades:** Madrugadores (6-8am), Diurnos, Nocturno After Work (6:30-8:30pm), Sabatinos y Modalidad Virtual.

- **3. Precios & Financiación:** Tarifas 2026 en COP, 10% Descuento Contado, Plan 3 Cuotas 0% Interés, PSE/Nequi y Convenios.

- **4. Admisiones & Sedes:** Placement Test 100% Gratuito, Sedes Bogotá, Medellín y Cali, Matrículas y Speaking Clubs Ilimitados.

*(Haz clic en una de las opciones abajo o escribe tu consulta en el chat)*`,
  timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  mode: "menu_navigation",
  action_buttons: [
    { label: "1. Cursos & Certificaciones", value: "1" },
    { label: "2. Horarios & Modalidades", value: "2" },
    { label: "3. Precios & Financiación", value: "3" },
    { label: "4. Admisiones & Sedes", value: "4" },
  ],
};

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  sessionId: string;
  currentMenuLabel: string;
  metrics: TelemetryMetrics | null;
  health: ServerHealth | null;

  // Actions
  setMessages: (messages: ChatMessage[] | ((prev: ChatMessage[]) => ChatMessage[])) => void;
  setIsLoading: (loading: boolean) => void;
  setSessionId: (id: string) => void;
  setCurrentMenuLabel: (label: string) => void;
  setMetrics: (metrics: TelemetryMetrics | null) => void;
  setHealth: (health: ServerHealth | null) => void;
  sendMessage: (text: string) => Promise<void>;
  resetChat: () => void;
  newChat: () => void;
  refreshTelemetry: () => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [INITIAL_WELCOME_MESSAGE],
  isLoading: false,
  sessionId: "web_session_nextjs",
  currentMenuLabel: "Menú Principal - Nova Idiomas",
  metrics: null,
  health: null,

  setMessages: (messagesOrFn) =>
    set((state) => ({
      messages: typeof messagesOrFn === "function" ? messagesOrFn(state.messages) : messagesOrFn,
    })),

  setIsLoading: (isLoading) => set({ isLoading }),
  setSessionId: (sessionId) => set({ sessionId }),
  setCurrentMenuLabel: (currentMenuLabel) => set({ currentMenuLabel }),
  setMetrics: (metrics) => set({ metrics }),
  setHealth: (health) => set({ health }),

  refreshTelemetry: async () => {
    const [m, h] = await Promise.all([fetchTelemetryMetrics(), fetchServerHealth()]);
    set({
      metrics: m || get().metrics,
      health: h || get().health,
    });
  },

  sendMessage: async (text: string) => {
    const { isLoading, sessionId, refreshTelemetry } = get();
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: "usr_" + Date.now(),
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    set((state) => ({
      messages: [...state.messages, userMsg],
      isLoading: true,
    }));

    try {
      const resp = await sendChatMessage(text, sessionId, false);

      const botMsg: ChatMessage = {
        id: "bot_" + Date.now(),
        sender: "bot",
        text: resp.text || "No se obtuvo respuesta del sistema.",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        confidence_score: resp.confidence_score,
        latency_ms: resp.latency_ms,
        source_documents: resp.source_documents,
        escalated_to_human: resp.escalated_to_human,
        cached: resp.cached,
        mode: resp.mode,
        action_buttons: resp.action_buttons || [],
      };

      set((state) => ({
        messages: [...state.messages, botMsg],
      }));

      // Update breadcrumb
      if (text === "0" || text.toLowerCase() === "menu") {
        set({ currentMenuLabel: "Menú Principal - Nova Idiomas" });
      } else if (text === "1") {
        set({ currentMenuLabel: "1. Cursos & Certificaciones" });
      } else if (text === "2") {
        set({ currentMenuLabel: "2. Horarios & Modalidades" });
      } else if (text === "3") {
        set({ currentMenuLabel: "3. Precios & Financiación" });
      } else if (text === "4") {
        set({ currentMenuLabel: "4. Admisiones & Sedes" });
      }
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: "err_" + Date.now(),
        sender: "bot",
        text: `⚠️ **Error de Comunicación:** No fue posible conectar con el servidor backend (${err.message}). Por favor verifica que el backend FastAPI esté corriendo en el puerto 8000.`,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        mode: "escalation",
      };
      set((state) => ({
        messages: [...state.messages, errorMsg],
      }));
    } finally {
      set({ isLoading: false });
      refreshTelemetry();
    }
  },

  resetChat: () => {
    get().sendMessage("0");
  },

  newChat: () => {
    const newSession = "sess_idiomas_" + Math.random().toString(36).substring(2, 9);
    if (typeof window !== "undefined") {
      localStorage.setItem("nova_idiomas_session", newSession);
    }
    set({
      sessionId: newSession,
      messages: [INITIAL_WELCOME_MESSAGE],
      currentMenuLabel: "Menú Principal - Nova Idiomas",
    });
  },
}));
