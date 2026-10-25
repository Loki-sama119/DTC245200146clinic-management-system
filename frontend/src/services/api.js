// ==============================================================================
// CLINIC MANAGEMENT — API CLIENT & TOKEN MANAGER
// ==============================================================================

const API_BASE = '/api';

class ApiService {
  constructor() {
    this.accessToken = localStorage.getItem('clinic_access_token');
    this.refreshToken = localStorage.getItem('clinic_refresh_token');
    this.currentUser = JSON.parse(localStorage.getItem('clinic_user') || 'null');
  }

  setSession(access, refresh, user) {
    this.accessToken = access;
    this.refreshToken = refresh;
    this.currentUser = user;
    localStorage.setItem('clinic_access_token', access);
    localStorage.setItem('clinic_refresh_token', refresh);
    localStorage.setItem('clinic_user', JSON.stringify(user));
  }

  clearSession() {
    this.accessToken = null;
    this.refreshToken = null;
    this.currentUser = null;
    localStorage.removeItem('clinic_access_token');
    localStorage.removeItem('clinic_refresh_token');
    localStorage.removeItem('clinic_user');
  }

  isAuthenticated() {
    return !!this.accessToken && !!this.currentUser;
  }

  getUser() {
    return this.currentUser;
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      let response = await fetch(url, { ...options, headers });

      // Nếu token hết hạn (401), thử refresh token một lần
      if (response.status === 401 && this.refreshToken && !endpoint.includes('/auth/login') && !endpoint.includes('/auth/token/refresh')) {
        const refreshed = await this.refreshAccessToken();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this.accessToken}`;
          response = await fetch(url, { ...options, headers });
        } else {
          this.clearSession();
          window.location.hash = '#/login';
          throw new Error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.');
        }
      }

      if (!response.ok) {
        let errData = {};
        try {
          errData = await response.json();
        } catch (_) {}
        const errorMsg = errData.detail || errData.message || JSON.stringify(errData) || `Lỗi HTTP ${response.status}`;
        throw new Error(errorMsg);
      }

      // 204 No Content
      if (response.status === 204) return null;

      return await response.json();
    } catch (err) {
      console.error(`[API Error] ${endpoint}:`, err);
      throw err;
    }
  }

  async refreshAccessToken() {
    try {
      const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: this.refreshToken })
      });
      if (res.ok) {
        const data = await res.json();
        this.accessToken = data.access;
        localStorage.setItem('clinic_access_token', data.access);
        return true;
      }
    } catch (e) {
      console.error('Refresh token failed:', e);
    }
    return false;
  }

  async login(username, password) {
    const res = await this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    this.setSession(res.access, res.refresh, res.user);
    return res.user;
  }

  logout() {
    this.clearSession();
    window.location.hash = '#/login';
  }

  // Generic CRUD helpers
  get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(query ? `${endpoint}?${query}` : endpoint, { method: 'GET' });
  }

  post(endpoint, data = {}) {
    return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) });
  }

  put(endpoint, data = {}) {
    return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export const api = new ApiService();
