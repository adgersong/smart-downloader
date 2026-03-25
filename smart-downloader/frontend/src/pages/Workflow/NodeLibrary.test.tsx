import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import NodeLibrary from './NodeLibrary';

describe('NodeLibrary', () => {
  const mockOnAddNode = jest.fn();

  beforeEach(() => {
    mockOnAddNode.mockClear();
  });

  it('渲染节点库标题', () => {
    render(<NodeLibrary onAddNode={mockOnAddNode} />);
    expect(screen.getByText('节点库')).toBeInTheDocument();
  });

  it('渲染所有节点类型', () => {
    render(<NodeLibrary onAddNode={mockOnAddNode} />);
    
    expect(screen.getByText('登录')).toBeInTheDocument();
    expect(screen.getByText('导航')).toBeInTheDocument();
    expect(screen.getByText('点击')).toBeInTheDocument();
    expect(screen.getByText('输入')).toBeInTheDocument();
    expect(screen.getByText('等待')).toBeInTheDocument();
    expect(screen.getByText('下载')).toBeInTheDocument();
    expect(screen.getByText('条件')).toBeInTheDocument();
  });

  it('渲染节点描述', () => {
    render(<NodeLibrary onAddNode={mockOnAddNode} />);
    
    expect(screen.getByText('登录到系统')).toBeInTheDocument();
    expect(screen.getByText('导航到 URL')).toBeInTheDocument();
    expect(screen.getByText('点击元素')).toBeInTheDocument();
    expect(screen.getByText('输入文本')).toBeInTheDocument();
    expect(screen.getByText('等待指定时间')).toBeInTheDocument();
    expect(screen.getByText('下载文件')).toBeInTheDocument();
    expect(screen.getByText('条件判断')).toBeInTheDocument();
  });

  it('点击节点调用 onAddNode', () => {
    render(<NodeLibrary onAddNode={mockOnAddNode} />);
    
    fireEvent.click(screen.getByText('登录'));
    expect(mockOnAddNode).toHaveBeenCalledWith('action', 'login');
    
    fireEvent.click(screen.getByText('点击'));
    expect(mockOnAddNode).toHaveBeenCalledWith('action', 'click');
    
    fireEvent.click(screen.getByText('条件'));
    expect(mockOnAddNode).toHaveBeenCalledWith('condition', undefined);
  });

  it('渲染使用提示', () => {
    render(<NodeLibrary onAddNode={mockOnAddNode} />);
    
    expect(screen.getByText('💡 使用提示')).toBeInTheDocument();
    expect(screen.getByText('• 点击节点添加到画布')).toBeInTheDocument();
    expect(screen.getByText('• 拖拽节点调整位置')).toBeInTheDocument();
    expect(screen.getByText('• 点击节点编辑属性')).toBeInTheDocument();
  });

  it('节点列表有正确的数量', () => {
    const { container } = render(<NodeLibrary onAddNode={mockOnAddNode} />);
    const listItems = container.querySelectorAll('.ant-list-item');
    expect(listItems).toHaveLength(7);
  });
});
