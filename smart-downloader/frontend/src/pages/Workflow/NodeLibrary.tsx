import React from 'react';
import { Card, List } from 'antd';
import {
  LoginOutlined,
  ArrowRightOutlined,
  ClickOutlined,
  EditOutlined,
  ClockCircleOutlined,
  DownloadOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';

interface NodeLibraryProps {
  onAddNode: (type: string, actionType?: string) => void;
}

interface NodeType {
  type: 'action' | 'condition';
  actionType?: string;
  label: string;
  icon: React.ReactNode;
  color: string;
  description: string;
}

const nodeTypes: NodeType[] = [
  {
    type: 'action',
    actionType: 'login',
    label: '登录',
    icon: <LoginOutlined />,
    color: '#722ED1',
    description: '登录到系统',
  },
  {
    type: 'action',
    actionType: 'navigate',
    label: '导航',
    icon: <ArrowRightOutlined />,
    color: '#1890FF',
    description: '导航到 URL',
  },
  {
    type: 'action',
    actionType: 'click',
    label: '点击',
    icon: <ClickOutlined />,
    color: '#52C41A',
    description: '点击元素',
  },
  {
    type: 'action',
    actionType: 'type',
    label: '输入',
    icon: <EditOutlined />,
    color: '#FA8C16',
    description: '输入文本',
  },
  {
    type: 'action',
    actionType: 'wait',
    label: '等待',
    icon: <ClockCircleOutlined />,
    color: '#86868B',
    description: '等待指定时间',
  },
  {
    type: 'action',
    actionType: 'download',
    label: '下载',
    icon: <DownloadOutlined />,
    color: '#EB2F96',
    description: '下载文件',
  },
  {
    type: 'condition',
    label: '条件',
    icon: <QuestionCircleOutlined />,
    color: '#0071E3',
    description: '条件判断',
  },
];

const NodeLibrary: React.FC<NodeLibraryProps> = ({ onAddNode }) => {
  return (
    <Card
      style={{
        width: 220,
        borderRight: '1px solid #2D2D2F',
        borderRadius: 0,
        background: '#121218',
        overflowY: 'auto',
      }}
      title="节点库"
      size="small"
    >
      <List
        dataSource={nodeTypes}
        renderItem={(item) => (
          <List.Item
            onClick={() => onAddNode(item.type, item.actionType)}
            style={{
              cursor: 'pointer',
              padding: '10px 12px',
              borderRadius: 6,
              marginBottom: 6,
              background: '#1D1D1F',
              border: `1px solid ${item.color}33`,
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = `${item.color}22`;
              e.currentTarget.style.borderColor = `${item.color}66`;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#1D1D1F';
              e.currentTarget.style.borderColor = `${item.color}33`;
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%' }}>
              <span
                style={{
                  fontSize: 18,
                  color: item.color,
                }}
              >
                {item.icon}
              </span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 500, color: '#E8E8ED', fontSize: 13 }}>
                  {item.label}
                </div>
                <div style={{ fontSize: 11, color: '#6E6E73', marginTop: 2 }}>
                  {item.description}
                </div>
              </div>
            </div>
          </List.Item>
        )}
      />
      <div
        style={{
          marginTop: 16,
          padding: '12px',
          background: '#1D1D1F',
          borderRadius: 6,
          fontSize: 11,
          color: '#6E6E73',
        }}
      >
        <div style={{ marginBottom: 4 }}>💡 使用提示</div>
        <div>• 点击节点添加到画布</div>
        <div>• 拖拽节点调整位置</div>
        <div>• 点击节点编辑属性</div>
      </div>
    </Card>
  );
};

export default NodeLibrary;
