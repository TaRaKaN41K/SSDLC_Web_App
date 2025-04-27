import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import api from '../api/axios';

interface User {
  username: string;
  email: string;
  photo_filename: string;
}

const HomePage = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);

  const limit = 3;

  const fetchUsers = async (page: number) => {
    setLoading(true);
    try {
      const response = await api.get(`/user/get_all_users`, {
        params: {
          page,
          limit, 
        },
      });

      setUsers(response.data.users || []);
      setTotalUsers(response.data.total_users || 0);
      setLoading(false);

      const totalPagesCalculated = Math.ceil(response.data.total_users / limit);
      setTotalPages(totalPagesCalculated);
    } catch (err) {
      setError('Ошибка при загрузке пользователей');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers(page);
  }, [page]);

  const handleLogin = () => {
    navigate('/login');
  };

  const handleRegister = () => {
    navigate('/register');
  };

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  // Функция для формирования URL фото
  const getPhotoUrl = (photo_filename: string) => {
    return photo_filename ? `${api.defaults.baseURL}/uploads/${photo_filename}`: '/default-avatar.png'; // Путь к дефолтному фото
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Список пользователей</h1>

      <ul className="mt-4">
        {users.map((user, index) => (
          <li key={index} className="p-4 border-b">
            {user.photo_filename ? (
              <img
                src={getPhotoUrl(user.photo_filename)}
                alt={user.username}
                className="w-12 h-12 rounded-full"
              />
            ) : (
              <img
                src="/default-avatar.png" // Путь к дефолтной иконке
                alt="default"
                className="w-12 h-12 rounded-full"
              />
            )}
            <div>
              <strong>{user.username}</strong>
            </div>
            <div>{user.email}</div>
          </li>
        ))}
      </ul>

      <div className="mt-4 flex justify-between">
        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
          className="bg-blue-500 text-white px-4 py-2 rounded"
          aria-label="Предыдущая страница"
        >
          Назад
        </button>

        <span className="self-center">
          Страница {page} из {totalPages}
        </span>

        <button
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
          className="bg-blue-500 text-white px-4 py-2 rounded"
          aria-label="Следующая страница"
        >
          Вперед
        </button>
      </div>

      <div className="mb-4">
        <button
          onClick={handleLogin}
          className="bg-green-500 text-white px-4 py-2 rounded mr-2"
        >
          Войти
        </button>
        <button
          onClick={handleRegister}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Зарегистрироваться
        </button>
      </div>
    </div>
  );
};

export default HomePage;
