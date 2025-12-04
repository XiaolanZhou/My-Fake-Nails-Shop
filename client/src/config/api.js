// API base URL
// - In development: http://localhost:5001
// - On Vercel: empty string (same domain, relative paths work)
// - Custom backend: set VITE_API_URL
export const API_BASE_URL = import.meta.env.VITE_API_URL ?? 
  (import.meta.env.DEV ? 'http://localhost:5001' : '');

// Helper to build API endpoints
export const api = (path) => `${API_BASE_URL}${path}`;
