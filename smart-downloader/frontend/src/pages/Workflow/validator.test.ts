import { validateWorkflow, getValidationSummary } from './validator';
import { Node, Edge } from '@xyflow/react';

describe('Workflow Validator', () => {
  const createNode = (id: string, type: string, actionType?: string, data = {}): Node => ({
    id,
    type,
    position: { x: 0, y: 0 },
    data: { label: '测试节点', actionType, ...data },
  });

  const createEdge = (source: string, target: string): Edge => ({
    id: `edge-${source}-${target}`,
    source,
    target,
  });

  describe('validateWorkflow', () => {
    it('空画布返回错误', () => {
      const result = validateWorkflow([], []);
      expect(result.valid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].message).toContain('至少需要包含一个节点');
    });

    it('单个节点验证通过', () => {
      const nodes = [createNode('1', 'action', 'login')];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(true);
    });

    it('空标签返回错误', () => {
      const nodes = [createNode('1', 'action', 'click', { label: '' })];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('标签不能为空'))).toBe(true);
    });

    it('导航节点缺少 URL 返回错误', () => {
      const nodes = [createNode('1', 'action', 'navigate', { selector: '' })];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('URL'))).toBe(true);
    });

    it('导航节点 URL 格式错误返回错误', () => {
      const nodes = [createNode('1', 'action', 'navigate', { url: 'not-a-url' })];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('URL 格式'))).toBe(true);
    });

    it('点击节点缺少选择器返回错误', () => {
      const nodes = [createNode('1', 'action', 'click', { selector: '' })];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('选择器'))).toBe(true);
    });

    it('输入节点缺少选择器返回错误', () => {
      const nodes = [createNode('1', 'action', 'type', { selector: '' })];
      const result = validateWorkflow(nodes, []);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.message.includes('选择器'))).toBe(true);
    });

    it('等待节点超过 60 秒返回警告', () => {
      const nodes = [createNode('1', 'action', 'wait', { waitTime: 70000 })];
      const result = validateWorkflow(nodes, []);
      expect(result.warnings.some(w => w.message.includes('60 秒'))).toBe(true);
    });

    it('完整流程验证通过', () => {
      const nodes = [
        createNode('1', 'action', 'login', { username: 'user', password: 'pass' }),
        createNode('2', 'action', 'navigate', { url: 'https://example.com' }),
        createNode('3', 'action', 'click', { selector: '#btn' }),
      ];
      const edges = [
        createEdge('1', '2'),
        createEdge('2', '3'),
      ];
      const result = validateWorkflow(nodes, edges);
      expect(result.valid).toBe(true);
    });
  });

  describe('getValidationSummary', () => {
    it('返回验证通过消息', () => {
      const result = getValidationSummary({ valid: true, errors: [], warnings: [] } as any);
      expect(result).toContain('验证通过');
    });

    it('返回带警告消息', () => {
      const result = getValidationSummary({ 
        valid: true, 
        errors: [], 
        warnings: [{ nodeId: '1', message: '警告', severity: 'warning' as const }] 
      } as any);
      expect(result).toContain('警告');
    });

    it('返回错误消息', () => {
      const result = getValidationSummary({ 
        valid: false, 
        errors: [{ nodeId: '1', message: '错误', severity: 'error' as const }], 
        warnings: [] 
      } as any);
      expect(result).toContain('错误');
    });
  });
});
