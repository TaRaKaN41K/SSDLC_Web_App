import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import api from '../api/axios';
import { getToken, removeToken } from '../auth/auth';


interface User {
  username: string;
  email: string;
  photo_filename: string;
}

const UserPage = () => {
  const [user, setMe] = useState<User | null>(null);
  const navigate = useNavigate();

  const handleLogout = async () => {
    const token = getToken();

    if (token) {
      try {
        await api.get('/auth/logout',);
        removeToken();
        navigate('/login');
      } catch (err) {
        console.error('Error logging out:', err);
        alert('Ошибка при выходе');
      }
    }
  };

  const handleDeleteAccount = async () => {
    const token = getToken();

    if (token) {
      try {
        await api.delete('/user/delete_account',);
        removeToken();
        navigate('/register');
      } catch (err) {
        console.error('Error deleting account:', err);
        alert('Ошибка при удалении аккаунта');
      }
    }
  };

  useEffect(() => {
    const token = getToken();

    if (token) {
      api.get('/user/me',)
        .then((res) => {
          setMe(res.data);
        })
        .catch((err) => {
          console.error('Error fetching user data:', err);
          setMe(null);
        });
    } else {
      setMe(null);
    }
  }, []);

    const getPhotoUrl = (photo_filename: string) => {
    return photo_filename ? `${api.defaults.baseURL}/uploads/${photo_filename}`: '/default-avatar.png';
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Добро пожаловать!</h1>
      {user ? (
        <div>
          {user.photo_filename ? (
            <img
              src={getPhotoUrl(user.photo_filename)}
              alt="Фото пользователя"
              className="w-32 h-32 object-cover rounded-full"
            />
          ) : (
            <img
                src="/default-avatar.png" // Путь к дефолтной иконке
                alt="default"
                className="w-12 h-12 rounded-full"
             />
          )}
          <p>Вы вошли как: {user.username}</p>
          <p>Email: {user.email}</p>

          <div className="flex flex-col gap-2 mt-4">
            <Link
              to="/edit-profile"
              className="bg-blue-500 text-white px-4 py-2 rounded text-center"
            >
              Редактировать профиль
            </Link>

            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded"
            >
              Выйти
            </button>

            <button
              onClick={handleDeleteAccount}
              className="bg-red-700 text-white px-4 py-2 rounded"
            >
              Удалить аккаунт
            </button>
          </div>
        </div>
      ) : (
        <p>Не удалось получить данные пользователя.</p>
      )}
    </div>
  );
};

export default UserPage;
