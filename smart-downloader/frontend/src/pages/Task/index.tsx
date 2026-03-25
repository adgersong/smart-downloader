import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, List, Button, Space, Progress, Tag, Timeline, message } from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  StopOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import { executeTask, cancelTask, getTasks } from '@/services/task';
import { useWebSocket } from '@/hooks/useWebSocket';
import type { Task } from '@/services/task';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [executingTask, setExecutingTask] = useState<Task | null>(null);
  const [logs, setLogs] = useState<any[]>([]);

  const fetchTasks = async () => {
    try {
      const response = await getTasks({ org_id: 1, page: 1, size: 10 });
      setTasks(response.items);
    } catch (error: any) {
      message.error(error.message);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const { sendMessage } = useWebSocket(
    executingTask?.id || 0,
    {
      onMessage: (data) => {
        console.log('WebSocket message:', data);
        if (data.type === 'log') {
          setLogs((prev) => [...prev, data.data]);
        } else if (data.type === 'status_update') {
          setExecutingTask((prev) =>
            prev ? { ...prev, ...data.data } : null
          );
        } else if (data.type === 'completed') {
          message.success('任务执行完成');
          setExecutingTask(null);
          setLogs([]);
          fetchTasks();
        } else if (data.type === 'error') {
          message.error(`任务执行失败：${data.data.error.message}`);
          setExecutingTask(null);
        }
      },
    }
  );

  const handleExecute = async (workflowId: number) => {
    try {
      const response = await executeTask({ workflow_id: workflowId });
      setExecutingTask({
        id: response.task_id,
        workflow_id: workflowId,
        status: 'pending',
        created_at: new Date().toISOString(),
      });
      message.success('任务已开始执行');
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const handleCancel = async (taskId: number) => {
    try {
      await cancelTask(taskId);
      message.success('任务已取消');
      setExecutingTask(null);
      fetchTasks();
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      pending: 'default',
      running: 'processing',
      success: 'success',
      failed: 'error',
      cancelled: 'warning',
    };
    return colors[status] || 'default';
  };

  const getStatusIcon = (status: string) => {
    const icons: Record<string, React.ReactNode> = {
      pending: <SyncOutlined spin />,
      running: <PlayCircleOutlined spin />,
      success: <CheckCircleOutlined />,
      failed: <CloseCircleOutlined />,
      cancelled: <PauseCircleOutlined />,
    };
    return icons[status] || <SyncOutlined />;
  };

  return (
    <PageContainer title="任务管理">
      <Card title="执行中的任务" style={{ marginBottom: 16 }}>
        {executingTask ? (
          <div>
            <div style={{ marginBottom: 16 }}>
              <Space>
                <Tag color={getStatusColor(executingTask.status)} icon={getStatusIcon(executingTask.status)}>
                  {executingTask.status}
                </Tag>
                <Button
                  danger
                  icon={<StopOutlined />}
                  onClick={() => handleCancel(executingTask.id)}
                >
                  停止
                </Button>
              </Space>
            </div>
            <Progress
              percent={executingTask.progress?.percentage || 0}
              status="active"
              format={(percent) => `${percent}% (${executingTask.progress?.current_step}/${executingTask.progress?.total_steps})`}
            />
            <Card
              title="执行日志"
              size="small"
              style={{ marginTop: 16, maxHeight: 300, overflow: 'auto' }}
            >
              <Timeline>
                {logs.map((log, index) => (
                  <Timeline.Item key={index} color={log.level === 'ERROR' ? 'red' : 'green'}>
                    <div style={{ fontSize: 12 }}>
                      [{new Date(log.timestamp).toLocaleTimeString()}] {log.message}
                    </div>
                  </Timeline.Item>
                ))}
              </Timeline>
            </Card>
          </div>
        ) : (
          <div style={{ color: '#86868B', textAlign: 'center', padding: 40 }}>
            暂无执行中的任务
          </div>
        )}
      </Card>

      <Card title="任务列表">
        <List
          dataSource={tasks}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                title={
                  <Space>
                    <span>{item.workflow_name || `任务 #${item.id}`}</span>
                    <Tag color={getStatusColor(item.status)} icon={getStatusIcon(item.status)}>
                      {item.status}
                    </Tag>
                  </Space>
                }
                description={`创建时间：${new Date(item.created_at).toLocaleString()}`}
              />
              <Space>
                {item.status === 'pending' && (
                  <Button
                    type="primary"
                    size="small"
                    icon={<PlayCircleOutlined />}
                    onClick={() => handleExecute(item.workflow_id)}
                  >
                    执行
                  </Button>
                )}
                {item.status === 'failed' && (
                  <Button
                    size="small"
                    icon={<SyncOutlined />}
                    onClick={() => handleExecute(item.workflow_id)}
                  >
                    重试
                  </Button>
                )}
              </Space>
            </List.Item>
          )}
        />
      </Card>
    </PageContainer>
  );
};

export default TaskList;
