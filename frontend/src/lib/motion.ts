import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
// Shared GSAP setup with reduced-motion guard for propuestas lab.
let registered = false;
export function motionSetup(): boolean {
  // Register plugin once and signal disabled when reduced motion requested.
  if (!registered) {
    gsap.registerPlugin(ScrollTrigger);
    registered = true;
  }
  if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return false;
  return true;
}
// Sober mechanical easing curve used across lab timelines.
export const EASE = "power2.out";
// Standard durations in seconds for reveals and navbar transitions.
export const DUR = { fast: 0.25, base: 0.45, slow: 0.7 };
