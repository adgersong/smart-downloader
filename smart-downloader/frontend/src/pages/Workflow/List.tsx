import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, List, Button, Space, Tag, Input, Select, Modal, message, Empty } from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  SearchOutlined,
  FilterOutlined,
  CopyOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'umi';
import request from '@/services/request';

interface Workflow {
  id: number;
  name: string;
  description?: string;
  status: 'draft' | 'active' | 'archived';
  version: string;
  created_at: string;
  updated_at: string;
  created_by?: string;
  last_run_at?: string;
  run_count: number;
}

const WorkflowList: React.FC = () => {
  const navigate = useNavigate();
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);

  const fetchWorkflows = async () => {
    setLoading(true);
    try {
      const response = await request.get('/workflows', {
        params: { status: statusFilter !== 'all' ? statusFilter : undefined },
      });
      setWorkflows(response.items || []);
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '加载流程列表失败';
      message.error(messageText);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkflows();
  }, [statusFilter]);

  const handleDelete = async () => {
    if (!selectedWorkflow) return;
    try {
      await request.delete(`/workflows/${selectedWorkflow.id}`);
      message.success('流程已删除');
      setDeleteModalOpen(false);
      fetchWorkflows();
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '删除失败';
      message.error(messageText);
    }
  };

  const handleDuplicate = async (workflow: Workflow) => {
    try {
      await request.post(`/workflows/${workflow.id}/duplicate`, {
        name: `${workflow.name} (副本)`,
      });
      message.success('流程已复制');
      fetchWorkflows();
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '复制失败';
      message.error(messageText);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'default',
      active: 'success',
      archived: 'warning',
    };
    return colors[status] || 'default';
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: '草稿',
      active: '已激活',
      archived: '已归档',
    };
    return labels[status] || status;
  };

  const filteredWorkflows = workflows.filter((wf) =>
    wf.name.toLowerCase().includes(searchText.toLowerCase()) ||
    wf.description?.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <PageContainer
      title="流程管理"
      subTitle="创建和管理浏览器自动化流程"
      extra={
        <Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/workflow/create')}
          >
            创建流程
          </Button>
        </Space>
      }
    >
      <Card style={{ marginBottom: 16 }}>
        <Space style={{ width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input
              placeholder="搜索流程..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: 240 }}
              allowClear
            />
            <Select
              value={statusFilter}
              onChange={setStatusFilter}
              style={{ width: 120 }}
              options={[
                { value: 'all', label: '全部状态' },
                { value: 'draft', label: '草稿' },
                { value: 'active', label: '已激活' },
                { value: 'archived', label: '已归档' },
              ]}
            />
          </Space>
          <Space>
            <Button icon={<FilterOutlined />}>筛选</Button>
          </Space>
        </Space>
      </Card>

      <Card>
        {filteredWorkflows.length === 0 ? (
          <Empty
            description={searchText ? '未找到匹配的流程' : '暂无流程，创建一个吧'}
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            {!searchText && (
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => navigate('/workflow/create')}
              >
                创建第一个流程
              </Button>
            )}
          </Empty>
        ) : (
          <List
            grid={{ gutter: 16, column: 2 }}
            dataSource={filteredWorkflows}
            loading={loading}
            renderItem={(item) => (
              <List.Item>
                <Card
                  hoverable
                  actions={[
                    <Button
                      key="view"
                      type="link"
                      icon={<EyeOutlined />}
                      onClick={() => navigate(`/workflow/${item.id}/preview`)}
                    >
                      预览
                    </Button>,
                    <Button
                      key="edit"
                      type="link"
                      icon={<EditOutlined />}
                      onClick={() => navigate(`/workflow/${item.id}/edit`)}
                    >
                      编辑
                    </Button>,
                    <Button
                      key="copy"
                      type="link"
                      icon={<CopyOutlined />}
                      onClick={() => handleDuplicate(item)}
                    >
                      复制
                    </Button>,
                    <Button
                      key="delete"
                      type="link"
                      danger
                      icon={<DeleteOutlined />}
                      onClick={() => {
                        setSelectedWorkflow(item);
                        setDeleteModalOpen(true);
                      }}
                    >
                      删除
                    </Button>,
                  ]}
                >
                  <Card.Meta
                    title={
                      <Space>
                        <span>{item.name}</span>
                        <Tag color={getStatusColor(item.status)}>
                          {getStatusLabel(item.status)}
                        </Tag>
                      </Space>
                    }
                    description={
                      <div style={{ marginTop: 8 }}>
                        <div style={{ fontSize: 12, color: '#6E6E73', marginBottom: 8 }}>
                          {item.description || '暂无描述'}
                        </div>
                        <Space split={<span style={{ color: '#2D2D2F' }}>|</span>}>
                          <span style={{ fontSize: 11, color: '#4A4A4F' }}>
                            版本：{item.version}
                          </span>
                          <span style={{ fontSize: 11, color: '#4A4A4F' }}>
                            运行：{item.run_count}次
                          </span>
                          {item.last_run_at && (
                            <span style={{ fontSize: 11, color: '#4A4A4F' }}>
                              最后运行：{new Date(item.last_run_at).toLocaleDateString()}
                            </span>
                          )}
                        </Space>
                      </div>
                    }
                  />
                </Card>
              </List.Item>
            )}
          />
        )}
      </Card>

      <Modal
        title="确认删除"
        open={deleteModalOpen}
        onOk={handleDelete}
        onCancel={() => setDeleteModalOpen(false)}
        okText="删除"
        cancelText="取消"
        okButtonProps={{ danger: true }}
      >
        <p>确定要删除流程 <strong>{selectedWorkflow?.name}</strong> 吗？</p>
        <p style={{ color: '#faad14', fontSize: 12 }}>
          此操作不可恢复，该流程下的所有任务和下载记录也将被删除。
        </p>
      </Modal>
    </PageContainer>
  );
};

export default WorkflowList;
