import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import qs from 'qs'; 
import CustomInput from '../components/CustomInput';
import CustomButton from '../components/CustomButton';
import ErrorAlert from '../components/ErrorAlert';

const EditProfilePage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [photoFile, setPhotoFile] = useState<File | null>(null);
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

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files ? e.target.files[0] : null;
    if (file) {
      setPhotoFile(file);
    }
  };

  const handleSave = async () => {
    const formData = new FormData();
    if (photoFile) {
      formData.append('photo_file', photoFile);
    }

    const queryParams = qs.stringify({
      email,
    });

    try {
      await api.post(`/user/edit_profile?${queryParams}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      navigate('/user');
    } catch (err) {
      console.error('Ошибка при сохранении профиля:', err);
      setErrorMessage('Не удалось сохранить изменения');
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-lg shadow-lg border border-gray-200 mt-16 space-y-4">
      <h1 className="text-2xl font-semibold mb-6 text-center text-gray-800">Редактирование профиля</h1>

      {errorMessage && <ErrorAlert message={errorMessage} size="medium" />}

      <CustomInput
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        size="medium"
        rounded={true}
      />

      <div className="mb-6">
        <label htmlFor="photo_file" className="block mb-2 text-sm text-gray-600">Фото профиля</label>
        <input
          id="photo_file"
          type="file"
          accept="image/*"
          onChange={handlePhotoChange}
          className="border p-2 w-full rounded-md"
        />
      </div>

      <CustomButton
        onClick={handleSave}
        text="Сохранить"
        size="medium"
        color="blue"
        loading={false}
      />

      <div className="mt-4 text-center">
        <p className="text-sm text-gray-700">
          <a href="/user" className="text-blue-500 hover:underline">
            Назад к профилю
          </a>
        </p>
      </div>
    </div>
  );
};

export default EditProfilePage;
