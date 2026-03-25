import React from 'react';
import { Button, Space, Tooltip } from 'antd';
import {
  SaveOutlined,
  UndoOutlined,
  RedoOutlined,
  PlayCircleOutlined,
  ExportOutlined,
} from '@ant-design/icons';

interface ToolbarProps {
  onSave: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onTest: () => void;
  onExport: () => void;
  readOnly?: boolean;
}

const Toolbar: React.FC<ToolbarProps> = ({
  onSave,
  onUndo,
  onRedo,
  onTest,
  onExport,
  readOnly = false,
}) => {
  return (
    <div
      style={{
        position: 'absolute',
        top: 12,
        left: 12,
        right: 12,
        zIndex: 1000,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          background: 'rgba(29, 29, 31, 0.95)',
          backdropFilter: 'blur(8px)',
          padding: '8px 16px',
          borderRadius: 8,
          boxShadow: '0 2px 12px rgba(0, 0, 0, 0.3)',
          border: '1px solid #2D2D2F',
        }}
      >
        <Space size="small">
          <Tooltip title="撤销 (Ctrl+Z)">
            <Button
              size="small"
              icon={<UndoOutlined />}
              onClick={onUndo}
              disabled={readOnly}
            >
              撤销
            </Button>
          </Tooltip>
          <Tooltip title="重做 (Ctrl+Y)">
            <Button
              size="small"
              icon={<RedoOutlined />}
              onClick={onRedo}
              disabled={readOnly}
            >
              重做
            </Button>
          </Tooltip>
        </Space>
      </div>

      <div
        style={{
          background: 'rgba(29, 29, 31, 0.95)',
          backdropFilter: 'blur(8px)',
          padding: '8px 16px',
          borderRadius: 8,
          boxShadow: '0 2px 12px rgba(0, 0, 0, 0.3)',
          border: '1px solid #2D2D2F',
        }}
      >
        <Space size="small">
          <Tooltip title="测试流程">
            <Button
              size="small"
              icon={<PlayCircleOutlined />}
              onClick={onTest}
              disabled={readOnly}
            >
              测试
            </Button>
          </Tooltip>
          <Tooltip title="导出 YAML">
            <Button
              size="small"
              icon={<ExportOutlined />}
              onClick={onExport}
            >
              导出
            </Button>
          </Tooltip>
          <Tooltip title="保存流程 (Ctrl+S)">
            <Button
              size="small"
              type="primary"
              icon={<SaveOutlined />}
              onClick={onSave}
              disabled={readOnly}
            >
              保存
            </Button>
          </Tooltip>
        </Space>
      </div>
    </div>
  );
};

export default Toolbar;
