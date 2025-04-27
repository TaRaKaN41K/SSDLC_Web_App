import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import qs from 'qs'; 

import api from '../api/axios'; 

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [photo, setPhoto] = useState<File | null>(null); // состояние для фото
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      setErrorMessage('Пароли не совпадают');
      return;
    }

    const queryParams = qs.stringify({
      username,
      email,
      password,
    });

    // Создаём FormData для файла
    const formData = new FormData();
    formData.append('photo_file', photo); // добавляем фото в FormData

    try {
      const res = await 
      api.post(`/user/create_account?${queryParams}`,
        formData,
        {headers: {'Content-Type': 'application/x-www-form-urlencoded'},}
      );

      alert('Регистрация прошла успешно. Пожалуйста, войдите.');
      navigate('/login');
    } catch (err: any) {
      console.error('Registration error:', err?.response?.data || err);

      if (err?.response?.data?.msg) {
        setErrorMessage(err.response.data.msg);
      } else {
        setErrorMessage('Ошибка регистрации. Попробуйте позже.');
      }
    }
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setPhoto(e.target.files[0]); // сохраняем выбранный файл
    }
  };

    return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Регистрация</h1>

      {errorMessage && <p className="text-red-500">{errorMessage}</p>}

      <input
        className="border p-2 w-full mb-2"
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        autoComplete="new-password"
      />
      <input
        className="border p-2 w-full mb-4"
        type="password"
        placeholder="Подтверждение пароля"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        autoComplete="new-password"
      />

      <div className="mb-4">
        <label htmlFor="photo_file" className="block mb-2">Загрузите фото</label>
        <input
          id="photo_file"
          className="border p-2 w-full"
          type="file"
          accept="image/*"
          onChange={handlePhotoChange}
        />
      </div>

      <button
        onClick={handleRegister}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
      >
        Зарегистрироваться
      </button>

      <div className="mt-4 text-center">
        <p>
          Уже есть аккаунт?{' '}
          <a href="/login" className="text-blue-500 hover:underline">
            Войти
          </a>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
