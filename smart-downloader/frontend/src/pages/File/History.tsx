import React, { useState, useEffect } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, Timeline, Space, Tag, Statistic, Row, Col, Button, Select, Empty } from 'antd';
import {
  DownloadOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import { RangePicker } from 'antd/es/date-picker';
import dayjs from 'dayjs';
import request from '@/services/request';

interface DownloadRecord {
  id: number;
  file_name: string;
  file_size: number;
  workflow_name: string;
  task_id: number;
  status: 'success' | 'failed' | 'pending';
  downloaded_at: string;
  downloaded_by?: string;
}

interface DownloadStats {
  total_downloads: number;
  total_size: number;
  success_rate: number;
  today_downloads: number;
}

const DownloadHistory: React.FC = () => {
  const [records, setRecords] = useState<DownloadRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<DownloadStats | null>(null);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const params: Record<string, string | undefined> = {
        status: statusFilter !== 'all' ? statusFilter : undefined,
      };
      
      if (dateRange) {
        params.start_date = dateRange[0].format('YYYY-MM-DD');
        params.end_date = dateRange[1].format('YYYY-MM-DD');
      }

      const response = await request.get('/downloads/history', { params });
      setRecords(response.items || []);
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '加载下载历史失败';
      console.error(messageText);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await request.get('/downloads/stats');
      setStats(response);
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '加载统计数据失败';
      console.error(messageText);
    }
  };

  useEffect(() => {
    fetchHistory();
    fetchStats();
  }, [dateRange, statusFilter]);

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      success: 'success',
      failed: 'error',
      pending: 'processing',
    };
    return colors[status] || 'default';
  };

  const getStatusIcon = (status: string) => {
    const icons: Record<string, React.ReactNode> = {
      success: <CheckCircleOutlined />,
      failed: <CloseCircleOutlined />,
      pending: <ClockCircleOutlined />,
    };
    return icons[status] || <ClockCircleOutlined />;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes >= 1024 * 1024 * 1024) {
      return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
    }
    if (bytes >= 1024 * 1024) {
      return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    }
    if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(2)} KB`;
    }
    return `${bytes} B`;
  };

  return (
    <PageContainer
      title="下载历史"
      subTitle="查看和管理所有下载记录"
    >
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总下载数"
              value={stats?.total_downloads || 0}
              prefix={<DownloadOutlined />}
              valueStyle={{ color: '#1890FF' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总下载量"
              value={formatFileSize(stats?.total_size || 0).split(' ')[0]}
              suffix={formatFileSize(stats?.total_size || 0).split(' ')[1]}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#52C41A' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="成功率"
              value={stats?.success_rate || 100}
              suffix="%"
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#722ED1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日下载"
              value={stats?.today_downloads || 0}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#FA8C16' }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        style={{ marginBottom: 16 }}
        title="筛选条件"
      >
        <Space wrap>
          <RangePicker
            value={dateRange}
            onChange={(dates) => setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)}
            allowClear
          />
          <Select
            value={statusFilter}
            onChange={setStatusFilter}
            style={{ width: 120 }}
            options={[
              { value: 'all', label: '全部状态' },
              { value: 'success', label: '成功' },
              { value: 'failed', label: '失败' },
              { value: 'pending', label: '进行中' },
            ]}
          />
          <Button onClick={() => {
            setDateRange(null);
            setStatusFilter('all');
          }}>
            重置筛选
          </Button>
        </Space>
      </Card>

      <Card>
        {records.length === 0 ? (
          <Empty
            description="暂无下载记录"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        ) : (
          <Timeline
            items={records.map((record) => ({
              key: record.id,
              color: record.status === 'success' ? 'green' : record.status === 'failed' ? 'red' : 'blue',
              dot: getStatusIcon(record.status),
              children: (
                <Card size="small" hoverable>
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Space>
                        <span style={{ fontWeight: 500, fontSize: 14 }}>
                          {record.file_name}
                        </span>
                        <Tag color={getStatusColor(record.status)} icon={getStatusIcon(record.status)}>
                          {record.status === 'success' ? '成功' : record.status === 'failed' ? '失败' : '进行中'}
                        </Tag>
                      </Space>
                      <span style={{ color: '#6E6E73', fontSize: 12 }}>
                        {dayjs(record.downloaded_at).format('YYYY-MM-DD HH:mm:ss')}
                      </span>
                    </div>
                    <Space split={<span style={{ color: '#2D2D2F' }}>|</span>}>
                      <span style={{ fontSize: 12, color: '#4A4A4F' }}>
                        流程：{record.workflow_name}
                      </span>
                      <span style={{ fontSize: 12, color: '#4A4A4F' }}>
                        大小：{formatFileSize(record.file_size)}
                      </span>
                      {record.downloaded_by && (
                        <span style={{ fontSize: 12, color: '#4A4A4F' }}>
                          下载者：{record.downloaded_by}
                        </span>
                      )}
                    </Space>
                  </Space>
                </Card>
              ),
            }))}
          />
        )}
      </Card>
    </PageContainer>
  );
};

export default DownloadHistory;
