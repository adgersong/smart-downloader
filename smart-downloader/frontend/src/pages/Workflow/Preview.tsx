import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, Button, Space, Tag, Descriptions, Alert, Modal, message } from 'antd';
import {
  LeftOutlined,
  EditOutlined,
  PlayCircleOutlined,
  CheckCircleOutlined,
  WarningOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useNavigate, useParams } from 'umi';
import WorkflowCanvas from './WorkflowCanvas';
import { validateWorkflow, getValidationSummary } from './validator';
import request from '@/services/request';

interface Workflow {
  id: number;
  name: string;
  description?: string;
  status: 'draft' | 'active' | 'archived';
  version: string;
  yaml_config?: string;
  created_at: string;
  updated_at: string;
}

const WorkflowPreview: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [validationResult, setValidationResult] = useState<{
    valid: boolean;
    errors: number;
    warnings: number;
  } | null>(null);
  const [yamlModalOpen, setYamlModalOpen] = useState(false);

  const fetchWorkflow = async () => {
    if (!id) return;
    try {
      const data = await request.get(`/workflows/${id}`);
      setWorkflow(data);
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '加载流程失败';
      message.error(messageText);
    }
  };

  useEffect(() => {
    fetchWorkflow();
  }, [id]);

  const handleRun = async () => {
    if (!workflow) return;
    try {
      await request.post('/tasks/execute', { workflow_id: workflow.id });
      message.success('任务已启动');
      navigate('/task');
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '启动任务失败';
      message.error(messageText);
    }
  };

  const handleValidate = () => {
    const stored = localStorage.getItem(`workflow-${id}`);
    if (stored) {
      const { nodes, edges } = JSON.parse(stored);
      const result = validateWorkflow(nodes, edges);
      setValidationResult({
        valid: result.valid,
        errors: result.errors.length,
        warnings: result.warnings.length,
      });
    } else {
      message.warning('流程数据不存在，请先保存流程');
    }
  };

  if (!workflow) {
    return null;
  }

  return (
    <PageContainer
      title={workflow.name}
      subTitle={`版本：${workflow.version}`}
      tags={
        <Tag color={workflow.status === 'active' ? 'success' : 'default'}>
          {workflow.status === 'active' ? '已激活' : workflow.status === 'draft' ? '草稿' : '已归档'}
        </Tag>
      }
      onBack={() => navigate('/workflow')}
      extra={
        <Space>
          <Button icon={<LeftOutlined />} onClick={() => navigate('/workflow')}>
            返回列表
          </Button>
          <Button
            icon={<EditOutlined />}
            onClick={() => navigate(`/workflow/${id}/edit`)}
          >
            编辑
          </Button>
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={handleRun}
            disabled={workflow.status === 'archived'}
          >
            执行流程
          </Button>
        </Space>
      }
    >
      {validationResult && (
        <Alert
          message={getValidationSummary({
            valid: validationResult.valid,
            errors: Array(validationResult.errors).fill({}),
            warnings: Array(validationResult.warnings).fill({}),
          } as any)}
          type={validationResult.valid ? 'success' : 'error'}
          showIcon
          icon={
            validationResult.valid ? (
              validationResult.warnings > 0 ? (
                <WarningOutlined />
              ) : (
                <CheckCircleOutlined />
              )
            ) : (
              <CloseCircleOutlined />
            )
          }
          style={{ marginBottom: 16 }}
          action={
            <Button size="small" onClick={() => setValidationResult(null)}>
              关闭
            </Button>
          }
        />
      )}

      <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
        <Card style={{ flex: 1 }}>
          <Descriptions size="small" column={2}>
            <Descriptions.Item label="流程名称">{workflow.name}</Descriptions.Item>
            <Descriptions.Item label="版本号">{workflow.version}</Descriptions.Item>
            <Descriptions.Item label="状态">
              <Tag color={workflow.status === 'active' ? 'success' : 'default'}>
                {workflow.status === 'active' ? '已激活' : workflow.status === 'draft' ? '草稿' : '已归档'}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="创建时间">
              {new Date(workflow.created_at).toLocaleString()}
            </Descriptions.Item>
            <Descriptions.Item label="更新时间">
              {new Date(workflow.updated_at).toLocaleString()}
            </Descriptions.Item>
            <Descriptions.Item label="描述">{workflow.description || '-'}</Descriptions.Item>
          </Descriptions>
        </Card>

        <Card style={{ width: 300 }}>
          <Space direction="vertical" style={{ width: '100%' }} size="small">
            <Button block onClick={handleValidate}>
              验证流程
            </Button>
            <Button block onClick={() => setYamlModalOpen(true)}>
              查看 YAML
            </Button>
          </Space>
        </Card>
      </div>

      <Card style={{ height: 'calc(100vh - 400px)', minHeight: 500 }}>
        <WorkflowCanvas workflowId={workflow.id} readOnly />
      </Card>

      <Modal
        title="YAML 配置"
        open={yamlModalOpen}
        onCancel={() => setYamlModalOpen(false)}
        width={800}
        footer={
          <Button onClick={() => setYamlModalOpen(false)}>关闭</Button>
        }
      >
        <pre
          style={{
            background: '#1D1D1F',
            padding: 16,
            borderRadius: 8,
            overflow: 'auto',
            maxHeight: 500,
            color: '#E8E8ED',
            fontSize: 12,
          }}
        >
          {workflow.yaml_config || '暂无 YAML 配置'}
        </pre>
      </Modal>
    </PageContainer>
  );
};

export default WorkflowPreview;
