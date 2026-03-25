import { convertToYaml } from './WorkflowCanvas';
import { Node, Edge } from '@xyflow/react';

describe('convertToYaml', () => {
  const createNode = (id: string, type: string, actionType: string, position = { x: 0, y: 0 }): Node => ({
    id,
    type,
    position,
    data: {
      label: `${actionType}节点`,
      actionType,
      selector: actionType === 'click' ? '#btn' : undefined,
      url: actionType === 'navigate' ? 'https://example.com' : undefined,
      waitTime: actionType === 'wait' ? 1000 : undefined,
    },
  } as any);

  const createEdge = (source: string, target: string): Edge => ({
    id: `e-${source}-${target}`,
    source,
    target,
  });

  it('转换单个节点为 YAML', () => {
    const nodes = [createNode('1', 'action', 'login')];
    const edges: Edge[] = [];
    const yaml = convertToYaml(nodes, edges);
    
    expect(yaml).toContain('workflow:');
    expect(yaml).toContain('name: "自动化流程"');
    expect(yaml).toContain('steps:');
    expect(yaml).toContain('- action: login');
  });

  it('转换多个节点为 YAML', () => {
    const nodes = [
      createNode('1', 'action', 'login', { x: 0, y: 0 }),
      createNode('2', 'action', 'navigate', { x: 0, y: 100 }),
      createNode('3', 'action', 'click', { x: 0, y: 200 }),
    ];
    const edges: Edge[] = [];
    const yaml = convertToYaml(nodes, edges);
    
    expect(yaml).toContain('- action: login');
    expect(yaml).toContain('- action: navigate');
    expect(yaml).toContain('- action: click');
  });

  it('按 Y 坐标排序节点', () => {
    const nodes = [
      createNode('1', 'action', 'click', { x: 0, y: 200 }),
      createNode('2', 'action', 'login', { x: 0, y: 0 }),
      createNode('3', 'action', 'navigate', { x: 0, y: 100 }),
    ];
    const yaml = convertToYaml(nodes, []);
    
    const loginIndex = yaml.indexOf('action: login');
    const navigateIndex = yaml.indexOf('action: navigate');
    const clickIndex = yaml.indexOf('action: click');
    
    expect(loginIndex).toBeLessThan(navigateIndex);
    expect(navigateIndex).toBeLessThan(clickIndex);
  });

  it('包含 URL 信息', () => {
    const nodes = [createNode('1', 'action', 'navigate')];
    const yaml = convertToYaml(nodes, []);
    
    expect(yaml).toContain('url: "https://example.com"');
  });

  it('包含选择器信息', () => {
    const nodes = [createNode('1', 'action', 'click')];
    const yaml = convertToYaml(nodes, []);
    
    expect(yaml).toContain('selector: "#btn"');
  });

  it('包含等待时间信息', () => {
    const nodes = [createNode('1', 'action', 'wait')];
    const yaml = convertToYaml(nodes, []);
    
    expect(yaml).toContain('wait_time: 1000');
  });

  it('生成有效的 YAML 格式', () => {
    const nodes = [
      createNode('1', 'action', 'login', { x: 0, y: 0 }),
      createNode('2', 'action', 'navigate', { x: 0, y: 100 }),
    ];
    const yaml = convertToYaml(nodes, []);
    
    expect(yaml).toMatch(/^workflow:\s*$/m);
    expect(yaml).toMatch(/^\s*name:/m);
    expect(yaml).toMatch(/^\s*version:/m);
    expect(yaml).toMatch(/^\s*steps:\s*$/m);
  });
});
