const API_BASE_URL = import.meta.env.API_URL || "http://localhost:8000";

export const API_URL = API_BASE_URL.replace(/\/$/, "");
