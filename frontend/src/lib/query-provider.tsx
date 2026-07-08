"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useState } from "react";

/**
 * Wraps the app with @tanstack/react-query. We create the QueryClient once
 * per browser session via useState so HMR doesn't recreate it on every render.
 *
 * Defaults:
 *   - staleTime: 30s — avoids hammering our API for the same data
 *   - retry: 1 — network blips recover; doesn't hide real failures
 *   - refetchOnWindowFocus: false — the user is the one triggering revalidation
 */
export function QueryProvider({ children }: { children: ReactNode }) {
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 30_000,
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}