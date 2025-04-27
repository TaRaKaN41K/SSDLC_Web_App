import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import qs from 'qs';

import api from '../api/axios';
import { saveToken, getToken } from './auth';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();

    if (token) {
      api.get('/user/me',)
      .then(() => {
        navigate('/user');
      })
      .catch((error) => {
        console.log('Токен недействителен или истёк', error);
      });
    }
  }, [navigate]);

  const handleLogin = async () => {
    try {
      const data = qs.stringify({ username, password });

      const res = await api.post(
        '/auth/login',
        data,
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      saveToken(res.data.access_token);
      navigate('/user');
    } catch (error) {
      console.error('Login error:', error.response ? error.response.data : error);
      alert('Ошибка входа');
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <input
        className="border p-2 w-full mb-2"
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        autoComplete="current-password"
      />
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
      >
        Войти
      </button>
    </div>
  );
};

export default LoginPage;
