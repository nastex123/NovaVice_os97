"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { motionSetup, EASE, DUR } from "../lib/motion";
// Reveal hook applying fade and slide once per element via ScrollTrigger.
export function useGsapReveal<T extends HTMLElement>(enabled = true) {
  // Ref attached to the animated container element.
  const ref = useRef<T | null>(null);
  useLayoutEffect(() => {
    // Skip animation when disabled or reduced motion is preferred.
    if (!enabled || !ref.current || !motionSetup()) return;
    const ctx = gsap.context(() => {
      // Batch animate direct children with stagger on scroll enter.
      gsap.fromTo(
        "[data-reveal]",
        { y: 12, opacity: 0 },
        { y: 0, opacity: 1, duration: DUR.base, ease: EASE, stagger: 0.08, overwrite: "auto" }
      );
    }, ref);
    // Release GSAP context and ScrollTriggers on unmount.
    return () => ctx.revert();
  }, [enabled]);
  return ref;
}
