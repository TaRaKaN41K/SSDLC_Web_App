import React, { useState } from 'react';
import { EyeInvisibleOutlined, EyeOutlined } from '@ant-design/icons';

interface CustomInputProps {
  type: 'text' | 'password' | 'email' | 'file' | 'number';
  placeholder: string;
  value: string;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  autoComplete?: string;
  rounded?: boolean;
  icon?: boolean;
  size?: 'small' | 'medium' | 'large'; // Для изменения размера поля
}

const CustomInput: React.FC<CustomInputProps> = ({
  type,
  placeholder,
  value,
  onChange,
  autoComplete,
  rounded = true,
  icon = false,
  size = 'medium',
}) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const togglePasswordVisibility = (event: React.MouseEvent) => {
    event.preventDefault();
    setIsPasswordVisible(!isPasswordVisible);
  };

  const handleMouseUp = () => {
    setIsPasswordVisible(false);
  };

  const inputSizeClasses = {
    small: 'h-8 text-sm p-2 pt-2 pb-2 mb-6',
    medium: 'h-10 text-base p-3 pt-3 pb-3 mb-8',
    large: 'h-12 text-lg p-4 pt-4 pb-4 mb-10',
  };

  return (
    <div className="relative w-full">
      <input
        type={type === 'password' && !isPasswordVisible ? 'password' : 'text'}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        className={`
            border 
            ${inputSizeClasses[size]} 
            w-full
            ${rounded ? 'rounded-md' : ''} 
            ${type === 'password' ? 'pr-12' : ''} 
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
            `
        }
      />
      {type === 'password' && icon && (
        <button
          type="button"
          onMouseDown={togglePasswordVisibility}
          onMouseUp={handleMouseUp}
          className="absolute top-2 right-3 text-gray-500"
        >
          {isPasswordVisible ? (
            <EyeOutlined className="text-lg" />
          ) : (
            <EyeInvisibleOutlined className="text-lg" />
          )}
        </button>
      )}
    </div>
  );
};

export default CustomInput;
