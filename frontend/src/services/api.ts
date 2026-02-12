import axios from 'axios';

// Empty string = same origin (production behind nginx); undefined = dev default
const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

// Auth Interfaces
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  refresh_token?: string;
  user?: User;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor to add Bearer token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor to handle 401s
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      // Ideally implement refresh token logic here. 
      // For now, we will clear storage and redirect to login if refresh fails or isn't implemented.
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface UploadResponse {
  session_id: string;
  filename: string;
  status: string;
  uploaded_at: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  logs?: string | null;
}

export interface SessionInfo {
  session_id: string;
  filename: string;
  uploaded_at: string;
  file_size?: number;
}

export const uploadDocument = async (formData: FormData): Promise<UploadResponse> => {
  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const sendMessage = async (sessionId: string, message: string): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/api/chat', {
    session_id: sessionId,
    message: message,
  });
  return response.data;
};

export const getSession = async (sessionId: string): Promise<SessionInfo> => {
  const response = await api.get<SessionInfo>(`/api/sessions/${sessionId}`);
  return response.data;
};

export const deleteSession = async (sessionId: string): Promise<{ status: string; session_id: string }> => {
  const response = await api.delete<{ status: string; session_id: string }>(`/api/sessions/${sessionId}`);
  return response.data;
};

export const listSessions = async (): Promise<{ sessions: SessionInfo[]; count: number }> => {
  const response = await api.get<{ sessions: SessionInfo[]; count: number }>('/api/sessions');
  return response.data;
};

// --- Auth API ---

export const login = async (credentials: any): Promise<AuthResponse> => {
  // Backend expects JSON body with { email, password }
  const response = await api.post<AuthResponse>('/api/auth/login', {
    email: credentials.email,
    password: credentials.password
  });
  return response.data;
};

export const signup = async (data: any): Promise<User> => {
  const response = await api.post<User>('/api/auth/signup', data);
  return response.data;
};

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>('/api/auth/me');
  return response.data;
};

export const forgotPassword = async (email: string): Promise<any> => {
  const response = await api.post('/api/auth/forgot-password', { email });
  return response.data;
};

export const resetPassword = async (data: any): Promise<any> => {
  const response = await api.post('/api/auth/reset-password', data);
  return response.data;
};

// --- Payment API ---

export interface CreateOrderRequest {
  amount: number;
  currency?: string;
  description?: string;
}

export interface CaptureOrderRequest {
  order_id: string;
}

export interface PaymentOrder {
  order_id: string;
  order: any;
  payment?: any;
}

export const createPaymentOrder = async (data: CreateOrderRequest): Promise<PaymentOrder> => {
  const response = await api.post<PaymentOrder>('/api/payments/create-order', data);
  return response.data;
};

export const capturePaymentOrder = async (data: CaptureOrderRequest): Promise<any> => {
  const response = await api.post('/api/payments/capture-order', data);
  return response.data;
};

export const getPaymentOrder = async (orderId: string): Promise<any> => {
  const response = await api.get(`/api/payments/order/${orderId}`);
  return response.data;
};

// --- Newsletter API ---

export const subscribeNewsletter = async (email: string): Promise<{ success: boolean; message: string }> => {
  const response = await api.post('/api/newsletter/subscribe', { email });
  return response.data;
};


