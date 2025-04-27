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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const limit = 3; // Количество пользователей на страницу

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
    } catch (err) {
      setError('Ошибка при загрузке пользователей');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers(page);
  }, [page]);

  const handleNextPage = () => {
    if (page < Math.ceil(totalUsers / limit)) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      setPage((prevPage) => prevPage - 1);
    }
  };

  // Функция для формирования URL фото
  const getPhotoUrl = (photo_filename: string) => {
    return photo_filename
      ? `${api.defaults.baseURL}/uploads/${photo_filename}`
      : '/default-avatar.png';  // Путь к дефолтному фото
  };

  if (loading && page === 1) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="p-4 mb-20">
      <h1 className="text-xl font-bold">Список пользователей</h1>

      <div className="mt-4">
        {users.map((user, index) => (
          <div key={index} className="p-4 border-b">
            {user.photo_filename ? (
              <img
                src={getPhotoUrl(user.photo_filename)}
                alt={user.username}
                className="w-12 h-12 rounded-full"
              />
            ) : (
              <img
                src="/default-avatar.png"  // Путь к дефолтной иконке
                alt="default"
                className="w-12 h-12 rounded-full"
              />
            )}
            <div>
              <strong>{user.username}</strong>
            </div>
            <div>{user.email}</div>
          </div>
        ))}
      </div>

      {/* Кнопки навигации с фиксированным положением */}
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 flex justify-between w-full max-w-md">
        <button
          onClick={handlePrevPage}
          disabled={page === 1}
          className="bg-blue-500 text-white px-4 py-2 rounded w-1/3"
        >
          &#8593;
        </button>

        <span className="self-center text-center w-1/3">
          {page} / {Math.ceil(totalUsers / limit)}
        </span>

        <button
          onClick={handleNextPage}
          disabled={page === Math.ceil(totalUsers / limit)}
          className="bg-blue-500 text-white px-4 py-2 rounded w-1/3"
        >
          &#8595;
        </button>
      </div>
    </div>
  );
};

export default HomePage;
