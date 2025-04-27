// src/components/LoginForm.tsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import qs from 'qs';
import api from '../api/axios';
import { saveToken } from '../auth/auth';
import { handleError } from '../utils/error_handler';
import CustomInput from '../components/CustomInput';
import CustomButton from '../components/CustomButton';
import ErrorAlert from '../components/ErrorAlert';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

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
    <div className="p-6 max-w-md mx-auto bg-white rounded-lg shadow-lg border border-gray-200 mt-16 space-y-4">
      <h2 className="text-center mb-6 text-2xl font-semibold text-gray-800">Войти в аккаунт</h2>

      {errorMessage && <ErrorAlert message={errorMessage} size="medium"/>}

      <CustomInput
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        rounded={true}
        size="medium"
      />

      <CustomInput
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        icon={true}
        rounded={true}
        size="medium"
      />

      <CustomButton
        onClick={handleLogin}
        text="Войти"
        size="medium"
        color="blue"
        loading={false}
      />

      <div className="mt-4 text-center">
        <p className="text-center text-sm text-gray-700">
          Нет аккаунта?{' '}
          <Link
            to="/register"
            className="inline-block text-blue-600 hover:text-blue-800 px-4 py-2 rounded-lg relative transition-all duration-300"
          >
            Зарегистрироваться
            <span className="absolute bottom-0 left-0 w-full h-1 bg-blue-600 scale-x-0 transition-all duration-300 transform hover:scale-x-100"></span>
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;
