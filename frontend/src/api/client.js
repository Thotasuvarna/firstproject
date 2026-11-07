/**
 * API Client for Fake Review & Network Detector Backend.
 */
// Use relative path so Vite dev-server proxy handles CORS correctly.
// In production build, the backend serves the frontend directly.
const BASE_URL = '/api/v1';

export function getAuthToken() {
  return localStorage.getItem('access_token');
}

export function setAuthSession(token, user) {
  localStorage.setItem('access_token', token);
  localStorage.setItem('user_profile', JSON.stringify(user));
}

export function clearAuthSession() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_profile');
}

export function getStoredUser() {
  const raw = localStorage.getItem('user_profile');
  try {
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

async function request(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    ...(options.headers || {})
  };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (!res.ok) {
    let errorDetail = 'Request failed';
    try {
      const errJson = await res.json();
      const detail = errJson.detail;
      errorDetail = Array.isArray(detail)
        ? detail.map((item) => item.msg || 'Request failed').join(', ')
        : detail || errorDetail;
    } catch {
      errorDetail = res.statusText;
    }
    throw new Error(errorDetail);
  }

  const contentType = res.headers.get('content-type');
  if (contentType && contentType.includes('application/pdf')) {
    return res.blob();
  }

  return res.json();
}

export const api = {
  // Auth
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const data = await request('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString()
    });
    setAuthSession(data.access_token, { id: data.user_id, email: data.email, role: data.role });
    return data;
  },

  async register(email, password, fullName) {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name: fullName })
    });
  },

  async getMe() {
    return request('/auth/me');
  },

  // Dashboard
  async getMetrics() {
    return request('/dashboard/metrics');
  },

  // Products
  async getProducts() {
    return request('/products');
  },

  async createProduct(product) {
    return request('/products', {
      method: 'POST',
      body: JSON.stringify(product)
    });
  },

  // Reviews
  async getReviews(params = {}) {
    const query = new URLSearchParams(params).toString();
    return request(`/reviews${query ? `?${query}` : ''}`);
  },

  async submitReview(review) {
    return request('/reviews', {
      method: 'POST',
      body: JSON.stringify(review)
    });
  },

  async uploadCSV(file) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/reviews/upload-csv', {
      method: 'POST',
      body: formData
    });
  },

  // Network & Graph
  async getNetworkGraph(minShared = 1) {
    return request(`/graph/network?min_shared=${minShared}`);
  },

  async getCollusionClusters() {
    return request('/graph/clusters');
  },

  // Auditing & Reports
  async recordAuditAction(action) {
    return request('/reports/audit-action', {
      method: 'POST',
      body: JSON.stringify(action)
    });
  },

  async downloadPDF() {
    const blob = await request('/reports/pdf');
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Forensic_Audit_Report_${new Date().toISOString().slice(0, 10)}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
};
