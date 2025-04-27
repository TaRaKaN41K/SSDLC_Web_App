import React from 'react';
import api from '../api/axios';
import IconButton from './IconButton'; // Импортируем компонент иконок

interface UserCardProps {
  username: string;
  email: string;
  photoFilename: string;
  onLogout?: () => void; // Функция для выхода
  onDeleteAccount?: () => void; // Функция для удаления аккаунта
  onEditProfile?: () => void; // Функция для редактирования профиля
}

const UserCard: React.FC<UserCardProps> = ({
  username,
  email,
  photoFilename,
  onLogout,
  onDeleteAccount,
  onEditProfile,
}) => {
  const getPhotoUrl = (photoFilename: string) => {
    return photoFilename ? `${api.defaults.baseURL}/uploads/${photoFilename}` : '/default-avatar.png';
  };

  return (
    <div className="bg-white bg-opacity-50 p-6 rounded-lg shadow-lg border border-gray-200 space-y-4 relative backdrop-blur-sm">
      <div className="flex justify-center">
        <img
          src={getPhotoUrl(photoFilename)}
          alt="Фото пользователя"
          className="w-32 h-32 object-cover rounded-full"
        />
      </div>

      <div className="text-center">
        <h2 className="text-xl font-semibold text-gray-800">{username}</h2>
        <p className="text-gray-600">{email}</p>
      </div>

      {/* Отображаем кнопки, если они переданы */}
      {(onLogout || onDeleteAccount || onEditProfile) && (
        <div className="mt-6 flex justify-center gap-6">
          {onEditProfile && (
            <IconButton
              icon="edit"
              onClick={onEditProfile}
              color="blue"
            />
          )}

          {onLogout && (
            <IconButton
              icon="logout"
              onClick={onLogout}
              color="green"
            />
          )}

          {onDeleteAccount && (
            <IconButton
              icon="delete"
              onClick={onDeleteAccount}
              color="red"
            />
          )}
        </div>
      )}
    </div>
  );
};

export default UserCard;
