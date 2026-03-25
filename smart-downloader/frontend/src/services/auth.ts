import request from './request';

export interface LoginParams {
  org_id: number;
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
    org_id: number;
    org_name: string;
  };
}

export interface UserInfo {
  id: number;
  username: string;
  email: string;
  role: string;
  org_id: number;
  org_name: string;
}

export async function login(data: LoginParams): Promise<LoginResponse> {
  const response = await request.post('/auth/login', data);
  return response;
}

export async function logout(): Promise<void> {
  return request.post('/auth/logout');
}

export async function getCurrentUser(): Promise<UserInfo> {
  return request.get('/auth/me');
}
