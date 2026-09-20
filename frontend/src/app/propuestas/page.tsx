"use client";
import React, { useLayoutEffect, useRef, useState } from "react";
import gsap from "gsap";
import { Header } from "../../components/Header";
import { PropuestasNavbar } from "../../components/PropuestasNavbar";
import { useGsapReveal } from "../../hooks/useGsapReveal";
import { motionSetup, EASE, DUR } from "../../lib/motion";
// Lab route comparing legacy motion stack against GSAP proposals.
export default function PropuestasPage() {
  // Reveal container for staggered lab cards on scroll.
  const labRef = useGsapReveal<HTMLDivElement>(true);
  // Visibility toggle driving both legacy and GSAP demo boxes.
  const [show, setShow] = useState(true);
  // Box animated imperatively with a reusable GSAP timeline.
  const gsapBox = useRef<HTMLDivElement | null>(null);
  // Counter proving single shared action source in the new navbar.
  const [clicks, setClicks] = useState(0);
  const bump = () => setClicks((c) => c + 1);
  useLayoutEffect(() => {
    // Mirror toggle state with GSAP transform and opacity only.
    if (!gsapBox.current || !motionSetup()) return;
    gsap.to(gsapBox.current, { scale: show ? 1 : 0.6, opacity: show ? 1 : 0, duration: DUR.fast, ease: EASE, overwrite: "auto" });
  }, [show]);
  const actions = [
    // Shared actions rendered in desktop row and mobile menu.
    { id: "nuevo", label: "Nuevo Chat", onSelect: bump },
    { id: "menu", label: "Menu (0)", onSelect: bump },
    { id: "telemetria", label: "Telemetria", onSelect: bump },
    { id: "monitor", label: "Monitor", onSelect: bump },
  ];
  return (
    <div className="min-h-screen bg-retroPaper text-black">
      <div className="border-b-2 border-black bg-black text-white px-4 py-2 text-xs font-mono">
        Laboratorio /propuestas: comparativa motion actual vs GSAP + navbar
      </div>
      <section className="px-4 pt-4">
        <h1 className="font-display text-lg font-extrabold">Navbar actual (legacy)</h1>
        <p className="text-xs font-mono opacity-70">Doble botonera por breakpoint, reloj 1s, sin menu movil.</p>
        <div className="mt-2 border-2 border-black">
          <Header />
        </div>
      </section>
      <section className="px-4 pt-6">
        <h1 className="font-display text-lg font-extrabold">Navbar propuesto (GSAP)</h1>
        <p className="text-xs font-mono opacity-70">Fuente unica de acciones, hamburguesa con aria-expanded, clicks: {clicks}.</p>
        <div className="mt-2 border-2 border-black">
          <PropuestasNavbar actions={actions} breadcrumb="Admisiones / Comparativa" clock="31 AGO 1997" />
        </div>
      </section>
      <div ref={labRef} className="px-4 py-6 grid gap-4 md:grid-cols-2">
        <article data-reveal className="border-2 border-black bg-retroBeige p-3">
          <h2 className="font-bold text-sm">Animacion legacy (CSS)</h2>
          <button onClick={() => setShow((v) => !v)} className="mt-2 border border-black px-2 py-0.5 text-xs">
            Alternar
          </button>
          <div
            className={`mt-3 h-16 bg-vicePink border border-black transition-all duration-300 ${show ? "opacity-100 translate-y-0" : "opacity-0 translate-y-3"}`}
          />
        </article>
        <article data-reveal className="border-2 border-black bg-retroBeige p-3">
          <h2 className="font-bold text-sm">Animacion propuesta (GSAP)</h2>
          <button onClick={() => setShow((v) => !v)} className="mt-2 border border-black px-2 py-0.5 text-xs">
            Alternar
          </button>
          <div ref={gsapBox} className="mt-3 h-16 bg-viceCyan border border-black" />
        </article>
        <article data-reveal className="border-2 border-black bg-retroBeige p-3 md:col-span-2">
          <h2 className="font-bold text-sm">Tabla comparativa</h2>
          <table className="mt-2 w-full text-[11px] font-mono border border-black">
            <thead>
              <tr className="bg-black text-white">
                <th className="p-1 text-left">Eje</th>
                <th className="p-1 text-left">Actual</th>
                <th className="p-1 text-left">Propuesto</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-black">
                <td className="p-1">Motor</td>
                <td className="p-1">CSS transition por componente</td>
                <td className="p-1">GSAP ticker unico, transform y opacity</td>
              </tr>
              <tr className="border-t border-black">
                <td className="p-1">Navbar movil</td>
                <td className="p-1">Botones duplicados md:hidden</td>
                <td className="p-1">Hamburguesa con aria-expanded</td>
              </tr>
              <tr className="border-t border-black">
                <td className="p-1">Reloj</td>
                <td className="p-1">setInterval 1s</td>
                <td className="p-1">Formato 30s memoizado</td>
              </tr>
              <tr className="border-t border-black">
                <td className="p-1">Accesibilidad</td>
                <td className="p-1">Sin expanded ni skip</td>
                <td className="p-1">Respeta reduced-motion</td>
              </tr>
            </tbody>
          </table>
        </article>
      </div>
    </div>
  );
}
