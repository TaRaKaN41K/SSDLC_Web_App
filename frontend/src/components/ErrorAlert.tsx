import React from 'react';
import { Alert } from 'antd';

interface ErrorAlertProps {
  message: string;
  size?: 'small' | 'medium' | 'large'; // Добавим размер
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, size = 'medium' }) => {
  const sizeClasses = {
    small: 'h-8 text-sm p-2 pt-2 pb-2',
    medium: 'h-10 text-base p-3 pt-3 pb-3',
    large: 'h-12 text-lg p-4 pt-4 pb-4',
  };

  return (
    <Alert
      message={message}
      type="error"
      showIcon
      className={`mb-4 ${sizeClasses[size]}`}
    />
  );
};

export default ErrorAlert;
