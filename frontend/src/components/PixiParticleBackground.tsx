"use client";

import React from "react";

export const PixiParticleBackground: React.FC = () => {
  return (
    <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
      {/* ============================================================ */}
      {/* ☁️ HIGH-DENSITY DRIFTING 16-BIT VOLUMETRIC PIXEL CLOUDS       */}
      {/* ============================================================ */}

      {/* Cloud 1: Giant Top Stratocumulus */}
      <div className="absolute top-4 left-0 animate-cloud-1 opacity-45">
        <svg width="240" height="64" viewBox="0 0 240 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="55" y="8" width="90" height="18" fill="#FAF6EE" />
          <rect x="35" y="20" width="145" height="26" fill="#FAF6EE" />
          <rect x="10" y="34" width="190" height="20" fill="#FAF6EE" />
          <rect x="100" y="4" width="55" height="14" fill="#FAF6EE" />
          <rect x="165" y="26" width="45" height="20" fill="#FAF6EE" />
          <rect x="16" y="48" width="180" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 2: Medium High Cumulus */}
      <div className="absolute top-16 left-0 animate-cloud-2 opacity-35">
        <svg width="190" height="54" viewBox="0 0 190 54" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="40" y="10" width="75" height="16" fill="#FAF6EE" />
          <rect x="22" y="20" width="118" height="22" fill="#FAF6EE" />
          <rect x="6" y="32" width="150" height="16" fill="#FAF6EE" />
          <rect x="75" y="4" width="45" height="10" fill="#FAF6EE" />
          <rect x="12" y="42" width="140" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 3: Giant Horizon Cloud Cluster */}
      <div className="absolute top-36 left-0 animate-cloud-3 opacity-30">
        <svg width="280" height="74" viewBox="0 0 280 74" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="65" y="12" width="110" height="22" fill="#FAF6EE" />
          <rect x="32" y="26" width="185" height="28" fill="#FAF6EE" />
          <rect x="10" y="42" width="240" height="24" fill="#FAF6EE" />
          <rect x="120" y="4" width="65" height="18" fill="#FAF6EE" />
          <rect x="18" y="58" width="228" height="8" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 4: Nimble Fast Cloud */}
      <div className="absolute top-12 left-0 animate-cloud-4 opacity-40">
        <svg width="150" height="44" viewBox="0 0 150 44" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="28" y="8" width="55" height="14" fill="#FAF6EE" />
          <rect x="15" y="18" width="90" height="16" fill="#FAF6EE" />
          <rect x="4" y="28" width="120" height="12" fill="#FAF6EE" />
          <rect x="9" y="36" width="112" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 5: Wide Upper Cirrus Cloud */}
      <div className="absolute top-8 left-0 animate-cloud-5 opacity-30">
        <svg width="210" height="48" viewBox="0 0 210 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="45" y="6" width="80" height="14" fill="#FAF6EE" />
          <rect x="20" y="16" width="140" height="18" fill="#FAF6EE" />
          <rect x="8" y="26" width="180" height="14" fill="#FAF6EE" />
          <rect x="14" y="36" width="170" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 6: Mid-Altitude Compact Puffy Cloud */}
      <div className="absolute top-28 left-0 animate-cloud-6 opacity-38">
        <svg width="165" height="48" viewBox="0 0 165 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="35" y="8" width="60" height="15" fill="#FAF6EE" />
          <rect x="18" y="18" width="105" height="18" fill="#FAF6EE" />
          <rect x="6" y="28" width="135" height="14" fill="#FAF6EE" />
          <rect x="10" y="38" width="128" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 7: Low Horizon Rolling Cloud */}
      <div className="absolute top-52 left-0 animate-cloud-7 opacity-22">
        <svg width="300" height="70" viewBox="0 0 300 70" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="70" y="10" width="120" height="20" fill="#FAF6EE" />
          <rect x="35" y="24" width="200" height="26" fill="#FAF6EE" />
          <rect x="12" y="38" width="260" height="22" fill="#FAF6EE" />
          <rect x="20" y="54" width="245" height="6" fill="#E8DEC8" />
        </svg>
      </div>

      {/* Cloud 8: High Speed Small Cloud */}
      <div className="absolute top-22 left-0 animate-cloud-8 opacity-35">
        <svg width="120" height="38" viewBox="0 0 120 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="20" y="6" width="45" height="12" fill="#FAF6EE" />
          <rect x="10" y="14" width="75" height="14" fill="#FAF6EE" />
          <rect x="4" y="22" width="95" height="10" fill="#FAF6EE" />
          <rect x="8" y="28" width="88" height="4" fill="#E8DEC8" />
        </svg>
      </div>

      {/* ============================================================ */}
      {/* 🦅 HIGH-DENSITY FLOCKS OF PIXEL-ART SEAGULLS                 */}
      {/* ============================================================ */}

      {/* Flock 1: V-Formation Trio (High Altitude) */}
      <div className="absolute top-14 left-0 animate-seagull-1 opacity-75">
        <div className="flex items-start gap-4">
          {/* Lead Gull */}
          <div className="mt-0">
            <svg width="32" height="14" viewBox="0 0 32 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="0" y="6" width="6" height="3" fill="#3D1C22" />
              <rect x="6" y="3" width="6" height="3" fill="#3D1C22" />
              <rect x="12" y="6" width="5" height="3" fill="#3D1C22" />
              <rect x="16" y="6" width="5" height="3" fill="#3D1C22" />
              <rect x="21" y="3" width="6" height="3" fill="#3D1C22" />
              <rect x="27" y="6" width="5" height="3" fill="#3D1C22" />
              <rect x="14" y="9" width="4" height="2" fill="#D8AF44" />
            </svg>
          </div>
          {/* Wingman Top */}
          <div className="mt-3">
            <svg width="24" height="10" viewBox="0 0 24 10" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="0" y="4" width="4" height="2" fill="#3D1C22" />
              <rect x="4" y="1" width="4" height="2" fill="#3D1C22" />
              <rect x="8" y="4" width="4" height="2" fill="#3D1C22" />
              <rect x="12" y="4" width="4" height="2" fill="#3D1C22" />
              <rect x="16" y="1" width="4" height="2" fill="#3D1C22" />
              <rect x="20" y="4" width="4" height="2" fill="#3D1C22" />
            </svg>
          </div>
          {/* Wingman Bottom */}
          <div className="mt-6">
            <svg width="20" height="9" viewBox="0 0 20 9" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="0" y="4" width="3" height="2" fill="#3D1C22" />
              <rect x="3" y="1" width="3" height="2" fill="#3D1C22" />
              <rect x="6" y="4" width="4" height="2" fill="#3D1C22" />
              <rect x="10" y="4" width="4" height="2" fill="#3D1C22" />
              <rect x="14" y="1" width="3" height="2" fill="#3D1C22" />
              <rect x="17" y="4" width="3" height="2" fill="#3D1C22" />
            </svg>
          </div>
        </div>
      </div>

      {/* Flock 2: Duo Cruisers (Mid Altitude) */}
      <div className="absolute top-32 left-0 animate-seagull-2 opacity-65">
        <div className="flex items-center gap-6">
          <svg width="28" height="12" viewBox="0 0 28 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="5" width="5" height="2" fill="#3D1C22" />
            <rect x="5" y="2" width="5" height="2" fill="#3D1C22" />
            <rect x="10" y="5" width="4" height="2" fill="#3D1C22" />
            <rect x="14" y="5" width="4" height="2" fill="#3D1C22" />
            <rect x="18" y="2" width="5" height="2" fill="#3D1C22" />
            <rect x="23" y="5" width="5" height="2" fill="#3D1C22" />
          </svg>
          <svg width="22" height="10" viewBox="0 0 22 10" fill="none" xmlns="http://www.w3.org/2000/svg" className="mt-2">
            <rect x="0" y="4" width="4" height="2" fill="#3D1C22" />
            <rect x="4" y="1" width="4" height="2" fill="#3D1C22" />
            <rect x="8" y="4" width="3" height="2" fill="#3D1C22" />
            <rect x="11" y="4" width="3" height="2" fill="#3D1C22" />
            <rect x="14" y="1" width="4" height="2" fill="#3D1C22" />
            <rect x="18" y="4" width="4" height="2" fill="#3D1C22" />
          </svg>
        </div>
      </div>

      {/* Flock 3: Solo High Glider */}
      <div className="absolute top-20 left-0 animate-seagull-3 opacity-60">
        <svg width="30" height="13" viewBox="0 0 30 13" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="5" width="5" height="3" fill="#3D1C22" />
          <rect x="5" y="2" width="5" height="3" fill="#3D1C22" />
          <rect x="10" y="5" width="5" height="3" fill="#3D1C22" />
          <rect x="15" y="5" width="5" height="3" fill="#3D1C22" />
          <rect x="20" y="2" width="5" height="3" fill="#3D1C22" />
          <rect x="25" y="5" width="5" height="3" fill="#3D1C22" />
        </svg>
      </div>

      {/* Flock 4: Low Horizon Pair */}
      <div className="absolute top-44 left-0 animate-seagull-4 opacity-55">
        <div className="flex items-center gap-3">
          <svg width="24" height="10" viewBox="0 0 24 10" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="4" width="4" height="2" fill="#3D1C22" />
            <rect x="4" y="1" width="4" height="2" fill="#3D1C22" />
            <rect x="8" y="4" width="4" height="2" fill="#3D1C22" />
            <rect x="12" y="4" width="4" height="2" fill="#3D1C22" />
            <rect x="16" y="1" width="4" height="2" fill="#3D1C22" />
            <rect x="20" y="4" width="4" height="2" fill="#3D1C22" />
          </svg>
          <svg width="18" height="8" viewBox="0 0 18 8" fill="none" xmlns="http://www.w3.org/2000/svg" className="-mt-1">
            <rect x="0" y="3" width="3" height="2" fill="#3D1C22" />
            <rect x="3" y="1" width="3" height="2" fill="#3D1C22" />
            <rect x="6" y="3" width="3" height="2" fill="#3D1C22" />
            <rect x="9" y="3" width="3" height="2" fill="#3D1C22" />
            <rect x="12" y="1" width="3" height="2" fill="#3D1C22" />
            <rect x="15" y="3" width="3" height="2" fill="#3D1C22" />
          </svg>
        </div>
      </div>

      {/* Flock 5: High Speed Darting Solo Gull */}
      <div className="absolute top-10 left-0 animate-seagull-5 opacity-50">
        <svg width="20" height="9" viewBox="0 0 20 9" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="4" width="3" height="2" fill="#3D1C22" />
          <rect x="3" y="1" width="3" height="2" fill="#3D1C22" />
          <rect x="6" y="4" width="4" height="2" fill="#3D1C22" />
          <rect x="10" y="4" width="4" height="2" fill="#3D1C22" />
          <rect x="14" y="1" width="3" height="2" fill="#3D1C22" />
          <rect x="17" y="4" width="3" height="2" fill="#3D1C22" />
        </svg>
      </div>

      {/* Flock 6: Mid-Level Companion Gull */}
      <div className="absolute top-40 left-0 animate-seagull-6 opacity-60">
        <svg width="26" height="11" viewBox="0 0 26 11" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="4" width="4" height="2" fill="#3D1C22" />
          <rect x="4" y="1" width="4" height="2" fill="#3D1C22" />
          <rect x="8" y="4" width="5" height="2" fill="#3D1C22" />
          <rect x="13" y="4" width="5" height="2" fill="#3D1C22" />
          <rect x="18" y="1" width="4" height="2" fill="#3D1C22" />
          <rect x="22" y="4" width="4" height="2" fill="#3D1C22" />
        </svg>
      </div>

      {/* ============================================================ */}
      {/* 🌴 DENSE MULTI-LAYERED PIXEL-ART PALM OASIS FORESTS          */}
      {/* ============================================================ */}

      {/* -------------------- LEFT PALM GROVE -------------------- */}

      {/* Left Palm 4: Deep Background Slender Palm */}
      <div className="absolute -bottom-8 left-28 sm:left-48 opacity-30 scale-[0.65] origin-bottom-left animate-palm-left-bg hidden md:block">
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

      {/* Left Palm 3: Mid-Depth Leaning Palm */}
      <div className="absolute -bottom-6 left-16 sm:left-28 opacity-45 scale-[0.80] origin-bottom-left animate-palm-left-mid hidden sm:block">
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

      {/* Left Palm 2: Secondary Foreground Palm */}
      <div className="absolute -bottom-6 left-4 sm:left-10 opacity-60 scale-[0.95] origin-bottom-left animate-palm-left-bg">
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

      {/* Left Palm 1: Giant Foreground Majestic Palm */}
      <div className="absolute -bottom-6 -left-6 sm:left-0 opacity-75 sm:opacity-85 scale-100 sm:scale-125 origin-bottom-left animate-palm-left">
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

      {/* -------------------- RIGHT PALM GROVE -------------------- */}

      {/* Right Palm 4: Deep Background Slender Palm */}
      <div className="absolute -bottom-8 right-28 sm:right-48 opacity-30 scale-[0.65] origin-bottom-right animate-palm-right-bg hidden md:block">
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

      {/* Right Palm 3: Mid-Depth Leaning Palm */}
      <div className="absolute -bottom-6 right-16 sm:right-28 opacity-45 scale-[0.80] origin-bottom-right animate-palm-right-mid hidden sm:block">
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

      {/* Right Palm 2: Secondary Foreground Palm */}
      <div className="absolute -bottom-6 right-4 sm:right-10 opacity-60 scale-[0.95] origin-bottom-right animate-palm-right-bg">
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

      {/* Right Palm 1: Giant Foreground Majestic Palm */}
      <div className="absolute -bottom-6 -right-6 sm:right-0 opacity-75 sm:opacity-85 scale-100 sm:scale-125 origin-bottom-right animate-palm-right">
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
    </div>
  );
};
