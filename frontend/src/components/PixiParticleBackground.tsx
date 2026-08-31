"use client";

import React from "react";

interface PixelSeagullProps {
  size?: "lg" | "md" | "sm";
  color?: string;
  beakColor?: string;
  className?: string;
}

const PixelSeagull: React.FC<PixelSeagullProps> = ({
  size = "md",
  color = "#3D1C22",
  beakColor = "#D8AF44",
  className = "",
}) => {
  if (size === "lg") {
    return (
      <div className={`relative inline-block w-[32px] h-[14px] ${className}`}>
        {/* Frame 1: Wings Up */}
        <svg className="absolute inset-0 animate-wing-up" width="32" height="14" viewBox="0 0 32 14" fill="none">
          <rect x="0" y="3" width="6" height="3" fill={color} />
          <rect x="6" y="5" width="6" height="3" fill={color} />
          <rect x="12" y="7" width="8" height="3" fill={color} />
          <rect x="20" y="5" width="6" height="3" fill={color} />
          <rect x="26" y="3" width="6" height="3" fill={color} />
          <rect x="14" y="9" width="4" height="2" fill={beakColor} />
        </svg>
        {/* Frame 2: Wings Down */}
        <svg className="absolute inset-0 animate-wing-down" width="32" height="14" viewBox="0 0 32 14" fill="none">
          <rect x="0" y="9" width="6" height="3" fill={color} />
          <rect x="6" y="6" width="6" height="3" fill={color} />
          <rect x="12" y="4" width="8" height="3" fill={color} />
          <rect x="20" y="6" width="6" height="3" fill={color} />
          <rect x="26" y="9" width="6" height="3" fill={color} />
          <rect x="14" y="6" width="4" height="2" fill={beakColor} />
        </svg>
      </div>
    );
  }

  if (size === "sm") {
    return (
      <div className={`relative inline-block w-[18px] h-[8px] ${className}`}>
        {/* Frame 1: Wings Up */}
        <svg className="absolute inset-0 animate-wing-up" width="18" height="8" viewBox="0 0 18 8" fill="none">
          <rect x="0" y="1" width="3" height="2" fill={color} />
          <rect x="3" y="3" width="3" height="2" fill={color} />
          <rect x="6" y="4" width="6" height="2" fill={color} />
          <rect x="12" y="3" width="3" height="2" fill={color} />
          <rect x="15" y="1" width="3" height="2" fill={color} />
        </svg>
        {/* Frame 2: Wings Down */}
        <svg className="absolute inset-0 animate-wing-down" width="18" height="8" viewBox="0 0 18 8" fill="none">
          <rect x="0" y="5" width="3" height="2" fill={color} />
          <rect x="3" y="3" width="3" height="2" fill={color} />
          <rect x="6" y="2" width="6" height="2" fill={color} />
          <rect x="12" y="3" width="3" height="2" fill={color} />
          <rect x="15" y="5" width="3" height="2" fill={color} />
        </svg>
      </div>
    );
  }

  return (
    <div className={`relative inline-block w-[24px] h-[10px] ${className}`}>
      {/* Frame 1: Wings Up */}
      <svg className="absolute inset-0 animate-wing-up" width="24" height="10" viewBox="0 0 24 10" fill="none">
        <rect x="0" y="2" width="4" height="2" fill={color} />
        <rect x="4" y="4" width="4" height="2" fill={color} />
        <rect x="8" y="5" width="8" height="2" fill={color} />
        <rect x="16" y="4" width="4" height="2" fill={color} />
        <rect x="20" y="2" width="4" height="2" fill={color} />
      </svg>
      {/* Frame 2: Wings Down */}
      <svg className="absolute inset-0 animate-wing-down" width="24" height="10" viewBox="0 0 24 10" fill="none">
        <rect x="0" y="7" width="4" height="2" fill={color} />
        <rect x="4" y="5" width="4" height="2" fill={color} />
        <rect x="8" y="3" width="8" height="2" fill={color} />
        <rect x="16" y="5" width="4" height="2" fill={color} />
        <rect x="20" y="7" width="4" height="2" fill={color} />
      </svg>
    </div>
  );
};

