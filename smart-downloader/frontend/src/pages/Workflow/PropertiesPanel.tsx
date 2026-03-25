import React, { useEffect } from 'react';
import { Card, Form, Input, Select, Button, InputNumber, Space } from 'antd';
import { Node } from '@xyflow/react';
import { DeleteOutlined, SaveOutlined } from '@ant-design/icons';

interface PropertiesPanelProps {
  node: Node | null;
  setNodes?: (nodes: Node[] | ((nds: Node[]) => Node[])) => void;
}

interface NodeFormData {
  label: string;
  actionType?: string;
  selector?: string;
  value?: string;
  url?: string;
  username?: string;
  password?: string;
  waitTime?: number;
  condition?: string;
}

const PropertiesPanel: React.FC<PropertiesPanelProps> = ({ node, setNodes }) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (node) {
      form.setFieldsValue(node.data as NodeFormData);
    } else {
      form.resetFields();
    }
  }, [node, form]);

  const handleSave = async () => {
    if (!node || !setNodes) return;
    
    try {
      const values = await form.validateFields();
      setNodes((nds: Node[]) =>
        nds.map((n) => {
          if (n.id === node.id) {
            return {
              ...n,
              data: { ...n.data, ...values },
            };
          }
          return n;
        })
      );
    } catch (error) {
      console.error('验证失败:', error);
    }
  };

  const handleDelete = () => {
    if (!node || !setNodes) return;
    setNodes((nds: Node[]) => nds.filter((n) => n.id !== node.id));
  };

  if (!node) {
    return (
      <Card
        style={{
          width: 300,
          borderLeft: '1px solid #2D2D2F',
          borderRadius: 0,
          background: '#121218',
        }}
      >
        <div style={{ color: '#6E6E73', textAlign: 'center', padding: '60px 20px' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🎯</div>
          <div style={{ fontWeight: 500, marginBottom: 8 }}>点击节点编辑属性</div>
          <div style={{ fontSize: 12, color: '#4A4A4F' }}>
            选择画布中的节点以查看和编辑其配置
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card
      style={{
        width: 300,
        borderLeft: '1px solid #2D2D2F',
        borderRadius: 0,
        background: '#121218',
      }}
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>节点属性</span>
          <Space>
            <Button
              type="text"
              danger
              size="small"
              icon={<DeleteOutlined />}
              onClick={handleDelete}
            >
              删除
            </Button>
          </Space>
        </div>
      }
      size="small"
    >
      <Form form={form} layout="vertical" onValuesChange={handleSave}>
        <Form.Item label="节点 ID" style={{ marginBottom: 12 }}>
          <Input value={node.id} disabled style={{ background: '#1D1D1F', borderColor: '#2D2D2F', color: '#6E6E73' }} />
        </Form.Item>

        <Form.Item label="节点类型" style={{ marginBottom: 12 }}>
          <Input value={node.type} disabled style={{ background: '#1D1D1F', borderColor: '#2D2D2F', color: '#6E6E73' }} />
        </Form.Item>

        <Form.Item label="标签" name="label" style={{ marginBottom: 12 }}>
          <Input placeholder="输入节点标签" style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }} />
        </Form.Item>

        {node.type === 'action' && (
          <>
            <Form.Item label="动作类型" name="actionType" style={{ marginBottom: 12 }}>
              <Select placeholder="选择动作类型" style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }}>
                <Select.Option value="login">🔐 登录</Select.Option>
                <Select.Option value="navigate">🧭 导航</Select.Option>
                <Select.Option value="click">👆 点击</Select.Option>
                <Select.Option value="type">⌨️ 输入</Select.Option>
                <Select.Option value="wait">⏱️ 等待</Select.Option>
                <Select.Option value="download">📥 下载</Select.Option>
              </Select>
            </Form.Item>

            <Form.Item label="CSS/XPath 选择器" name="selector" style={{ marginBottom: 12 }}>
              <Input placeholder="例如：#login-btn, //button[@id='submit']" style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }} />
            </Form.Item>

            <Form.Item label="输入值" name="value" style={{ marginBottom: 12 }}>
              <Input.TextArea
                placeholder="输入要输入的文本"
                rows={3}
                style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }}
              />
            </Form.Item>

            <Form.Item label="目标 URL" name="url" style={{ marginBottom: 12 }}>
              <Input placeholder="https://..." style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }} />
            </Form.Item>

            <Form.Item label="用户名" name="username" style={{ marginBottom: 12 }}>
              <Input placeholder="登录用户名" style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }} />
            </Form.Item>

            <Form.Item label="密码" name="password" style={{ marginBottom: 12 }}>
              <Input.Password placeholder="登录密码" style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }} />
            </Form.Item>

            <Form.Item label="等待时间 (毫秒)" name="waitTime" style={{ marginBottom: 12 }}>
              <InputNumber
                placeholder="1000"
                min={0}
                step={100}
                style={{ width: '100%', background: '#1D1D1F', borderColor: '#2D2D2F' }}
              />
            </Form.Item>
          </>
        )}

        {node.type === 'condition' && (
          <>
            <Form.Item label="条件表达式" name="condition" style={{ marginBottom: 12 }}>
              <Input.TextArea
                placeholder="例如：element.exists() && element.visible()"
                rows={4}
                style={{ background: '#1D1D1F', borderColor: '#2D2D2F' }}
              />
            </Form.Item>
          </>
        )}

        <Button type="primary" icon={<SaveOutlined />} onClick={handleSave} block>
          保存更改
        </Button>
      </Form>
    </Card>
  );
};

export default PropertiesPanel;
