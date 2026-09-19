import { useEffect, useState } from "react";
// Retro offline detector with vintage dialog signal (TODO-5.7).
export function useOfflineStatus(): boolean {
  const [offline, setOffline] = useState(false);
  useEffect(() => {
    const on = () => setOffline(!navigator.onLine);
    on();
    window.addEventListener("online", on);
    window.addEventListener("offline", on);
    return () => {
      window.removeEventListener("online", on);
      window.removeEventListener("offline", on);
    };
  }, []);
  return offline;
}
