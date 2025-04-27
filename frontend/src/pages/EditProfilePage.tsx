import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import api from '../api/axios';
import qs from 'qs'; 


const EditProfilePage = () => {
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/user/me');
        setEmail(res.data.email || '');
      } catch (err) {
        console.error('Ошибка при получении данных профиля:', err);
        setErrorMessage('Не удалось загрузить профиль');
      }
    };

    fetchProfile();
  }, []);

  const queryParams = qs.stringify({
        email,
      });

  const handleSave = async () => {
    try {
      await api.post(`/user/edit_profile?${queryParams}`);
      navigate('/user');
    } catch (err) {
      console.error('Ошибка при сохранении профиля:', err);
      setErrorMessage('Не удалось сохранить изменения');
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Редактирование профиля</h1>

      {errorMessage && <p className="text-red-500 mb-2">{errorMessage}</p>}

      <input
        className="border p-2 w-full mb-2"
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button
        onClick={handleSave}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
      >
        Сохранить
      </button>
    </div>
  );
};

export default EditProfilePage;
