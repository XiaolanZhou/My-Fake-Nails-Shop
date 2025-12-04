// API base URL configuration
// - VITE_API_URL env var takes precedence if set
// - In production (Vercel): use empty string for same-domain API calls
// - In development: use localhost:5001

const isDev = import.meta.env.DEV === true;
const envUrl = import.meta.env.VITE_API_URL;

export const API_BASE_URL = envUrl !== undefined 
  ? envUrl 
  : (isDev ? 'http://localhost:5001' : '');

// Helper to build API endpoints
export const api = (path) => `${API_BASE_URL}${path}`;

// Debug log (remove in production)
if (isDev) {
  console.log('API_BASE_URL:', API_BASE_URL);
}
