"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const AppContent = dynamic(() => import("@/components/AppContent"), { ssr: false });

/**
 * Renders empty shell until after client mount, then AppContent (ThemeProvider + AuthProvider + children).
 * AppContent is ssr: false so the server never sends that tree → avoids #418 hydration mismatch.
 */
export function ClientHydrationGate({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) {
    return <div className="min-h-screen bg-iv-black" />;
  }
  return <AppContent>{children}</AppContent>;
}
