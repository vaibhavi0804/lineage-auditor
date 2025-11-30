/**
 * API client for communicating with FastAPI backend.
 */
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handler
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const datasets = {
  list: () => api.get('/datasets'),
  get: (id) => api.get(`profiles/${id}/latest`),
  upload: (file, name) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name || file.name);
    return api.post('/datasets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const profiles = {
  list: (datasetId) => api.get(`/profiles/${datasetId}`),
  latest: (datasetId) => api.get(`/profiles/${datasetId}/latest`),
};

export const issues = {
  list: () => api.get('/issues'),
  byDataset: (datasetId) => api.get(`/issues/dataset/${datasetId}`),
};

export const lineage = {
  get: (datasetId) => api.get(`/lineage/${datasetId}`),
};

export default api;
