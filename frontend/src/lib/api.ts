import axios from "axios";

export const API_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/v1";

export const api = axios.create({ baseURL: API_URL });

// login/register/refresh must never carry a (possibly stale) Authorization
// header — SimpleJWT rejects the whole request before the view runs.
const PUBLIC_AUTH = /\/auth\/(login|register|refresh)$/;

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token && !PUBLIC_AUTH.test(config.url ?? "")) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, drop tokens and send the user back to login (FR: expired token → login)
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (
      error.response?.status === 401 &&
      !error.config?.url?.includes("/auth/")
    ) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
