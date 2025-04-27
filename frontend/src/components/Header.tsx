import React from 'react';
import { Link } from 'react-router-dom';
import { getToken } from '../auth/auth'; // Импортируем функцию для получения токена

const Header = () => {
  const token = getToken(); // Проверка токена для определения авторизован ли пользователь

  return (
    <header className="bg-blue-500 p-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="text-white text-2xl font-bold">
          SSDLC Web App
        </div>
        <nav className="space-x-4">
          <Link
            to="/"
            className="text-white hover:text-blue-300"
          >
            Главная
          </Link>
          <Link
            to={token ? "/user" : "/login"}
            className="text-white hover:text-blue-300"
          >
            Я 
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
