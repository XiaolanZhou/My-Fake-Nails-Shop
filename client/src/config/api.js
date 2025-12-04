// API base URL - uses environment variable in production, localhost in development
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

// Helper to build API endpoints
export const api = (path) => `${API_BASE_URL}${path}`;
