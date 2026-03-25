import React from 'react';
import { Button as AntdButton, type ButtonProps as AntdButtonProps } from 'antd';

interface ButtonProps extends AntdButtonProps {
  loading?: boolean;
}

/**
 * 基础按钮组件 - 采用高级灰主题色
 */
export const Button: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <AntdButton {...props}>
      {children}
    </AntdButton>
  );
};

/**
 * 主按钮
 */
export const PrimaryButton: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <AntdButton type="primary" {...props}>
      {children}
    </AntdButton>
  );
};

/**
 * 危险按钮
 */
export const DangerButton: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <AntdButton danger type="primary" {...props}>
      {children}
    </AntdButton>
  );
};
