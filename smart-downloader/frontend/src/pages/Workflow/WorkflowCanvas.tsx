import React, { useCallback, useState, useRef } from 'react';
import {
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap,
  Background,
  Connection,
  Edge,
  Node,
  ControlsPosition,
  MiniMapPosition,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { message } from 'antd';
import ActionNode, { ActionNodeData } from './ActionNode';
import ConditionNode from './ConditionNode';
import Toolbar from './Toolbar';
import PropertiesPanel from './PropertiesPanel';
import NodeLibrary from './NodeLibrary';

const nodeTypes = {
  action: ActionNode,
  condition: ConditionNode,
};

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'action',
    position: { x: 250, y: 100 },
    data: { label: '开始', actionType: 'login' },
  },
];

interface WorkflowCanvasProps {
  workflowId?: number;
  readOnly?: boolean;
}

const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({ workflowId, readOnly = false }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  const onConnect = useCallback(
    (params: Connection) =>
      setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#0071E3', strokeWidth: 2 } }, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      if (readOnly) return;
      setSelectedNode(node);
    },
    [readOnly]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  const handleAddNode = (type: string, actionType?: string) => {
    if (readOnly) {
      message.warning('只读模式下无法添加节点');
      return;
    }

    const newNode: Node = {
      id: `node-${Date.now()}`,
      type,
      position: {
        x: Math.random() * 400 + 100,
        y: Math.random() * 400 + 100,
      },
      data: {
        label: actionType || type,
        actionType,
      },
    };
    setNodes((nds) => nds.concat(newNode));
    message.success(`已添加 ${actionType || type} 节点`);
  };

  const handleSave = () => {
    const workflow = { nodes, edges };
    console.log('保存流程:', workflow);
    
    const yamlConfig = convertToYaml(nodes, edges);
    console.log('YAML 配置:', yamlConfig);
    
    localStorage.setItem(`workflow-${workflowId || 'draft'}`, JSON.stringify(workflow));
    message.success('流程已保存');
  };

  const handleUndo = () => {
    message.info('撤销功能开发中');
  };

  const handleRedo = () => {
    message.info('重做功能开发中');
  };

  const handleTest = () => {
    message.info('流程测试功能开发中');
  };

  const handleExportYaml = () => {
    const yamlConfig = convertToYaml(nodes, edges);
    const blob = new Blob([yamlConfig], { type: 'text/yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `workflow-${workflowId || 'draft'}.yaml`;
    a.click();
    URL.revokeObjectURL(url);
    message.success('YAML 已导出');
  };
    <div ref={reactFlowWrapper} style={{ width: '100%', height: '100%', display: 'flex' }}>
      {!readOnly && <NodeLibrary onAddNode={handleAddNode} />}
      <div style={{ flex: 1, position: 'relative' }}>
        <Toolbar
          onSave={handleSave}
          onUndo={handleUndo}
          onRedo={handleRedo}
          onTest={handleTest}
          onExport={handleExportYaml}
          readOnly={readOnly}
        />
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[15, 15]}
          deleteKeyCode={['Backspace', 'Delete']}
          onNodesDelete={(deleted) => {
            deleted.forEach((node) => {
              console.log('删除节点:', node.id);
            });
          }}
          onEdgesDelete={(deleted) => {
            deleted.forEach((edge) => {
              console.log('删除边:', edge.id);
            });
          }}
          defaultEdgeOptions={{
            style: { stroke: '#0071E3', strokeWidth: 2 },
            type: 'default',
          }}
        >
          <Background
            variant={BackgroundVariant.Dots}
            gap={20}
            size={1}
            color="#2D2D2F"
          />
          <Controls position={ControlsPosition.BottomRight} showInteractive={false} />
          <MiniMap
            position={MiniMapPosition.BottomLeft}
            nodeColor={(node) => {
              if (node.type === 'action') {
                const actionType = (node.data as ActionNodeData).actionType;
                const colors: Record<string, string> = {
                  login: '#722ED1',
                  navigate: '#1890FF',
                  click: '#52C41A',
                  type: '#FA8C16',
                  wait: '#86868B',
                  download: '#EB2F96',
                };
                return colors[actionType || 'login'];
              }
              return '#0071E3';
            }}
            maskColor="rgba(0, 0, 0, 0.6)"
          />
        </ReactFlow>
      </div>
      {!readOnly && <PropertiesPanel node={selectedNode} setNodes={setNodes} />}
    </div>
  );
};

function convertToYaml(nodes: Node[], _edges: Edge[]): string {
  const steps = nodes
    .sort((a, b) => a.position.y - b.position.y)
    .map((node) => {
      const data = node.data as ActionNodeData;
      return `  - action: ${data.actionType || 'click'}
    label: "${data.label}"
    selector: "${data.selector || ''}"
    value: "${data.value || ''}"
    ${data.url ? `url: "${data.url}"` : ''}
    ${data.waitTime ? `wait_time: ${data.waitTime}` : ''}`;
    })
    .join('\n');

  return `workflow:
  name: "自动化流程"
  version: "1.0"
  steps:
${steps}
`;
}

export default WorkflowCanvas;
export { convertToYaml };
