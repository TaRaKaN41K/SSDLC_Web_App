import React, { useState } from 'react';
import { Button } from 'antd';

interface CustomButtonProps {
  onClick: () => void;
  text: string;
  size?: 'small' | 'medium' | 'large';
  color?: 'blue' | 'green' | 'red';
  loading?: boolean;
  marginTop?: string;
  marginBottom?: string;
}

const CustomButton: React.FC<CustomButtonProps> = ({
  onClick,
  text,
  size = 'medium', 
  color = 'red',
  loading = false,
  marginTop = 'mt-4',
  marginBottom = 'mb-4',
}) => {
    
    const sizeClasses = {
        small: 'h-8 text-sm p-2 pt-2 pb-2 mb-6',
        medium: 'h-10 text-base p-3 pt-3 pb-3 mb-8',
        large: 'h-12 text-lg p-4 pt-4 pb-4 mb-10',
      };


    const colorClasses = {
        blue: 'bg-blue-500 hover:bg-blue-600 text-white',
        green: 'bg-green-500 hover:bg-green-600 text-white',
        red: 'bg-red-500 hover:bg-red-600 text-white'
    };

  return (
    <Button
      type="primary"
      onClick={onClick}
      className={`
        ${sizeClasses[size]} 
        ${colorClasses[color]} 
        ${marginTop} 
        ${marginBottom}
        inline-block 
        px-4 
        py-2 
        rounded-lg 
        shadow-md 
        transition-all 
        duration-300 
        transform 
        hover:scale-105 
        w-full`
    }
      loading={loading}
    >
      {text}
    </Button>
  );
};

export default CustomButton;
