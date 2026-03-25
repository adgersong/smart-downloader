import request from './request';

export interface BusinessSystem {
  id: number;
  org_id: number;
  name: string;
  url: string;
  type: string;
  description?: string;
  login_config?: Record<string, any>;
  has_credential: boolean;
  workflow_count: number;
  created_at: string;
  updated_at: string;
}

export interface SystemListParams {
  org_id: number;
  type?: string;
  page?: number;
  size?: number;
}

export interface SystemListResponse {
  items: BusinessSystem[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export interface CreateSystemParams {
  org_id: number;
  name: string;
  url: string;
  type: string;
  description?: string;
  login_config?: Record<string, any>;
}

export interface UpdateSystemParams {
  name?: string;
  url?: string;
  type?: string;
  description?: string;
  login_config?: Record<string, any>;
}

/**
 * 获取业务系统列表
 */
export async function getSystems(params: SystemListParams): Promise<SystemListResponse> {
  return request.get('/systems', { params });
}

/**
 * 获取业务系统详情
 */
export async function getSystem(id: number): Promise<BusinessSystem> {
  return request.get(`/systems/${id}`);
}

/**
 * 创建业务系统
 */
export async function createSystem(data: CreateSystemParams): Promise<BusinessSystem> {
  return request.post('/systems', data);
}

/**
 * 更新业务系统
 */
export async function updateSystem(
  id: number,
  data: UpdateSystemParams
): Promise<BusinessSystem> {
  return request.put(`/systems/${id}`, data);
}

/**
 * 删除业务系统
 */
export async function deleteSystem(id: number): Promise<void> {
  return request.delete(`/systems/${id}`);
}
