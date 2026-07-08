"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export interface Vehicle {
  id: string;
  display_name: string | null;
  manufacturer: string | null;
  model: string | null;
  model_year: string | null;
  collection_enabled: boolean;
  active_interval_seconds: number;
  parked_interval_seconds: number;
  image_url: string | null;
  connector_status: string | null;
  last_error_text?: string | null;
  needs_user_reauth_reason?: string | null;
  secure_mode?: boolean;
  consecutive_auth_failures?: number;
  last_auth_at?: string | null;
  last_auth_method?: string | null;
  created_at: string;
}

export interface VehicleStatus {
  vin_last4?: string;
  display_name?: string;
  manufacturer?: string;
  model?: string;
  image_url?: string | null;
  latest_battery_level: number | null;
  latest_range_km: number | null;
  latest_charging_state: string | null;
  latest_vehicle_state: string | null;
  latest_position: { latitude: number; longitude: number } | null;
  last_updated: string | null;
  is_online?: boolean | null;
  doors_locked?: string | null;
  connector_status?: string | null;
  odometer_km?: number | null;
  model_year?: string | null;
}

/** Fetches the full vehicle list (incl. auth lifecycle fields). */
export function useVehicles() {
  return useQuery<Vehicle[]>({
    queryKey: ["vehicles"],
    queryFn: () => api.getVehicles(),
    // Auth lifecycle state changes only when the backend tells us — refetch on focus
    // is wasteful here. The manual-refresh action will explicitly invalidate.
    refetchInterval: 60_000,
  });
}

/** Fetches a single vehicle's connector status (lighter endpoint). */
export function useVehicleStatus(vehicleId: string | null) {
  return useQuery<VehicleStatus | null>({
    queryKey: ["vehicle-status", vehicleId],
    queryFn: async () => {
      if (!vehicleId) return null;
      return api.getVehicleStatus(vehicleId);
    },
    enabled: !!vehicleId,
    refetchInterval: 60_000,
  });
}

/** Forces an immediate collector cycle for this vehicle. */
export function useManualRefresh() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vehicleId: string) => api.refreshVehicle(vehicleId),
    onSuccess: () => {
      // After the collector cycle, vehicle list will reflect new auth state.
      // Refetch in 3s to give the collector time to process the queue.
      setTimeout(() => qc.invalidateQueries({ queryKey: ["vehicles"] }), 3_000);
    },
  });
}

/** Toggles secure_mode for a single vehicle. */
export function useToggleSecureMode() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ vehicleId, secureMode }: { vehicleId: string; secureMode: boolean }) =>
      api.updateVehicle(vehicleId, { secure_mode: secureMode }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["vehicles"] }),
  });
}

/** Toggles collection_enabled for a vehicle. */
export function useToggleCollection() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ vehicleId, enabled }: { vehicleId: string; enabled: boolean }) =>
      api.updateVehicle(vehicleId, { collection_enabled: enabled }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["vehicles"] }),
  });
}

/** Deletes a vehicle. */
export function useDeleteVehicle() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vehicleId: string) => api.deleteVehicle(vehicleId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["vehicles"] }),
  });
}