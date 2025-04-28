import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import UserCard from '../components/UserCard'; // Компонент карточки пользователя
import '../styles/wheel.css'; // Импортируем стили для колесика

interface User {
  username: string;
  email: string;
  photo_filename: string;
}

const HomePage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const [selectedUserIndex, setSelectedUserIndex] = useState<number | null>(null);
  const limit = 8;
  const [wheelDirection, setWheelDirection] = useState<'up' | 'down' | null>(null); // Направление колесика
  const [animateWheel, setAnimateWheel] = useState(false); // Состояние для анимации колесика

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
      setWheelDirection('down');
      setAnimateWheel(true); // Активируем анимацию при изменении страницы
      setPage((prevPage) => prevPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      setWheelDirection('up');
      setAnimateWheel(true); // Активируем анимацию при изменении страницы
      setPage((prevPage) => prevPage - 1);
    }
  };

  const handleCardClick = (index: number) => {
    if (selectedUserIndex === index) {
      setSelectedUserIndex(null);
    } else {
      setSelectedUserIndex(index);
    }
  };

  // Обработчик событий клавиш
  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        handlePrevPage();
      } else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        handleNextPage();
      }
    };

    window.addEventListener('keydown', handleKeydown);

    return () => {
      window.removeEventListener('keydown', handleKeydown);
    };
  }, [page, totalUsers]);

  useEffect(() => {
    // После изменения страницы анимация должна завершиться, так как состояние wheelDirection изменяется
    const timer = setTimeout(() => {
      setAnimateWheel(false); // Останавливаем анимацию после её завершения
    }, 600); // Продолжительность анимации в 600ms

    return () => clearTimeout(timer);
  }, [page]);

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
                ? 'scale-110 z-50 rotate-y-180'
                : 'opacity-100'
            } ${selectedUserIndex !== null && selectedUserIndex !== index ? 'opacity-70 blur-sm' : ''}`}
            onClick={() => handleCardClick(index)}
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

      {/* Элемент с анимацией колеса */}
      <div className="fixed bottom-0 left-0 right-0 bg-white p-4 flex justify-center items-center border-t border-gray-200">
        <div className="relative overflow-hidden w-20 h-10 flex justify-center items-center">
          <div className="wheel-container">
            {wheelDirection === 'up' && animateWheel && (
              <div className="wheel wheel-up wheel-up-transition">
                {page}
              </div>
            )}
            {wheelDirection === 'down' && animateWheel && (
              <div className="wheel wheel-down wheel-down-transition">
                {page}
              </div>
            )}
            {/* Если анимация закончена, то просто показываем число */}
            {!animateWheel && (
              <div className="wheel">
                {page}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
