import React from "react";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { RetroDesktop } from "../components/RetroDesktop";

export default function Home() {
  return (
    <div className="relative flex flex-col w-full h-full min-h-screen overflow-hidden z-10 select-none">
      {/* Top 90s OS Menu Bar */}
      <Header />

      {/* Main Interactive Desktop Workspace (Client boundary isolated) */}
      <RetroDesktop />

      {/* Bottom Retro Application Dock */}
      <Footer />
    </div>
  );
}
