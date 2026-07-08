# Release v1.1.3 - 🔑 Authentication & Frontend Architecture Refactor

This release introduces a major authentication architecture overhaul and modernizes the frontend data fetching layer to resolve persistent API anti-bot rejection issues and transient backend server errors.

---

## 🚀 Key Improvements

### 🛡️ Authentication anti-bot 403s & 500s Resilience
The backend data collector now effectively distinguishes between transient server errors (500s) and hard authorization rejections (403s/401s). The internal token lifecycle state machine has been upgraded to handle silent re-logins using securely stored credentials whenever access is rejected by anti-bot measures. This enables the system to reliably bypass strict token expiry limits without dropping the connection.

### ⚡ Dashboard Data Fetching via TanStack Query
The legacy `useState` & `useEffect` data fetching patterns on the vehicle dashboard have been completely replaced with `@tanstack/react-query`. This modernizes the frontend stack, ensures the UI stays fresh without causing unnecessary re-renders or "stuck" loading states, and significantly improves maintainability.

### 🧩 In-card Auth Strategy UI
Authentication methods and connector error indicators have been moved directly inside the vehicle card title row. This provides immediate, right-aligned context regarding the last successful connection type (e.g. "refresh", "silent login") and any active transient errors directly where users expect to see them.

### 🔐 Manual Re-authentication UI
A new contextual banner seamlessly prompts users to re-enter credentials specifically when the backend flags that manual intervention is required. Upon successful re-authentication, React Query instantly invalidates the local cache, clearing the banner and resuming live data flow without requiring a manual page reload.

### 🧹 React Hook Dependency Fixes
Resolved numerous existing React Doctor `rules-of-hooks` errors, `useEffect` callback syncing loops, and `exhaustive-deps` warnings on the main dashboard components, contributing to a healthier and more predictable frontend codebase.

---

## 🛠️ Technical Details
- **Frontend Health**: React Doctor score improved significantly due to the removal of legacy anti-patterns in the dashboard.
- **Database Schema**: A new migration was added to include a `force_login_next` column in the `connector_sessions` table, replacing the fragile in-memory flag.
- **New Endpoints**: Added the `POST /api/v1/vehicles/{id}/reauthenticate` endpoint to handle secure manual credential submissions and immediate state invalidation.
