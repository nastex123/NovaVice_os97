import type { Metadata } from "next";
import "./globals.css";
import { PixiParticleBackground } from "../components/PixiParticleBackground";

export const metadata: Metadata = {
  title: "Nova Tech University | Asistente Inteligente de Admisiones (RAG)",
  description:
    "Portal oficial de admisiones impulsado por RAG en Python y OpenCode con navegación interactiva y consultas en tiempo real.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className="antialiased bg-background text-slate-100 flex h-screen w-screen overflow-hidden">
        <PixiParticleBackground />
        {children}
      </body>
    </html>
  );
}
