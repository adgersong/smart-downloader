import request from './request';

export interface Task {
  id: number;
  workflow_id: number;
  workflow_name?: string;
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled';
  schedule?: string;
  progress?: {
    current_step: number;
    total_steps: number;
    percentage: number;
  };
  created_at: string;
  started_at?: string;
  completed_at?: string;
  estimated_remaining?: number;
}

export interface TaskListParams {
  org_id: number;
  workflow_id?: number;
  status?: string;
  page?: number;
  size?: number;
}

export interface TaskListResponse {
  items: Task[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export interface ExecuteTaskParams {
  workflow_id: number;
  context?: Record<string, any>;
  schedule?: {
    enabled: boolean;
    cron?: string;
  };
}

export interface TaskLogEntry {
  timestamp: string;
  level: string;
  step: string;
  message: string;
}

/**
 * 获取任务列表
 */
export async function getTasks(params: TaskListParams): Promise<TaskListResponse> {
  return request.get('/tasks', { params });
}

/**
 * 获取任务详情
 */
export async function getTask(id: number): Promise<Task> {
  return request.get(`/tasks/${id}`);
}

/**
 * 执行任务
 */
export async function executeTask(data: ExecuteTaskParams): Promise<{ task_id: number }> {
  return request.post('/tasks/execute', data);
}

/**
 * 取消任务
 */
export async function cancelTask(id: number): Promise<void> {
  return request.post(`/tasks/${id}/cancel`);
}

/**
 * 重试任务
 */
export async function retryTask(id: number): Promise<{ task_id: number }> {
  return request.post(`/tasks/${id}/retry`);
}

/**
 * 获取任务日志
 */
export async function getTaskLogs(id: number): Promise<{ logs: TaskLogEntry[] }> {
  return request.get(`/tasks/${id}/logs`);
}
