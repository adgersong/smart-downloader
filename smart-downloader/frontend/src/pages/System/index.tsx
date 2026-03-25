import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Table, Button, Space, Input, Tag, message, Modal, Form, Select } from 'antd';
import {
  SearchOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface SystemItem {
  id: number;
  name: string;
  url: string;
  type: string;
  description?: string;
  login_config?: Record<string, any>;
  workflow_count: number;
  has_credential: boolean;
  updated_at: string;
}

const SystemList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [systems, setSystems] = useState<SystemItem[]>([]);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSystem, setEditingSystem] = useState<SystemItem | null>(null);
  const [form] = Form.useForm();

  const fetchSystems = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/systems?org_id=1');
      const data = await response.json();
      if (data.code === 0) {
        setSystems(data.data.items);
      }
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSystems();
  }, []);

  const handleCreate = () => {
    setEditingSystem(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: SystemItem) => {
    setEditingSystem(record);
    form.setFieldsValue({
      name: record.name,
      url: record.url,
      type: record.type,
      description: record.description,
    });
    setModalVisible(true);
  };

  const handleDelete = (record: SystemItem) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除系统 "${record.name}" 吗？`,
      onOk: async () => {
        try {
          await fetch(`/api/v1/systems/${record.id}`, { method: 'DELETE' });
          message.success('删除成功');
          fetchSystems();
        } catch (error) {
          message.error('删除失败');
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const url = editingSystem
        ? `/api/v1/systems/${editingSystem.id}`
        : '/api/v1/systems';
      const method = editingSystem ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...values,
          org_id: 1,
        }),
      });

      const data = await response.json();
      if (data.code === 0) {
        message.success(editingSystem ? '更新成功' : '创建成功');
        setModalVisible(false);
        fetchSystems();
      }
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  const getTypeTag = (type: string) => {
    const types: Record<string, { color: string; text: string }> = {
      financial: { color: 'green', text: '财务系统' },
      erp: { color: 'blue', text: 'ERP 系统' },
      crm: { color: 'orange', text: 'CRM 系统' },
      custom: { color: 'default', text: '自定义' },
    };
    const config = types[type] || { color: 'default', text: type };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  const columns: ColumnsType<SystemItem> = [
    {
      title: '系统名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => getTypeTag(type),
    },
    {
      title: '流程数',
      dataIndex: 'workflow_count',
      key: 'workflow_count',
    },
    {
      title: '凭证',
      dataIndex: 'has_credential',
      key: 'has_credential',
      render: (has: boolean) =>
        has ? (
          <Tag icon={<CheckCircleOutlined />} color="success">已配置</Tag>
        ) : (
          <Tag icon={<CloseCircleOutlined />} color="error">未配置</Tag>
        ),
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      render: (text: string) => new Date(text).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const filteredSystems = systems.filter((system) =>
    system.name.toLowerCase().includes(searchKeyword.toLowerCase())
  );

  return (
    <PageContainer
      title="业务系统管理"
      extra={
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          新建系统
        </Button>
      }
    >
      <Input
        placeholder="搜索系统..."
        prefix={<SearchOutlined />}
        value={searchKeyword}
        onChange={(e) => setSearchKeyword(e.target.value)}
        style={{ width: 300, marginBottom: 16 }}
      />
      <Table
        columns={columns}
        dataSource={filteredSystems}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title={editingSystem ? '编辑系统' : '新建系统'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="系统名称"
            rules={[{ required: true, message: '请输入系统名称' }]}
          >
            <Input placeholder="请输入系统名称" />
          </Form.Item>
          <Form.Item
            name="url"
            label="系统 URL"
            rules={[
              { required: true, message: '请输入系统 URL' },
              { type: 'url', message: '请输入有效的 URL' },
            ]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>
          <Form.Item
            name="type"
            label="系统类型"
            rules={[{ required: true, message: '请选择系统类型' }]}
          >
            <Select placeholder="请选择系统类型">
              <Select.Option value="financial">财务系统</Select.Option>
              <Select.Option value="erp">ERP 系统</Select.Option>
              <Select.Option value="crm">CRM 系统</Select.Option>
              <Select.Option value="custom">自定义</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="description" label="系统描述">
            <Input.TextArea rows={3} placeholder="请输入系统描述" />
          </Form.Item>
        </Form>
      </Modal>
    </PageContainer>
  );
};

export default SystemList;
