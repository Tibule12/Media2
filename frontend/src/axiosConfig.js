import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add a request interceptor to set Authorization header dynamically
axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('idToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
      console.log('Setting Authorization header:', config.headers['Authorization']);
    } else {
      console.log('No token found in localStorage');
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle 401 Unauthorized globally
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      console.log('Unauthorized! Redirecting to login.');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
