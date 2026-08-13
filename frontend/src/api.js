// ==== SOZLAMALAR ====
// Backend deploy qilingandan so'ng .env faylida VITE_API_BASE ni almashtiring
// (qarang: .env.example)
export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// ==== TELEGRAM WEBAPP INIT ====
export const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
}
export const initData = tg?.initData || "";

// ==== TOKEN (localStorage) ====
const TOKEN_KEY = "kitobjavon_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export function isLoggedIn() {
  return Boolean(getToken() || initData);
}

function authHeaders() {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (initData) headers["X-Telegram-Init-Data"] = initData;
  return headers;
}

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} xato: ${res.status}`);
  return res.json();
}

export async function apiAuthed(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...authHeaders(),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const msg =
      err.detail ||
      (Array.isArray(err.non_field_errors) ? err.non_field_errors[0] : null) ||
      (typeof err === "object" ? Object.values(err).flat()?.[0] : null) ||
      `So'rov xato: ${res.status}`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return res.json();
}

export async function apiRegister({ phone, password, full_name }) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, password, full_name }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg =
      data.detail ||
      data.phone?.[0] ||
      data.password?.[0] ||
      data.non_field_errors?.[0] ||
      "Ro'yxatdan o'tishda xatolik";
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  setToken(data.token);
  return data;
}

export async function apiLogin({ phone, password }) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg =
      data.detail ||
      data.non_field_errors?.[0] ||
      data.phone?.[0] ||
      "Kirishda xatolik";
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  setToken(data.token);
  return data;
}

export function apiLogout() {
  setToken("");
}
