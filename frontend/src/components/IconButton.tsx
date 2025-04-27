import React from 'react';
import { FaEdit } from 'react-icons/fa'; // Карандаш
import { FaSignOutAlt } from 'react-icons/fa'; // Иконка выхода
import { FaTrashAlt } from 'react-icons/fa'; // Иконка удаления
import { Link } from 'react-router-dom';

interface IconButtonProps {
  icon: 'edit' | 'logout' | 'delete'; // тип иконки
  onClick?: () => void; // функция клика
  to?: string; // если это ссылка, то передаем маршрут
  color?: 'blue' | 'green' | 'red'; // Цвет иконки
}

const IconButton: React.FC<IconButtonProps> = ({ icon, onClick, to, color = 'gray' }) => {
  // Маппинг цветов
  const colorClasses: Record<string, string> = {
    blue: 'text-blue-700',
    green: 'text-green-700',
    red: 'text-red-700',
    gray: 'text-gray-700', // по умолчанию серый
  };

  const renderIcon = () => {
    switch (icon) {
      case 'edit':
        return <FaEdit className={`${colorClasses[color]} text-lg`} />;
      case 'logout':
        return <FaSignOutAlt className={`${colorClasses[color]} text-lg`} />;
      case 'delete':
        return <FaTrashAlt className={`${colorClasses[color]} text-lg`} />;
      default:
        return null;
    }
  };

  return to ? (
    <Link
      to={to}
      className="p-2 rounded-full w-10 h-10 flex items-center justify-center cursor-pointer transform transition-all hover:text-gray-500 hover:scale-110"
    >
      {renderIcon()}
    </Link>
  ) : (
    <button
      onClick={onClick}
      className="p-2 rounded-full w-10 h-10 flex items-center justify-center cursor-pointer transform transition-all hover:text-gray-500 hover:scale-110"
    >
      {renderIcon()}
    </button>
  );
};

export default IconButton;