export const PixiParticleBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none select-none overflow-hidden z-0">
      {/* Drifting 16-bit volumetric pixel clouds (Bidirectional: Left-to-Right & Right-to-Left) */}

      {/* Cloud 1: Giant Top Stratocumulus (L2R) */}
      <div className="absolute top-4 left-0 animate-cloud-l2r-1 opacity-45">
        <svg width="240" height="64" viewBox="0 0 240 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="55" y="8" width="90" height="18" fill="#FAF6EE" />
          <rect x="35" y="20" width="145" height="26" fill="#FAF6EE" />
          <rect x="10" y="34" width="190" height="20" fill="#FAF6EE" />
          <rect x="100" y="4" width="55" height="14" fill="#FAF6EE" />
          <rect x="165" y="26" width="45" height="20" fill="#FAF6EE" />
          <rect x="16" y="48" width="180" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 2: Medium High Cumulus (R2L) */}
      <div className="absolute top-16 left-0 animate-cloud-r2l-1 opacity-35">
        <svg width="190" height="54" viewBox="0 0 190 54" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="40" y="10" width="75" height="16" fill="#FAF6EE" />
          <rect x="22" y="20" width="118" height="22" fill="#FAF6EE" />
          <rect x="6" y="32" width="150" height="16" fill="#FAF6EE" />
          <rect x="75" y="4" width="45" height="10" fill="#FAF6EE" />
          <rect x="12" y="42" width="140" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 3: Giant Horizon Cloud Cluster (L2R) */}
      <div className="absolute top-36 left-0 animate-cloud-l2r-2 opacity-30">
        <svg width="280" height="74" viewBox="0 0 280 74" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="65" y="12" width="110" height="22" fill="#FAF6EE" />
          <rect x="32" y="26" width="185" height="28" fill="#FAF6EE" />
          <rect x="10" y="42" width="240" height="24" fill="#FAF6EE" />
          <rect x="120" y="4" width="65" height="18" fill="#FAF6EE" />
          <rect x="18" y="58" width="228" height="8" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 4: Nimble Fast Cloud (R2L) */}
      <div className="absolute top-12 left-0 animate-cloud-r2l-2 opacity-40">
        <svg width="150" height="44" viewBox="0 0 150 44" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="28" y="8" width="55" height="14" fill="#FAF6EE" />
          <rect x="15" y="18" width="90" height="16" fill="#FAF6EE" />
          <rect x="4" y="28" width="120" height="12" fill="#FAF6EE" />
          <rect x="9" y="36" width="112" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 5: Wide Upper Cirrus Cloud (L2R) */}
      <div className="absolute top-8 left-0 animate-cloud-l2r-3 opacity-30">
        <svg width="210" height="48" viewBox="0 0 210 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="45" y="6" width="80" height="14" fill="#FAF6EE" />
          <rect x="20" y="16" width="140" height="18" fill="#FAF6EE" />
          <rect x="8" y="26" width="180" height="14" fill="#FAF6EE" />
          <rect x="14" y="36" width="170" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 6: Mid-Altitude Compact Puffy Cloud (R2L) */}
      <div className="absolute top-28 left-0 animate-cloud-r2l-3 opacity-38">
        <svg width="165" height="48" viewBox="0 0 165 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="35" y="8" width="60" height="15" fill="#FAF6EE" />
          <rect x="18" y="18" width="105" height="18" fill="#FAF6EE" />
          <rect x="6" y="28" width="135" height="14" fill="#FAF6EE" />
          <rect x="10" y="38" width="128" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 7: Low Horizon Rolling Cloud (L2R) */}
      <div className="absolute top-52 left-0 animate-cloud-l2r-4 opacity-22">
        <svg width="300" height="70" viewBox="0 0 300 70" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="70" y="10" width="120" height="20" fill="#FAF6EE" />
          <rect x="35" y="24" width="200" height="26" fill="#FAF6EE" />
          <rect x="12" y="38" width="260" height="22" fill="#FAF6EE" />
          <rect x="20" y="54" width="245" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 8: High Speed Small Cloud (R2L) */}
      <div className="absolute top-22 left-0 animate-cloud-r2l-4 opacity-35">
        <svg width="120" height="38" viewBox="0 0 120 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="20" y="6" width="45" height="12" fill="#FAF6EE" />
          <rect x="10" y="14" width="75" height="14" fill="#FAF6EE" />
          <rect x="4" y="22" width="95" height="10" fill="#FAF6EE" />
          <rect x="8" y="28" width="88" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 9: Upper Wispy Cirrus (L2R) */}
      <div className="absolute top-2 left-0 animate-cloud-l2r-5 opacity-32">
        <svg width="200" height="46" viewBox="0 0 200 46" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="42" y="6" width="72" height="13" fill="#FAF6EE" />
          <rect x="18" y="15" width="128" height="17" fill="#FAF6EE" />
          <rect x="6" y="26" width="168" height="13" fill="#FAF6EE" />
          <rect x="12" y="36" width="158" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 10: Small Fast Puff (R2L) */}
      <div className="absolute top-6 left-0 animate-cloud-r2l-5 opacity-30">
        <svg width="140" height="40" viewBox="0 0 140 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="26" y="7" width="52" height="12" fill="#FAF6EE" />
          <rect x="12" y="16" width="88" height="14" fill="#FAF6EE" />
          <rect x="4" y="26" width="112" height="10" fill="#FAF6EE" />
          <rect x="8" y="33" width="105" height="3" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 11: Mid Upper Dense (L2R) */}
      <div className="absolute top-10 left-0 animate-cloud-l2r-6 opacity-38">
        <svg width="180" height="50" viewBox="0 0 180 50" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="38" y="8" width="66" height="14" fill="#FAF6EE" />
          <rect x="16" y="18" width="118" height="18" fill="#FAF6EE" />
          <rect x="4" y="30" width="150" height="14" fill="#FAF6EE" />
          <rect x="10" y="40" width="140" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 12: Broad High Stratocumulus (R2L) */}
      <div className="absolute top-14 left-0 animate-cloud-r2l-6 opacity-28">
        <svg width="260" height="62" viewBox="0 0 260 62" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="58" y="10" width="100" height="17" fill="#FAF6EE" />
          <rect x="28" y="22" width="168" height="23" fill="#FAF6EE" />
          <rect x="8" y="36" width="222" height="18" fill="#FAF6EE" />
          <rect x="16" y="50" width="210" height="5" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 13: Tiny Low Drift (L2R) */}
      <div className="absolute top-20 left-0 animate-cloud-l2r-7 opacity-25">
        <svg width="130" height="36" viewBox="0 0 130 36" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="22" y="6" width="48" height="10" fill="#FAF6EE" />
          <rect x="10" y="14" width="82" height="13" fill="#FAF6EE" />
          <rect x="4" y="23" width="105" height="9" fill="#FAF6EE" />
          <rect x="8" y="29" width="98" height="3" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 14: Mid Horizon Wide (R2L) */}
      <div className="absolute top-24 left-0 animate-cloud-r2l-7 opacity-33">
        <svg width="220" height="52" viewBox="0 0 220 52" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="46" y="8" width="84" height="15" fill="#FAF6EE" />
          <rect x="20" y="18" width="142" height="19" fill="#FAF6EE" />
          <rect x="6" y="30" width="186" height="15" fill="#FAF6EE" />
          <rect x="12" y="41" width="176" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 15: Lower Mid Puffy (L2R) */}
      <div className="absolute top-32 left-0 animate-cloud-l2r-8 opacity-27">
        <svg width="160" height="42" viewBox="0 0 160 42" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="30" y="7" width="58" height="12" fill="#FAF6EE" />
          <rect x="14" y="16" width="102" height="15" fill="#FAF6EE" />
          <rect x="4" y="26" width="132" height="11" fill="#FAF6EE" />
          <rect x="9" y="34" width="124" height="3" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 16: Compact Upper-Mid (R2L) */}
      <div className="absolute top-40 left-0 animate-cloud-r2l-8 opacity-36">
        <svg width="175" height="46" viewBox="0 0 175 46" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="34" y="7" width="62" height="13" fill="#FAF6EE" />
          <rect x="16" y="17" width="112" height="17" fill="#FAF6EE" />
          <rect x="4" y="27" width="145" height="12" fill="#FAF6EE" />
          <rect x="10" y="36" width="136" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 17: Very Low Horizon Massive (L2R) */}
      <div className="absolute top-56 left-0 animate-cloud-l2r-9 opacity-20">
        <svg width="290" height="68" viewBox="0 0 290 68" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="66" y="10" width="116" height="19" fill="#FAF6EE" />
          <rect x="32" y="23" width="196" height="25" fill="#FAF6EE" />
          <rect x="10" y="37" width="254" height="21" fill="#FAF6EE" />
          <rect x="18" y="53" width="240" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 18: High Thin Cirrus (R2L) */}
      <div className="absolute top-48 left-0 animate-cloud-r2l-9 opacity-31">
        <svg width="150" height="38" viewBox="0 0 150 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="28" y="6" width="52" height="11" fill="#FAF6EE" />
          <rect x="12" y="14" width="90" height="13" fill="#FAF6EE" />
          <rect x="4" y="23" width="118" height="10" fill="#FAF6EE" />
          <rect x="9" y="30" width="110" height="3" fill="#E8DEC8" />
        </svg>
      </div>

      {/* High-density flocks of pixel-art seagulls (Bidirectional + 2-State Flapping) */}

      {/* Flock 1: V-Formation Trio (High Altitude, Left-to-Right) */}
      <div className="absolute top-14 left-0 animate-seagull-l2r-1 opacity-75">
        <div className="flex items-start gap-4">
          <PixelSeagull size="lg" />
          <PixelSeagull size="md" className="mt-3" />
          <PixelSeagull size="sm" className="mt-6" />
        </div>
      </div>

      {/* Flock 2: Duo Cruisers (Mid Altitude, Right-to-Left) */}
      <div className="absolute top-32 left-0 animate-seagull-r2l-1 opacity-65">
        <div className="flex items-center gap-6">
          <PixelSeagull size="lg" />
          <PixelSeagull size="md" className="mt-2" />
        </div>
      </div>

      {/* Flock 3: Solo High Glider (Left-to-Right) */}
      <div className="absolute top-20 left-0 animate-seagull-l2r-2 opacity-60">
        <PixelSeagull size="lg" />
      </div>

      {/* Flock 4: Low Horizon Pair (Right-to-Left) */}
      <div className="absolute top-44 left-0 animate-seagull-r2l-2 opacity-55">
        <div className="flex items-center gap-3">
          <PixelSeagull size="md" />
          <PixelSeagull size="sm" className="-mt-1" />
        </div>
      </div>

      {/* Flock 5: High Speed Darting Solo Gull (Left-to-Right) */}
      <div className="absolute top-10 left-0 animate-seagull-l2r-3 opacity-50">
        <PixelSeagull size="sm" />
      </div>

      {/* Flock 6: Mid-Level Companion Gull (Right-to-Left) */}
      <div className="absolute top-40 left-0 animate-seagull-r2l-3 opacity-60">
        <PixelSeagull size="md" />
      </div>

      {/* Left palm grove */}

      {/* Left Palm 4: Deep Background Slender Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 left-28 sm:left-48 opacity-30 scale-[0.85] origin-bottom-left animate-palm-left-bg hidden md:block">
        <svg width="240" height="320" viewBox="0 0 240 320" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="90" y="270" width="18" height="50" fill="#240E12" />
          <rect x="94" y="220" width="16" height="52" fill="#240E12" />
          <rect x="100" y="170" width="15" height="52" fill="#240E12" />
          <rect x="108" y="120" width="14" height="52" fill="#240E12" />
          <rect x="118" y="70" width="12" height="52" fill="#240E12" />
          <rect x="65" y="45" width="55" height="12" fill="#182A1F" />
          <rect x="20" y="55" width="50" height="12" fill="#182A1F" />
          <rect x="114" y="10" width="16" height="55" fill="#1E3527" />
          <rect x="125" y="40" width="60" height="12" fill="#182A1F" />
          <rect x="180" y="55" width="45" height="12" fill="#182A1F" />
        </svg>
      </div>

      {/* Left Palm 3: Mid-Depth Leaning Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 left-16 sm:left-28 opacity-45 scale-[1.0] origin-bottom-left animate-palm-left-mid hidden sm:block">
        <svg width="260" height="340" viewBox="0 0 260 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="100" y="290" width="22" height="50" fill="#2E1418" />
          <rect x="104" y="240" width="20" height="52" fill="#2E1418" />
          <rect x="110" y="190" width="18" height="52" fill="#2E1418" />
          <rect x="118" y="140" width="16" height="52" fill="#2E1418" />
          <rect x="128" y="90" width="14" height="52" fill="#2E1418" />
          <rect x="70" y="65" width="60" height="14" fill="#1C3024" />
          <rect x="25" y="75" width="55" height="14" fill="#1C3024" />
          <rect x="125" y="30" width="18" height="60" fill="#243C2E" />
          <rect x="135" y="60" width="65" height="14" fill="#1C3024" />
          <rect x="190" y="75" width="50" height="14" fill="#1C3024" />
        </svg>
      </div>

      {/* Left Palm 2: Secondary Foreground Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 left-4 sm:left-10 opacity-60 scale-[1.15] origin-bottom-left animate-palm-left-bg">
        <svg width="270" height="360" viewBox="0 0 270 360" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="85" y="300" width="24" height="60" fill="#35181D" />
          <rect x="90" y="240" width="22" height="64" fill="#35181D" />
          <rect x="98" y="180" width="20" height="64" fill="#35181D" />
          <rect x="108" y="125" width="18" height="60" fill="#35181D" />
          <rect x="120" y="75" width="16" height="55" fill="#35181D" />
          <rect x="68" y="55" width="55" height="15" fill="#263E2F" />
          <rect x="24" y="66" width="50" height="15" fill="#263E2F" />
          <rect x="120" y="22" width="16" height="60" fill="#2E4B39" />
          <rect x="132" y="50" width="60" height="15" fill="#263E2F" />
          <rect x="185" y="62" width="48" height="15" fill="#263E2F" />
        </svg>
      </div>

      {/* Left Palm 1: Giant Foreground Majestic Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 -left-6 sm:left-0 opacity-75 sm:opacity-85 scale-100 sm:scale-[1.55] origin-bottom-left animate-palm-left">
        <svg width="300" height="380" viewBox="0 0 300 380" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="95" y="320" width="26" height="60" fill="#3D1C22" />
          <rect x="100" y="260" width="24" height="64" fill="#3D1C22" />
          <rect x="108" y="200" width="22" height="64" fill="#3D1C22" />
          <rect x="118" y="140" width="20" height="64" fill="#3D1C22" />
          <rect x="130" y="85" width="18" height="60" fill="#3D1C22" />
          <rect x="93" y="340" width="6" height="6" fill="#241014" />
          <rect x="98" y="280" width="6" height="6" fill="#241014" />
          <rect x="106" y="220" width="6" height="6" fill="#241014" />
          {/* Fronds */}
          <rect x="75" y="65" width="60" height="16" fill="#2E4A38" />
          <rect x="30" y="76" width="55" height="16" fill="#2E4A38" />
          <rect x="0" y="92" width="38" height="18" fill="#2E4A38" />
          <rect x="65" y="86" width="65" height="14" fill="#243D2D" />
          <rect x="18" y="104" width="52" height="16" fill="#243D2D" />
          <rect x="130" y="30" width="18" height="65" fill="#3A5E47" />
          <rect x="125" y="10" width="16" height="26" fill="#3A5E47" />
          <rect x="120" y="0" width="12" height="16" fill="#3A5E47" />
          <rect x="142" y="60" width="65" height="16" fill="#2E4A38" />
          <rect x="198" y="70" width="58" height="16" fill="#2E4A38" />
          <rect x="248" y="88" width="40" height="18" fill="#2E4A38" />
          <rect x="140" y="82" width="60" height="14" fill="#243D2D" />
          <rect x="192" y="98" width="50" height="16" fill="#243D2D" />
        </svg>
      </div>

      {/* Right palm grove */}

      {/* Right Palm 4: Deep Background Slender Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 right-28 sm:right-48 opacity-30 scale-[0.85] origin-bottom-right animate-palm-right-bg hidden md:block">
        <svg width="240" height="320" viewBox="0 0 240 320" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="132" y="270" width="18" height="50" fill="#240E12" />
          <rect x="130" y="220" width="16" height="52" fill="#240E12" />
          <rect x="125" y="170" width="15" height="52" fill="#240E12" />
          <rect x="118" y="120" width="14" height="52" fill="#240E12" />
          <rect x="110" y="70" width="12" height="52" fill="#240E12" />
          <rect x="120" y="45" width="55" height="12" fill="#182A1F" />
          <rect x="170" y="55" width="50" height="12" fill="#182A1F" />
          <rect x="110" y="10" width="16" height="55" fill="#1E3527" />
          <rect x="55" y="40" width="60" height="12" fill="#182A1F" />
          <rect x="15" y="55" width="45" height="12" fill="#182A1F" />
        </svg>
      </div>

      {/* Right Palm 3: Mid-Depth Leaning Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 right-16 sm:right-28 opacity-45 scale-[1.0] origin-bottom-right animate-palm-right-mid hidden sm:block">
        <svg width="260" height="340" viewBox="0 0 260 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="138" y="290" width="22" height="50" fill="#2E1418" />
          <rect x="134" y="240" width="20" height="52" fill="#2E1418" />
          <rect x="128" y="190" width="18" height="52" fill="#2E1418" />
          <rect x="120" y="140" width="16" height="52" fill="#2E1418" />
          <rect x="110" y="90" width="14" height="52" fill="#2E1418" />
          <rect x="125" y="65" width="60" height="14" fill="#1C3024" />
          <rect x="175" y="75" width="55" height="14" fill="#1C3024" />
          <rect x="112" y="30" width="18" height="60" fill="#243C2E" />
          <rect x="55" y="60" width="65" height="14" fill="#1C3024" />
          <rect x="15" y="75" width="50" height="14" fill="#1C3024" />
        </svg>
      </div>

      {/* Right Palm 2: Secondary Foreground Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 right-4 sm:right-10 opacity-60 scale-[1.15] origin-bottom-right animate-palm-right-bg">
        <svg width="270" height="360" viewBox="0 0 270 360" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="160" y="300" width="24" height="60" fill="#35181D" />
          <rect x="156" y="240" width="22" height="64" fill="#35181D" />
          <rect x="150" y="180" width="20" height="64" fill="#35181D" />
          <rect x="142" y="125" width="18" height="60" fill="#35181D" />
          <rect x="132" y="75" width="16" height="55" fill="#35181D" />
          <rect x="145" y="55" width="55" height="15" fill="#263E2F" />
          <rect x="195" y="66" width="50" height="15" fill="#263E2F" />
          <rect x="134" y="22" width="16" height="60" fill="#2E4B39" />
          <rect x="75" y="50" width="60" height="15" fill="#263E2F" />
          <rect x="35" y="62" width="48" height="15" fill="#263E2F" />
        </svg>
      </div>

      {/* Right Palm 1: Giant Foreground Majestic Palm - scaled up, bottom-0 like grass */}
      <div className="absolute bottom-0 -right-6 sm:right-0 opacity-75 sm:opacity-85 scale-100 sm:scale-[1.55] origin-bottom-right animate-palm-right">
        <svg width="300" height="380" viewBox="0 0 300 380" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="175" y="320" width="26" height="60" fill="#3D1C22" />
          <rect x="170" y="260" width="24" height="64" fill="#3D1C22" />
          <rect x="162" y="200" width="22" height="64" fill="#3D1C22" />
          <rect x="152" y="140" width="20" height="64" fill="#3D1C22" />
          <rect x="140" y="85" width="18" height="60" fill="#3D1C22" />
          <rect x="195" y="340" width="6" height="6" fill="#241014" />
          <rect x="190" y="280" width="6" height="6" fill="#241014" />
          <rect x="180" y="220" width="6" height="6" fill="#241014" />
          {/* Fronds */}
          <rect x="160" y="65" width="60" height="16" fill="#2E4A38" />
          <rect x="210" y="76" width="55" height="16" fill="#2E4A38" />
          <rect x="258" y="92" width="38" height="18" fill="#2E4A38" />
          <rect x="165" y="86" width="65" height="14" fill="#243D2D" />
          <rect x="224" y="104" width="52" height="16" fill="#243D2D" />
          <rect x="145" y="30" width="18" height="65" fill="#3A5E47" />
          <rect x="150" y="10" width="16" height="26" fill="#3A5E47" />
          <rect x="160" y="0" width="12" height="16" fill="#3A5E47" />
          <rect x="90" y="60" width="65" height="16" fill="#2E4A38" />
          <rect x="40" y="70" width="58" height="16" fill="#2E4A38" />
          <rect x="6" y="88" width="40" height="18" fill="#2E4A38" />
          <rect x="95" y="82" width="60" height="14" fill="#243D2D" />
          <rect x="52" y="98" width="50" height="16" fill="#243D2D" />
        </svg>
      </div>

      {/* Tropical Pixel-Art Grass Layer - Verde Seco Retro (fixed to viewport bottom) */}
      <div className="fixed bottom-0 left-0 w-screen h-[48px] sm:h-[54px] pointer-events-none z-[5] overflow-hidden">
        {/* Static continuous base */}
        <div className="absolute bottom-0 left-0 w-full h-[14px] sm:h-[16px] bg-[#8A9A6A] border-t-[2px] border-black/60" />
        <div className="absolute bottom-[14px] sm:bottom-[16px] left-0 w-full h-[3px] bg-[#A8B88E] opacity-80" />
        <div className="absolute bottom-[14px] sm:bottom-[16px] left-0 w-full h-[2px] bg-[#6B7D5A] opacity-60" style={{ marginTop: "3px" }} />
        {/* Swaying tufts row - only tufts animate, base stays static */}
        <div className="absolute bottom-[14px] sm:bottom-[16px] left-0 w-full h-[34px] sm:h-[38px] flex items-end justify-between px-1 sm:px-3 gap-[1px] sm:gap-[2px]">
          {[18, 26, 14, 22, 28, 16, 24, 20, 30, 15, 26, 18, 22, 28, 16, 24, 20, 26, 14, 30, 18, 22, 16, 28, 20, 24, 18, 26].map((h, i) => (
            <div
              key={i}
              className="animate-grass flex-shrink-0 hidden sm:flex"
              style={{ animationDelay: `${(i * 0.18) % 2.8}s`, animationDuration: `${3.2 + (i % 4) * 0.4}s` } as React.CSSProperties}
            >
              <svg width="14" height={h} viewBox={`0 0 14 ${h}`} fill="none" xmlns="http://www.w3.org/2000/svg" className="block">
                <rect x="2" y={h - 10} width="2" height="10" fill={i % 3 === 0 ? "#6B7D5A" : i % 3 === 1 ? "#8A9A6A" : "#9AB08A"} />
                <rect x="6" y={h - h} width="3" height={h} fill={i % 2 === 0 ? "#8A9A6A" : "#A8B88E"} />
                <rect x="10" y={h - 12} width="2" height="12" fill={i % 3 === 2 ? "#6B7D5A" : "#7A8F5A"} />
                <rect x="6" y={h - h} width="3" height="3" fill="#B8C8A0" opacity="0.7" />
              </svg>
            </div>
          ))}
          {/* Mobile: fewer tufts */}
          {[18, 26, 14, 22, 28, 16, 24, 20, 30, 15, 26, 18].map((h, i) => (
            <div
              key={`m-${i}`}
              className="animate-grass flex-shrink-0 flex sm:hidden"
              style={{ animationDelay: `${(i * 0.22) % 2.5}s` } as React.CSSProperties}
            >
              <svg width="12" height={h} viewBox={`0 0 12 ${h}`} fill="none" xmlns="http://www.w3.org/2000/svg" className="block">
                <rect x="1" y={h - 9} width="2" height="9" fill="#6B7D5A" />
                <rect x="5" y={h - h} width="3" height={h} fill="#8A9A6A" />
                <rect x="9" y={h - 11} width="2" height="11" fill="#7A8F5A" />
              </svg>
            </div>
          ))}
        </div>
        {/* Dense ground pixel texture */}
        <div
          className="absolute bottom-0 left-0 w-full h-[14px] sm:h-[16px] opacity-30 pointer-events-none"
          style={{
            backgroundImage: `repeating-linear-gradient(90deg, transparent 0px, transparent 6px, rgba(0,0,0,0.15) 6px, rgba(0,0,0,0.15) 7px)`,
          }}
        />
      </div>
    </div>
  );
};
