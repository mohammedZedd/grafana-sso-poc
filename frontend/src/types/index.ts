// frontend/src/types/index.ts
export interface User {
  sub: string;
  email: string;
  name: string;
  picture?: string;
  token?: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
  timestamp?: string;
}

export interface GrafanaSession {
  session_created: boolean;
  session_id: string;
  user: string;
  expires_in: number;
}