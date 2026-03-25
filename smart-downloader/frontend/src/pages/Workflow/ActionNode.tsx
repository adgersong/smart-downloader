import React from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import {
  LoginOutlined,
  ArrowRightOutlined,
  ClickOutlined,
  EditOutlined,
  ClockCircleOutlined,
  DownloadOutlined,
} from '@ant-design/icons';

export interface ActionNodeData {
  label: string;
  actionType?: 'login' | 'navigate' | 'click' | 'type' | 'wait' | 'download';
  selector?: string;
  value?: string;
  url?: string;
  username?: string;
  password?: string;
  waitTime?: number;
}

const nodeConfig: Record<string, { label: string; icon: React.ReactNode; color: string }> = {
  login: { label: '登录', icon: <LoginOutlined />, color: '#722ED1' },
  navigate: { label: '导航', icon: <ArrowRightOutlined />, color: '#1890FF' },
  click: { label: '点击', icon: <ClickOutlined />, color: '#52C41A' },
  type: { label: '输入', icon: <EditOutlined />, color: '#FA8C16' },
  wait: { label: '等待', icon: <ClockCircleOutlined />, color: '#86868B' },
  download: { label: '下载', icon: <DownloadOutlined />, color: '#EB2F96' },
};

const ActionNode: React.FC<NodeProps<Node<ActionNodeData>>> = ({ data }) => {
  const config = nodeConfig[data.actionType || 'login'];

  return (
    <div
      style={{
        background: `linear-gradient(135deg, ${config.color} 0%, ${config.color}DD 100%)`,
        border: `1px solid ${config.color}AA`,
        borderRadius: 8,
        padding: 12,
        minWidth: 160,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
      }}
    >
      <Handle type="target" position={Position.Top} />
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          fontWeight: 'bold',
          marginBottom: 8,
          color: '#FFFFFF',
        }}
      >
        <span style={{ fontSize: 16 }}>{config.icon}</span>
        <span>{data.label || config.label}</span>
      </div>

      {data.actionType && data.actionType !== 'login' && (
        <div
          style={{
            fontSize: 11,
            color: 'rgba(255,255,255,0.8)',
            marginBottom: 4,
            background: 'rgba(0,0,0,0.2)',
            padding: '2px 6px',
            borderRadius: 4,
            display: 'inline-block',
          }}
        >
          {config.label}
        </div>
      )}

      {data.selector && (
        <div
          style={{
            fontSize: 10,
            color: 'rgba(255,255,255,0.7)',
            marginTop: 6,
            wordBreak: 'break-all',
            background: 'rgba(0,0,0,0.15)',
            padding: '4px 6px',
            borderRadius: 4,
          }}
        >
          <span style={{ opacity: 0.6 }}>选择器:</span> {data.selector}
        </div>
      )}

      {data.url && (
        <div
          style={{
            fontSize: 10,
            color: 'rgba(255,255,255,0.7)',
            marginTop: 4,
            wordBreak: 'break-all',
            background: 'rgba(0,0,0,0.15)',
            padding: '4px 6px',
            borderRadius: 4,
          }}
        >
          <span style={{ opacity: 0.6 }}>URL:</span> {data.url}
        </div>
      )}

      {data.username && (
        <div
          style={{
            fontSize: 10,
            color: 'rgba(255,255,255,0.7)',
            marginTop: 4,
            background: 'rgba(0,0,0,0.15)',
            padding: '4px 6px',
            borderRadius: 4,
          }}
        >
          <span style={{ opacity: 0.6 }}>用户名:</span> {data.username}
        </div>
      )}

      {data.waitTime && (
        <div
          style={{
            fontSize: 10,
            color: 'rgba(255,255,255,0.7)',
            marginTop: 4,
            background: 'rgba(0,0,0,0.15)',
            padding: '4px 6px',
            borderRadius: 4,
          }}
        >
          <span style={{ opacity: 0.6 }}>等待:</span> {data.waitTime}ms
        </div>
      )}

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default ActionNode;
