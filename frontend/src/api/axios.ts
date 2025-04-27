import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8001',
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    console.assert(error.response?.data?.error_code)

    if (error.response?.status === 401 &&
        error.response?.data?.error_code === 4003 &&
         !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshResponse = await api.post(
            '/auth/regenerate_access',
             {},
             {withCredentials: true})
        const newAccessToken = refreshResponse.data.access_token;

        localStorage.setItem('access_token', newAccessToken);
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        console.error('Ошибка обновления токена:', refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
