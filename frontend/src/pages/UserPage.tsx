// src/pages/UserPage.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { getToken, removeToken } from '../auth/auth';
import { handleError } from '../utils/error_handler';
import UserCard from '../components/UserCard';

interface User {
  username: string;
  email: string;
  photo_filename: string;
}

const UserPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogout = async () => {
    const token = getToken();
    if (token) {
      try {
        await api.get('/auth/logout');
        removeToken();
        navigate('/login');
      } catch (err) {
        console.error('Error logging out:', err);
        setErrorMessage('Ошибка при выходе');
      }
    }
  };

  const handleDeleteAccount = async () => {
    const token = getToken();
    if (token) {
      try {
        await api.delete('/user/delete_account');
        removeToken();
        navigate('/register');
      } catch (err) {
        console.error('Error deleting account:', err);
        setErrorMessage('Ошибка при удалении аккаунта');
      }
    }
  };

  const handleEditProfile = () => {
    navigate('/edit-profile');
  };

  useEffect(() => {
    const token = getToken();
    if (token) {
      api.get('/user/me')
        .then((res) => {
          setUser(res.data);
        })
        .catch((err) => {
          console.error('Error fetching user data:', err);
          const errorText = handleError(err);
          setErrorMessage(errorText);
          setUser(null);
        });
    } else {
      setUser(null);
    }
  }, [navigate]);

  return (
    <div className="p-6 max-w-md mx-auto mt-16">
      <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Добро пожаловать!</h1>

      {errorMessage && (
        <div className="text-red-500 mb-4">
          <strong>{errorMessage}</strong>
        </div>
      )}

      {user && (
        <UserCard
          username={user.username}
          email={user.email}
          photoFilename={user.photo_filename}
          onLogout={handleLogout}
          onDeleteAccount={handleDeleteAccount}
          onEditProfile={handleEditProfile}
        />
      )}
    </div>
  );
};

export default UserPage;
