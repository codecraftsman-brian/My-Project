import axios from 'axios';

// Create axios instance with common configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
const auth = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getUser: () => api.get('/auth/user'),
  changePassword: (passwordData) => api.post('/auth/change-password', passwordData),
  deleteAccount: (password) => api.post('/auth/delete-account', { password }),
};

// Account endpoints
const accounts = {
  getAll: () => api.get('/dashboard/accounts'),
  getAuthUrl: () => api.get('/auth/tiktok-auth-url'),
  completeAuth: (code, accountName) => api.post('/accounts/complete-auth', { code, account_name: accountName }),
  update: (id, data) => api.put(`/accounts/${id}`, data),
  delete: (id) => api.delete(`/accounts/${id}`),
  refreshToken: (id) => api.post(`/accounts/${id}/refresh-token`),
};

// Scheduler endpoints
const scheduler = {
  getPosts: (filters = {}) => api.get('/scheduler/posts', { params: filters }),
  schedulePost: (formData) => api.post('/scheduler/schedule', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  reschedulePost: (id, scheduledTime) => api.put(`/scheduler/reschedule/${id}`, { scheduled_time: scheduledTime }),
  updatePost: (id, formData) => api.put(`/scheduler/update/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  cancelPost: (id) => api.delete(`/scheduler/cancel/${id}`),
};

// Dashboard endpoints
const dashboard = {
  getStats: () => api.get('/dashboard/stats'),
  getMonthlyStats: () => api.get('/dashboard/monthly-stats'),
  getFailedPosts: () => api.get('/dashboard/failed-posts'),
  getUpcomingPosts: () => api.get('/dashboard/upcoming-posts'),
};

export default {
  auth,
  accounts,
  scheduler,
  dashboard,
};