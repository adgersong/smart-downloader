export interface Organization {
  id: number;
  name: string;
  config?: Record<string, any>;
  stats?: {
    user_count: number;
    system_count: number;
    workflow_count: number;
    task_count: number;
  };
  created_at: string;
  updated_at: string;
}

export interface OrganizationListParams {
  page?: number;
  size?: number;
  keyword?: string;
}

export interface OrganizationListResponse {
  items: Organization[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export interface CreateOrganizationParams {
  name: string;
  config?: Record<string, any>;
}

export interface UpdateOrganizationParams {
  name?: string;
  config?: Record<string, any>;
}

export async function getOrganizations(
  params: OrganizationListParams
): Promise<OrganizationListResponse> {
  return request.get('/organizations', { params });
}

export async function getOrganization(id: number): Promise<Organization> {
  return request.get(`/organizations/${id}`);
}

export async function createOrganization(
  data: CreateOrganizationParams
): Promise<Organization> {
  return request.post('/organizations', data);
}

export async function updateOrganization(
  id: number,
  data: UpdateOrganizationParams
): Promise<Organization> {
  return request.put(`/organizations/${id}`, data);
}

export async function deleteOrganization(id: number): Promise<void> {
  return request.delete(`/organizations/${id}`);
}
