import React from 'react';
import { Form as AntdForm, type FormProps as AntdFormProps, type FormItemProps } from 'antd';

interface FormProps extends AntdFormProps {}

/**
 * 基础表单组件
 */
export const Form: React.FC<FormProps> = ({ children, ...props }) => {
  return <AntdForm {...props}>{children}</AntdForm>;
};

/**
 * 表单项
 */
export const FormItem: React.FC<FormItemProps> = ({ children, ...props }) => {
  return <AntdForm.Item {...props}>{children}</AntdForm.Item>;
};

Form.Item = FormItem;
