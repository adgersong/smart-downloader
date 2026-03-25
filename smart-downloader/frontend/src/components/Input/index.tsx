import React from 'react';
import { Input as AntdInput, type InputProps as AntdInputProps } from 'antd';

interface InputProps extends AntdInputProps {}

/**
 * 基础输入框组件
 */
export const Input: React.FC<InputProps> = (props) => {
  return <AntdInput {...props} />;
};

/**
 * 密码输入框
 */
export const PasswordInput: React.FC<InputProps> = (props) => {
  return <AntdInput.Password {...props} />;
};

/**
 * 文本域
 */
export const TextArea: React.FC<InputProps> = (props) => {
  return <AntdInput.TextArea {...props} />;
};
