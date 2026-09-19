"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { motionSetup, EASE, DUR } from "../lib/motion";
// Delegated hover and press animation for buttons inside a container.
export function useGsapHoverGroup<T extends HTMLElement>() {
  // Ref attached to the container holding animated buttons.
  const ref = useRef<T | null>(null);
  useLayoutEffect(() => {
    // Delegate hover through mouseover to cover dynamically added buttons.
    const root = ref.current;
    if (!root || !motionSetup()) return;
    const pick = (e: Event) => (e.target as HTMLElement).closest?.("button:not([disabled])");
    const over = (e: MouseEvent) => {
      // Lift button slightly with tighter shadow on hover enter.
      const b = pick(e);
      if (!b) return;
      gsap.to(b, { y: -1, scale: 1.02, duration: DUR.fast, ease: EASE, overwrite: "auto" });
    };
    const out = (e: MouseEvent) => {
      // Restore button resting position on hover leave.
      const b = pick(e);
      if (!b) return;
      gsap.to(b, { y: 0, scale: 1, duration: DUR.fast, ease: EASE, overwrite: "auto" });
    };
    const down = (e: MouseEvent) => {
      // Press button down for tactile retro feedback.
      const b = pick(e);
      if (!b) return;
      gsap.to(b, { y: 1, scale: 0.98, duration: 0.1, ease: EASE, overwrite: "auto" });
    };
    root.addEventListener("mouseover", over);
    root.addEventListener("mouseout", out);
    root.addEventListener("mousedown", down);
    // Release delegated listeners on unmount.
    return () => {
      root.removeEventListener("mouseover", over);
      root.removeEventListener("mouseout", out);
      root.removeEventListener("mousedown", down);
    };
  }, []);
  return ref;
}
