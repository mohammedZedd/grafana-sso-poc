// frontend/src/services/api.service.ts
import axios, { AxiosInstance } from 'axios';
import { User, GrafanaSession } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  setToken(token: string): void {
    this.token = token;
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  async getMe(): Promise<User> {
    const response = await this.api.get('/api/me');
    return response.data;
  }

  async testAuth(): Promise<any> {
    const response = await this.api.get('/api/test-auth');
    return response.data;
  }

  async getGrafanaUrl(): Promise<any> {
    const response = await this.api.get('/api/grafana-url');
    return response.data;
  }

  async createGrafanaSession(): Promise<GrafanaSession> {
    const response = await this.api.post('/api/create-grafana-session');
    return response.data;
  }

  async validateToken(): Promise<any> {
    const response = await this.api.post('/api/validate-token');
    return response.data;
  }
}

const apiService = new ApiService();
export default apiService;