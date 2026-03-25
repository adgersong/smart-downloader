import React from 'react';
import { Handle, Position, NodeProps, Node } from '@xyflow/react';

interface ConditionNodeData {
  label: string;
  condition?: string;
}

const ConditionNode: React.FC<NodeProps<Node<ConditionNodeData>>> = ({
  data,
}) => {
  return (
    <div
      style={{
        background: 'linear-gradient(135deg, #0071E3 0%, #007AFF 100%)',
        border: '1px solid #005BB5',
        borderRadius: 8,
        padding: 12,
        minWidth: 150,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 'bold', marginBottom: 4 }}>{data.label}</div>
      {data.condition && (
        <div style={{ fontSize: 12, color: '#E8F0FE' }}>
          {data.condition}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default ConditionNode;
