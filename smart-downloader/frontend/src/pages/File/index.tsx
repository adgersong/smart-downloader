import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Table, Button, Space, message, Modal, Image, Drawer } from 'antd';
import {
  DownloadOutlined,
  DeleteOutlined,
  EyeOutlined,
  FilePdfOutlined,
  FileExcelOutlined,
  FileWordOutlined,
  FileImageOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import request from '@/services/request';

interface FileItem {
  id: number;
  name: string;
  size: number;
  mime_type: string;
  workflow_id: number;
  workflow_name: string;
  task_id: number;
  downloaded_at: string;
  url?: string;
}

interface FileListParams {
  page?: number;
  size?: number;
  workflow_id?: number;
}

interface FileListResponse {
  items: FileItem[];
  pagination: {
    page: number;
    size: number;
    total: number;
  };
}

const FileList: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewFile, setPreviewFile] = useState<FileItem | null>(null);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<FileItem | null>(null);

  const fetchFiles = async (params: FileListParams = {}) => {
    setLoading(true);
    try {
      const response: FileListResponse = await request.get('/files', {
        params: {
          page: params.page || pagination.current,
          size: params.size || pagination.pageSize,
          workflow_id: params.workflow_id,
        },
      });
      setFiles(response.items);
      setPagination({
        current: response.pagination.page,
        pageSize: response.pagination.size,
        total: response.pagination.total,
      });
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '加载文件列表失败';
      message.error(messageText);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleDownload = async (file: FileItem) => {
    try {
      const response = await request.get(`/files/${file.id}/download`, {
        responseType: 'blob',
      });
      
      const blob = new Blob([response]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      message.success(`开始下载：${file.name}`);
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '下载失败';
      message.error(messageText);
    }
  };

  const handlePreview = (file: FileItem) => {
    setPreviewFile(file);
    setPreviewOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!fileToDelete) return;
    try {
      await request.delete(`/files/${fileToDelete.id}`);
      message.success('文件已删除');
      setDeleteModalOpen(false);
      fetchFiles();
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '删除失败';
      message.error(messageText);
    }
  };

  const getFileIcon = (mimeType: string) => {
    if (mimeType.includes('pdf')) return <FilePdfOutlined />;
    if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return <FileExcelOutlined />;
    if (mimeType.includes('word')) return <FileWordOutlined />;
    if (mimeType.includes('image')) return <FileImageOutlined />;
    return <FileImageOutlined />;
  };

  const isImage = (mimeType: string) => mimeType.startsWith('image/');
  const isPdf = (mimeType: string) => mimeType === 'application/pdf';

  const columns: ColumnsType<FileItem> = [
    {
      title: '文件名',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record) => (
        <Space>
          <span style={{ fontSize: 18, color: '#1890FF' }}>
            {getFileIcon(record.mime_type)}
          </span>
          <span>{name}</span>
        </Space>
      ),
    },
    {
      title: '大小',
      dataIndex: 'size',
      key: 'size',
      render: (size: number) => {
        if (size >= 1024 * 1024) {
          return `${(size / (1024 * 1024)).toFixed(2)} MB`;
        }
        return `${(size / 1024).toFixed(2)} KB`;
      },
    },
    {
      title: '来源流程',
      dataIndex: 'workflow_name',
      key: 'workflow_name',
    },
    {
      title: '下载时间',
      dataIndex: 'downloaded_at',
      key: 'downloaded_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handlePreview(record)}
          >
            预览
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => handleDownload(record)}
          >
            下载
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => {
              setFileToDelete(record);
              setDeleteModalOpen(true);
            }}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <PageContainer title="文件管理">
      <Table
        columns={columns}
        dataSource={files}
        loading={loading}
        rowKey="id"
        pagination={{
          current: pagination.current,
          pageSize: pagination.pageSize,
          total: pagination.total,
          showSizeChanger: true,
          showTotal: (total) => `共 ${total} 个文件`,
          pageSizeOptions: ['10', '20', '50', '100'],
          onChange: (page, pageSize) => {
            setPagination({ ...pagination, current: page, pageSize });
            fetchFiles({ page, size: pageSize });
          },
        }}
      />

      <Drawer
        title="文件预览"
        placement="right"
        width={800}
        open={previewOpen}
        onClose={() => {
          setPreviewOpen(false);
          setPreviewFile(null);
        }}
      >
        {previewFile && (
          <div style={{ textAlign: 'center' }}>
            {isImage(previewFile.mime_type) ? (
              <Image
                src={previewFile.url}
                alt={previewFile.name}
                style={{ maxWidth: '100%' }}
              />
            ) : isPdf(previewFile.mime_type) ? (
              <div style={{ background: '#f5f5f5', padding: 20, borderRadius: 8 }}>
                <FilePdfOutlined style={{ fontSize: 48, color: '#ff4d4f' }} />
                <p style={{ marginTop: 16 }}>PDF 预览功能开发中</p>
                <p style={{ color: '#666', fontSize: 12 }}>
                  文件名：{previewFile.name}
                  <br />
                  大小：{(previewFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            ) : (
              <div style={{ background: '#f5f5f5', padding: 40, borderRadius: 8 }}>
                {getFileIcon(previewFile.mime_type)}
                <p style={{ marginTop: 16 }}>该文件类型暂不支持预览</p>
                <Button
                  type="primary"
                  icon={<DownloadOutlined />}
                  onClick={() => handleDownload(previewFile)}
                  style={{ marginTop: 16 }}
                >
                  下载文件
                </Button>
              </div>
            )}
          </div>
        )}
      </Drawer>

      <Modal
        title="确认删除"
        open={deleteModalOpen}
        onOk={handleDeleteConfirm}
        onCancel={() => {
          setDeleteModalOpen(false);
          setFileToDelete(null);
        }}
        okText="删除"
        cancelText="取消"
        okButtonProps={{ danger: true }}
      >
        <p>确定要删除文件 <strong>{fileToDelete?.name}</strong> 吗？</p>
        <p style={{ color: '#faad14', fontSize: 12 }}>
          此操作不可恢复，文件将被永久删除。
        </p>
      </Modal>
    </PageContainer>
  );
};

export default FileList;
