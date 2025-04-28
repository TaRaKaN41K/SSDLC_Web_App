import React from 'react';
import { FaEdit, FaSignOutAlt, FaTrashAlt, FaHome, FaUser } from 'react-icons/fa'; // Добавляем новые иконки
import { Link } from 'react-router-dom';

interface IconButtonProps {
  icon: 'edit' | 'logout' | 'delete' | 'home' | 'user'; // Добавляем новые иконки
  onClick?: () => void;
  to?: string;
  color?: 'blue' | 'green' | 'red' | 'gray' | 'white'; // Добавляем белый цвет
}

const IconButton: React.FC<IconButtonProps> = ({ icon, onClick, to, color = 'gray' }) => {
  const colorClasses: Record<string, string> = {
    blue: 'text-blue-700',
    green: 'text-green-700',
    red: 'text-red-700',
    gray: 'text-gray-700',
    white: 'text-white', // Белый цвет
  };

  const renderIcon = () => {
    switch (icon) {
      case 'edit':
        return <FaEdit className={`${colorClasses[color]} text-lg`} />;
      case 'logout':
        return <FaSignOutAlt className={`${colorClasses[color]} text-lg`} />;
      case 'delete':
        return <FaTrashAlt className={`${colorClasses[color]} text-lg`} />;
      case 'home':
        return <FaHome className={`${colorClasses[color]} text-lg`} />;
      case 'user':
        return <FaUser className={`${colorClasses[color]} text-lg`} />;
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
