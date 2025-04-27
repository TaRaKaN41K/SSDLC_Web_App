// utils/errorHandler.ts

import { ErrorCode } from '../constants/error_code';

export const handleError = (error: any): string => {
  let errorText = 'Ошибка входа';

  if (error.response) {
    const { status, data } = error.response;

    switch (data.error_code) {
      case ErrorCode.INVALID_PASSWORD:
        errorText = 'Неверный логин или пароль.';
        break;
      case ErrorCode.INVALID_TOKEN:
        errorText = 'Доступ запрещен.';
        break;
      case ErrorCode.USER_NO_ACTIVE:
        errorText = 'Аккаунт не активирован.';
        break;
      case ErrorCode.FORBIDDEN:
        errorText = 'Доступ запрещен.';
        break;
      case ErrorCode.SERVER_ERROR:
        errorText = 'Ошибка на сервере. Пожалуйста, попробуйте позже.';
        break;
      default:
        errorText = 'Неизвестная ошибка. Попробуйте снова.';
        break;
    }
  } else if (error.request) {
    errorText = 'Нет ответа от сервера. Пожалуйста, проверьте подключение.';
  } else {
    errorText = 'Ошибка при отправке запроса.';
  }

  return errorText;
};

export const handleGeneralError = (error: any): string => {
  let errorText = 'Произошла ошибка';

  if (error.response) {
    const { status, data } = error.response;

    if (data && data.message) {
      errorText = data.message;
    } else {
      errorText = 'Ошибка на сервере. Пожалуйста, попробуйте позже.';
    }
  } else if (error.request) {
    errorText = 'Нет ответа от сервера. Пожалуйста, проверьте подключение.';
  } else {
    errorText = 'Ошибка при отправке запроса.';
  }

  return errorText;
};
