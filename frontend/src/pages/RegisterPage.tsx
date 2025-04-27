import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import qs from 'qs';
import api from '../api/axios';
import { handleError } from '../utils/error_handler';
import CustomInput from '../components/CustomInput';
import CustomButton from '../components/CustomButton';
import ErrorAlert from '../components/ErrorAlert';

const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [photo, setPhoto] = useState<File | null>(null);
  const navigate = useNavigate();

  
  const handleRegister = async () => {
    if (password !== confirmPassword) {
      setErrorMessage('Пароли не совпадают');
      return;
    }
    else if (!username || !password || !email || !confirmPassword) {
      setErrorMessage('Введите все поля');
      return;
    }

    const queryParams = qs.stringify({
      username,
      email,
      password,
    });

    // Создаём FormData для файла
    const formData = new FormData();
    if (photo) {
      formData.append('photo_file', photo);
    }

    try {
      const res = await api.post(`/user/create_account?${queryParams}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      navigate('/login');
    } catch (err: any) {
      console.error('Registration error:', err?.response?.data || err);

      // Если ошибка приходит от сервера с сообщением
      if (err?.response?.data?.msg) {
        setErrorMessage(err.response.data.msg);
      } else {
        setErrorMessage('Ошибка регистрации. Попробуйте позже.');
      }
    }
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setPhoto(e.target.files[0]);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-lg shadow-lg border border-gray-200 mt-16 space-y-4">
      <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Регистрация</h1>

      {errorMessage && <ErrorAlert message={errorMessage} size="medium"/>}

      <CustomInput
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        size="medium"
        rounded={true}
      />
      <CustomInput
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        size="medium"
        rounded={true}
      />
      <CustomInput
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        autoComplete="new-password"
        icon={true}
        rounded={true}
        size="medium"
      />
      <CustomInput
        type="password"
        placeholder="Подтверждение пароля"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        autoComplete="new-password"
        icon={true}
        rounded={true}
        size="medium"
      />

      <div className="mb-6">
        <label htmlFor="photo_file" className="block mb-2 text-sm text-gray-600">Загрузите фото</label>
        <input
          id="photo_file"
          className="border p-2 w-full rounded-md"
          type="file"
          accept="image/*"
          onChange={handlePhotoChange}
        />
      </div>

      <CustomButton onClick={handleRegister} text="Зарегистрироваться" size="medium" color="blue" loading={false} />

      <div className="mt-4 text-center">
        <p className="text-sm text-gray-700">
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
