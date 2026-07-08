"use client";

import { Shield, ShieldOff, Loader2 } from "lucide-react";
import { useState } from "react";
import { useToggleSecureMode } from "@/lib/hooks/use-vehicles";

/**
 * Toggle for the secure_mode flag on a vehicle.
 *
 * When ON (default), the backend's SkodaTokenLifecycle will silently re-login
 * with the stored password if a refresh fails — keeping collection alive without
 * prompting the user. The cost is that the password is decrypted server-side
 * and used whenever needed.
 *
 * When OFF, a refresh failure flips the vehicle to `auth_failed` and the user
 * has to manually reconnect via the banner. Safer for users who don't trust
 * the server with their password at rest.
 */
export function SecureModeToggle({
  vehicleId,
  secureMode,
}: {
  vehicleId: string;
  secureMode: boolean;
}) {
  const toggle = useToggleSecureMode();
  const [confirming, setConfirming] = useState(false);

  if (secureMode) {
    return (
      <div className="rounded-xl border border-iv-border bg-iv-surface/50 p-4">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-iv-text">
              Silent re-auth enabled
            </p>
            <p className="text-xs text-iv-muted mt-1 leading-relaxed">
              If your saved login ever expires, iVDrive will silently re-login
              with your stored credentials. Collection keeps going without you.
            </p>
            {confirming ? (
              <div className="mt-3 flex gap-2">
                <button
                  onClick={() => {
                    toggle.mutate(
                      { vehicleId, secureMode: false },
                      { onSettled: () => setConfirming(false) }
                    );
                  }}
                  disabled={toggle.isPending}
                  className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-iv-black text-sm font-medium flex items-center gap-1.5"
                >
                  {toggle.isPending && (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  )}
                  Confirm disable
                </button>
                <button
                  onClick={() => setConfirming(false)}
                  disabled={toggle.isPending}
                  className="px-3 py-1.5 rounded-lg bg-iv-surface border border-iv-border text-sm"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => setConfirming(true)}
                className="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-iv-surface border border-iv-border hover:border-amber-500/50 text-sm"
              >
                <ShieldOff className="w-3.5 h-3.5" />
                Disable silent re-auth
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-amber-500/40 bg-amber-500/5 p-4">
      <div className="flex items-start gap-3">
        <ShieldOff className="w-5 h-5 text-amber-400 mt-0.5 shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-amber-100">
            Silent re-auth disabled
          </p>
          <p className="text-xs text-amber-200/70 mt-1 leading-relaxed">
            If your saved login ever expires, you'll need to manually reconnect
            via the banner. No silent re-authentication will happen.
          </p>
          <button
            onClick={() => toggle.mutate({ vehicleId, secureMode: true })}
            disabled={toggle.isPending}
            className="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-iv-black text-sm font-medium"
          >
            {toggle.isPending && (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            )}
            <Shield className="w-3.5 h-3.5" />
            Enable silent re-auth
          </button>
        </div>
      </div>
    </div>
  );
}