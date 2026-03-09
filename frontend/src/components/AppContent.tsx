"use client";

import { ThemeProvider } from "@/lib/theme-provider";
import { AuthProvider } from "@/lib/auth-context";

/**
 * Wraps ThemeProvider + AuthProvider. Loaded with ssr: false so the server
 * never sends this tree → no hydration mismatch (#418) from theme/auth.
 */
export default function AppContent({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <AuthProvider>{children}</AuthProvider>
    </ThemeProvider>
  );
}
