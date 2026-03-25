import request from './request';
import type {
  Organization,
  OrganizationListParams,
  OrganizationListResponse,
  CreateOrganizationParams,
  UpdateOrganizationParams,
} from '@/types/organization';

/**
 * 获取组织列表
 */
export async function getOrganizations(
  params: OrganizationListParams
): Promise<OrganizationListResponse> {
  return request.get('/organizations', { params });
}

/**
 * 获取组织详情
 */
export async function getOrganization(id: number): Promise<Organization> {
  return request.get(`/organizations/${id}`);
}

/**
 * 创建组织
 */
export async function createOrganization(
  data: CreateOrganizationParams
): Promise<Organization> {
  return request.post('/organizations', data);
}

/**
 * 更新组织
 */
export async function updateOrganization(
  id: number,
  data: UpdateOrganizationParams
): Promise<Organization> {
  return request.put(`/organizations/${id}`, data);
}

/**
 * 删除组织
 */
export async function deleteOrganization(id: number): Promise<void> {
  return request.delete(`/organizations/${id}`);
}
