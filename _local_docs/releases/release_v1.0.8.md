# Release v1.0.8 - The "Mobile & Stability" Update
**Date:** 2026-03-03
**Tag:** `v1.0.8`

## 📱 Mobile-First Adaptive UI
- **Bottom Navigation Bar:** Native app-like navigation for mobile devices, replacing the sidebar on small screens.
- **Adaptive Dashboards:** All statistics (Trips, Charging, Overview) now switch to a vertical Card-based view on mobile to prevent "squeezing."
- **Hero Optimization:** Redesigned the Map-Car overlay with adaptive gradients (Vertical for mobile, Horizontal for desktop) and removed "foggy" backdrop blurs for 100% clarity.
- **Responsive Settings:** Vehicle configuration cards now stack vertically on mobile.

## 🔋 Smart Polling v2.3.2
- **Infinite Stabilization Fix:** Resolved a critical logic error where the stabilization counter (used to capture final drive data) would reset to 0 for parked cars, causing them to poll every 5 minutes indefinitely.
- **Countdown Logic:** Re-engineered the post-activity buffer to use a strict countdown, ensuring the car returns to the 10-minute parked interval once data is captured.
- **Sync Protection:** Optimized the 90-second background sync to prevent it from resetting "Active" polling states.

## 🛠 Fixes & Polish
- **Charging Stats:** Implemented a responsive dual-view `StatTable` for charging power and rate metrics.
- **Z-Index Correction:** Leaflet zoom controls and "Open in Maps" buttons now sit cleanly above all transition layers.
- **Coordinates:** Position coordinates are now visible on both mobile and desktop views.

---
*Deployed from main session by M7xBeast.*
