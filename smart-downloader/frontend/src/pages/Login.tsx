import React from 'react';
import { useNavigate } from 'umi';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined, BankOutlined } from '@ant-design/icons';

export default () => {
  const navigate = useNavigate();

  const onFinish = async (values: any) => {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          org_id: parseInt(values.org_id),
          username: values.username,
          password: values.password,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        message.success('登录成功');
        navigate('/dashboard');
      } else {
        message.error(data.detail || '登录失败');
      }
    } catch (error: any) {
      message.error(error.message || '登录失败');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    }}>
      <Card 
        title={
          <div style={{ textAlign: 'center', fontSize: '24px' }}>
            智下载 SmartDownloader
          </div>
        }
        subTitle="智能浏览器自动化下载系统"
        style={{ width: 400 }}
      >
        <Form
          name="login"
          onFinish={onFinish}
          initialValues={{ org_id: 1, username: 'admin', password: 'admin123' }}
          size="large"
        >
          <Form.Item
            name="org_id"
            rules={[{ required: true, message: '请输入组织 ID!' }]}
          >
            <Input 
              prefix={<BankOutlined />} 
              placeholder="组织 ID" 
              type="number"
            />
          </Form.Item>

          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名!' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码!' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large">
              登录
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};
