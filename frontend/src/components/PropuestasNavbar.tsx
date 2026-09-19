"use client";
import React, { useLayoutEffect, useRef, useState } from "react";
import gsap from "gsap";
import { motionSetup, EASE, DUR } from "../lib/motion";
// New navbar proposal with hamburger menu and single action source.
export interface NavbarAction {
  // Stable identifier for the navbar action.
  id: string;
  // Visible label rendered in desktop and mobile menus.
  label: string;
  // Click handler dispatched by both menu variants.
  onSelect: () => void;
}
interface Props {
  // Actions shared by desktop row and mobile dropdown.
  actions: NavbarAction[];
  // Active topic breadcrumb shown at the center.
  breadcrumb: string;
  // Clock string rendered on the right side.
  clock: string;
}
export const PropuestasNavbar: React.FC<Props> = ({ actions, breadcrumb, clock }) => {
  // Open state for the mobile dropdown menu.
  const [open, setOpen] = useState(false);
  // Root element animated on mount with a sober slide.
  const rootRef = useRef<HTMLElement | null>(null);
  // Dropdown panel animated with height and fade on toggle.
  const panelRef = useRef<HTMLDivElement | null>(null);
  useLayoutEffect(() => {
    // Animate navbar entrance once when motion is allowed.
    if (!rootRef.current || !motionSetup()) return;
    const ctx = gsap.context(() => {
      // Slide navbar down slightly while fading in.
      gsap.fromTo(rootRef.current, { y: -10, opacity: 0 }, { y: 0, opacity: 1, duration: DUR.base, ease: EASE, overwrite: "auto" });
    }, rootRef);
    // Clean GSAP context on unmount to free memory.
    return () => ctx.revert();
  }, []);
  useLayoutEffect(() => {
    // Animate dropdown open and close with fade and slide.
    if (!panelRef.current || !motionSetup()) return;
    gsap.to(panelRef.current, { height: open ? "auto" : 0, opacity: open ? 1 : 0, duration: DUR.fast, ease: EASE, overwrite: "auto" });
  }, [open ]);
  return (
    <header ref={rootRef} className="h-auto border-b-2 border-black bg-retroBeige px-3 py-1.5 z-30 text-xs font-bold text-black">
      <div className="flex items-center justify-between gap-2">
        <span className="font-display tracking-wider font-extrabold">NOVA OS 97</span>
        <nav className="hidden md:flex items-center gap-1 text-[11px] uppercase" aria-label="Principal">
          {actions.map((a) => (
            <button key={a.id} onClick={a.onSelect} className="hover:bg-black hover:text-white px-2 py-0.5">
              {a.label}
            </button>
          ))}
        </nav>
        <span className="hidden lg:inline font-mono text-[11px]">{breadcrumb}</span>
        <div className="flex items-center gap-2">
          <span className="hidden sm:inline font-mono text-[11px]">{clock}</span>
          <button onClick={() => setOpen((v) => !v)} aria-expanded={open} aria-label="Abrir menu" className="md:hidden border border-black px-2 py-0.5">
            {open ? "Cerrar" : "Menu"}
          </button>
        </div>
      </div>
      <div ref={panelRef} style={{ height: 0, opacity: 0, overflow: "hidden" }} className="md:hidden">
        <nav className="flex flex-col py-1" aria-label="Movil">
          {actions.map((a) => (
            <button
              key={a.id}
              onClick={() => {
                a.onSelect();
                setOpen(false);
              }}
              className="text-left px-2 py-1 hover:bg-black hover:text-white uppercase text-[11px]"
            >
              {a.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};
