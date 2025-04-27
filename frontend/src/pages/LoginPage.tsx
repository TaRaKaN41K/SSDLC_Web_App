import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import qs from 'qs';
import api from '../api/axios';
import { getToken, saveToken } from '../auth/auth';
import { handleError } from '../utils/error_handler'; // Импортируем обработчик ошибок

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  // Check if the user is already logged in
  useEffect(() => {
    const token = getToken();

    if (token) {
      api.get('/user/me')
        .then(() => {
          navigate('/user');
        })
        .catch((error) => {
          console.log('Invalid token', error);
        });
    }
  }, [navigate]);

  // Function to handle login
  const handleLogin = async () => {
    if (!username || !password) {
      setErrorMessage('Пожалуйста, заполните оба поля.');
      return;
    }

    try {
      const data = qs.stringify({ username, password });

      const res = await api.post(
        '/auth/login',
        data,
        {
          withCredentials: true,
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
      );

      saveToken(res.data.access_token);
      navigate('/user');
    } catch (error: any) {
      const errorText = handleError(error);
      setErrorMessage(errorText);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Войти в аккаунт</h1>

      {errorMessage && (
        <div className="text-red-500 mb-4">
          <strong>{errorMessage}</strong>
        </div>
      )}

      <input
        className="border p-2 w-full mb-2"
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-4"
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

      {/* Ссылка на страницу регистрации */}
      <div className="mt-4 text-center">
        <p>
          Нет аккаунта?{' '}
          <Link to="/register" className="text-blue-500 hover:underline">
            Зарегистрироваться
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
