import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
       // Simple implementation for now. In a full system, you would try to refresh the token here.
       if (typeof window !== "undefined" && !window.location.pathname.startsWith('/login')) {
           localStorage.removeItem('token');
           window.location.href = '/login';
       }
    }
    return Promise.reject(error);
  }
);
