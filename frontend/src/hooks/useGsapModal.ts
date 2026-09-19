"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { motionSetup, EASE, DUR } from "../lib/motion";
// Shared entrance animation for retro modals replacing framer-motion.
export function useGsapModal<T extends HTMLElement>(open: boolean) {
  // Ref attached to the animated modal panel element.
  const ref = useRef<T | null>(null);
  useLayoutEffect(() => {
    // Animate scale and fade on open when motion is allowed.
    if (!open || !ref.current || !motionSetup()) return;
    const ctx = gsap.context(() => {
      // Sober pop-in with slight rise for retro windows.
      gsap.fromTo(ref.current, { opacity: 0, scale: 0.96, y: 10 }, { opacity: 1, scale: 1, y: 0, duration: DUR.base, ease: EASE, overwrite: "auto" });
    }, ref);
    // Release GSAP context on close or unmount.
    return () => ctx.revert();
  }, [open]);
  return ref;
}
