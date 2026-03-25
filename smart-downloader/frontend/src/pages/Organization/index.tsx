import React, { useEffect, useState } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Table, Button, Space, Modal, Form, Input, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import {
  getOrganizations,
  createOrganization,
  updateOrganization,
  deleteOrganization,
} from '@/services/organization';
import type { Organization } from '@/types/organization';

export default () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Organization[]>([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0,
  });
  const [modalVisible, setModalVisible] = useState(false);
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null);
  const [form] = Form.useForm();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getOrganizations({
        page: pagination.current,
        size: pagination.pageSize,
      });
      setData(response.items);
      setPagination((prev) => ({
        ...prev,
        total: response.pagination.total,
      }));
    } catch (error: any) {
      message.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [pagination.current, pagination.pageSize]);

  const handleCreate = () => {
    setEditingOrg(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Organization) => {
    setEditingOrg(record);
    form.setFieldsValue({ name: record.name });
    setModalVisible(true);
  };

  const handleDelete = (record: Organization) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除组织 "${record.name}" 吗？`,
      onOk: async () => {
        try {
          await deleteOrganization(record.id);
          message.success('删除成功');
          fetchData();
        } catch (error: any) {
          message.error(error.message);
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingOrg) {
        await updateOrganization(editingOrg.id, values);
        message.success('更新成功');
      } else {
        await createOrganization(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      fetchData();
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const columns: ColumnsType<Organization> = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80,
    },
    {
      title: '组织名称',
      dataIndex: 'name',
    },
    {
      title: '用户数',
      dataIndex: ['stats', 'user_count'],
      width: 100,
    },
    {
      title: '系统数',
      dataIndex: ['stats', 'system_count'],
      width: 100,
    },
    {
      title: '流程数',
      dataIndex: ['stats', 'workflow_count'],
      width: 100,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      width: 180,
      render: (text: string) => new Date(text).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
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

  return (
    <PageContainer
      title="组织管理"
      extra={
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          新建组织
        </Button>
      }
    >
      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        pagination={{
          ...pagination,
          onChange: (page, pageSize) => {
            setPagination((prev) => ({
              ...prev,
              current: page,
              pageSize,
            }));
          },
        }}
        rowKey="id"
      />

      <Modal
        title={editingOrg ? '编辑组织' : '新建组织'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="组织名称"
            rules={[{ required: true, message: '请输入组织名称' }]}
          >
            <Input placeholder="请输入组织名称" />
          </Form.Item>
        </Form>
      </Modal>
    </PageContainer>
  );
};
