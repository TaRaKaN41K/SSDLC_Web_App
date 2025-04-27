import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import UserCard from '../components/UserCard'; // Компонент карточки пользователя

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
  const [selectedUserIndex, setSelectedUserIndex] = useState<number | null>(null); // Состояние для выбранной карточки
  const limit = 8; // Количество пользователей на страницу (обновлено для плитки)

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

  const handleCardClick = (index: number) => {
    if (selectedUserIndex === index) {
      setSelectedUserIndex(null); // Если кликаем на уже выбранную карточку, сбрасываем выбор
    } else {
      setSelectedUserIndex(index); // Выбираем новую карточку
    }
  };

  // Функция для формирования URL фото
  const getPhotoUrl = (photo_filename: string) => {
    return photo_filename
      ? `${api.defaults.baseURL}/uploads/${photo_filename}`
      : '/default-avatar.png'; // Путь к дефолтному фото
  };

  if (loading && page === 1) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="p-4 mb-20">
      <h1 className="text-xl font-bold text-center mb-6">Список пользователей</h1>

      {/* Отображаем пользователей в плитке */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {users.map((user, index) => (
          <div
            key={index}
            className={`transition-all duration-500 transform perspective-1000 ${
              selectedUserIndex === index
                ? 'scale-110 z-50 rotate-y-180' // Переворачиваем выбранную карточку
                : 'opacity-100' // Все остальные карточки без размытия
            } ${selectedUserIndex !== null && selectedUserIndex !== index ? 'opacity-70 blur-sm' : ''}`} // Размываем все карточки, кроме выбранной
            onClick={() => handleCardClick(index)} // Обработчик клика
          >
            <div
              className={`card-inner ${selectedUserIndex === index ? 'rotate-y-180' : ''} transition-transform duration-500`}
            >
              <UserCard
                username={user.username}
                email={user.email}
                photoFilename={user.photo_filename}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Кнопки навигации */}
      <div className="flex justify-between mt-6">
        <button
          onClick={handlePrevPage}
          disabled={page === 1}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          &#8593;
        </button>

        <span className="self-center">
          Страница {page} / {Math.ceil(totalUsers / limit)}
        </span>

        <button
          onClick={handleNextPage}
          disabled={page === Math.ceil(totalUsers / limit)}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          &#8595;
        </button>
      </div>
    </div>
  );
};

export default HomePage;
