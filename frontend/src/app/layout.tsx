import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nova Idiomas Colombia | Asistente de Admisiones",
  description:
    "Portal oficial de admisiones e idiomas con RAG híbrido y asistencia académica personalizada en tiempo real.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased bg-retroPaper text-black flex h-screen w-screen overflow-hidden">
        {children}
      </body>
    </html>
  );
}
