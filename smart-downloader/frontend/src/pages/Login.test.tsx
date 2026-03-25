import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { message } from 'antd';
import Login from './Login';
import * as authService from '@/services/auth';

jest.mock('antd', () => ({
  ...jest.requireActual('antd'),
  message: {
    success: jest.fn(),
    error: jest.fn(),
  },
}));

jest.mock('@/services/auth', () => ({
  login: jest.fn(),
}));

const renderWithRouter = (ui: React.ReactElement) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('Login Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  it('renders login form correctly', () => {
    renderWithRouter(<Login />);
    
    expect(screen.getByPlaceholderText(/请输入组织 ID/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/用户名/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/密码/i)).toBeInTheDocument();
    expect(screen.getByText(/登录/i)).toBeInTheDocument();
  });

  it('shows validation error when submit empty form', async () => {
    renderWithRouter(<Login />);
    
    const submitButton = screen.getByText(/登录/i);
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/请输入组织 ID/i)).toBeInvalid();
    });
  });

  it('calls login API with correct data when form is submitted', async () => {
    const mockLogin = jest.spyOn(authService, 'login');
    mockLogin.mockResolvedValue({
      access_token: 'mock_token',
      token_type: 'Bearer',
      expires_in: 86400,
      user: {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        role: 'admin',
        org_id: 1,
        org_name: '财务部',
      },
    });

    renderWithRouter(<Login />);
    
    fireEvent.change(screen.getByPlaceholderText(/请输入组织 ID/i), {
      target: { value: '1' },
    });
    fireEvent.change(screen.getByPlaceholderText(/用户名/i), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByPlaceholderText(/密码/i), {
      target: { value: 'password123' },
    });
    
    fireEvent.click(screen.getByText(/登录/i));
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        org_id: 1,
        username: 'admin',
        password: 'password123',
      });
    });
  });

  it('stores token in localStorage after successful login', async () => {
    jest.spyOn(authService, 'login').mockResolvedValue({
      access_token: 'test_token',
      token_type: 'Bearer',
      expires_in: 86400,
      user: {
        id: 1,
        username: 'admin',
        email: '',
        role: 'admin',
        org_id: 1,
        org_name: '财务部',
      },
    });

    renderWithRouter(<Login />);
    
    fireEvent.change(screen.getByPlaceholderText(/请输入组织 ID/i), {
      target: { value: '1' },
    });
    fireEvent.change(screen.getByPlaceholderText(/用户名/i), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByPlaceholderText(/密码/i), {
      target: { value: 'password' },
    });
    
    fireEvent.click(screen.getByText(/登录/i));
    
    await waitFor(() => {
      expect(localStorage.getItem('access_token')).toBe('test_token');
    });
  });

  it('shows error message when login fails', async () => {
    jest.spyOn(authService, 'login').mockRejectedValue(new Error('用户名或密码错误'));

    renderWithRouter(<Login />);
    
    fireEvent.change(screen.getByPlaceholderText(/请输入组织 ID/i), {
      target: { value: '1' },
    });
    fireEvent.change(screen.getByPlaceholderText(/用户名/i), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByPlaceholderText(/密码/i), {
      target: { value: 'wrong' },
    });
    
    fireEvent.click(screen.getByText(/登录/i));
    
    await waitFor(() => {
      expect(message.error).toHaveBeenCalledWith('用户名或密码错误');
    });
  });

  it('has auto-login checkbox checked by default', () => {
    renderWithRouter(<Login />);
    
    const checkbox = screen.getByLabelText(/自动登录/i);
    expect(checkbox).toBeChecked();
  });
});
