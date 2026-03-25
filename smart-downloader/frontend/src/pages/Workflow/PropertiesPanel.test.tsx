import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PropertiesPanel from './PropertiesPanel';
import { Node } from '@xyflow/react';

const mockSetNodes = jest.fn();

describe('PropertiesPanel', () => {
  const createNode = (id: string, type: string, data: any): Node => ({
    id,
    type,
    position: { x: 0, y: 0 },
    data,
  });

  beforeEach(() => {
    mockSetNodes.mockClear();
  });

  it('渲染空状态', () => {
    render(<PropertiesPanel node={null} setNodes={mockSetNodes} />);
    expect(screen.getByText('点击节点编辑属性')).toBeInTheDocument();
  });

  it('渲染节点 ID', () => {
    const node = createNode('test-123', 'action', { label: '测试' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByDisplayValue('test-123')).toBeInTheDocument();
  });

  it('渲染节点类型', () => {
    const node = createNode('1', 'action', { label: '测试' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByDisplayValue('action')).toBeInTheDocument();
  });

  it('渲染标签输入框', () => {
    const node = createNode('1', 'action', { label: '我的节点' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('输入节点标签')).toHaveValue('我的节点');
  });

  it('渲染动作类型选择器', () => {
    const node = createNode('1', 'action', { label: '点击', actionType: 'click' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByText('🔐 登录')).toBeInTheDocument();
    expect(screen.getByText('👆 点击')).toBeInTheDocument();
    expect(screen.getByText('🧭 导航')).toBeInTheDocument();
  });

  it('渲染选择器输入框', () => {
    const node = createNode('1', 'action', { label: '点击', selector: '#submit' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('例如：#login-btn')).toHaveValue('#submit');
  });

  it('渲染 URL 输入框', () => {
    const node = createNode('1', 'action', { label: '导航', url: 'https://example.com' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('https://...')).toHaveValue('https://example.com');
  });

  it('渲染用户名输入框', () => {
    const node = createNode('1', 'action', { label: '登录', username: 'admin' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('登录用户名')).toHaveValue('admin');
  });

  it('渲染密码输入框', () => {
    const node = createNode('1', 'action', { label: '登录', password: 'secret' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('登录密码')).toBeInTheDocument();
  });

  it('渲染等待时间输入框', () => {
    const node = createNode('1', 'action', { label: '等待', waitTime: 2000 });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('1000')).toHaveValue(2000);
  });

  it('渲染条件表达式输入框', () => {
    const node = createNode('1', 'condition', { label: '条件', condition: 'element.exists()' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByPlaceholderText('例如：element.exists()')).toHaveValue('element.exists()');
  });

  it('调用 setNodes 更新节点', () => {
    const node = createNode('1', 'action', { label: '原标签' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    
    const labelInput = screen.getByPlaceholderText('输入节点标签');
    fireEvent.change(labelInput, { target: { value: '新标签' } });
    
    expect(mockSetNodes).toHaveBeenCalled();
  });

  it('显示删除按钮', () => {
    const node = createNode('1', 'action', { label: '测试' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    expect(screen.getByText('删除')).toBeInTheDocument();
  });

  it('点击删除调用 setNodes', () => {
    const node = createNode('1', 'action', { label: '测试' });
    render(<PropertiesPanel node={node} setNodes={mockSetNodes} />);
    
    fireEvent.click(screen.getByText('删除'));
    
    expect(mockSetNodes).toHaveBeenCalledWith(expect.any(Function));
  });
});
