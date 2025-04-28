import React from 'react';
import { Link } from 'react-router-dom';
import { getToken } from '../auth/auth';
import { FaHome, FaUser } from 'react-icons/fa';
import IconButton from './IconButton';

const Header = () => {
  const token = getToken();

  return (
    <header className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 
      bg-white bg-opacity-80 backdrop-blur-md 
      px-8 py-2 rounded-full shadow-2xl 
      flex justify-between items-center max-w-6xl w-[95%] border border-gray-200">
      
      {/* Логотип + ссылка на GitHub */}
      <div className="relative group text-gray-800 text-xl font-bold">
        <Link
          to="https://github.com/TaRaKaN41K/SSDLC_Web_App.git"
          target="_blank"
          className="hover:text-blue-500 transition-colors"
        >
          SSDLC Web App
        </Link>
      </div>

      {/* Навигация */}
      <nav className="space-x-4 flex items-center">
        <IconButton icon="home" to="/" color="gray" />
        <IconButton icon="user" to={token ? "/user" : "/login"} color="gray" />
      </nav>
    </header>
  );
};

export default Header;
