import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

describe('Dashboard Page', () => {
  it('renders dashboard title', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('仪表盘')).toBeInTheDocument();
  });

  it('renders all statistic cards', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('组织数')).toBeInTheDocument();
    expect(screen.getByText('流程数')).toBeInTheDocument();
    expect(screen.getByText('任务数')).toBeInTheDocument();
    expect(screen.getByText('文件数')).toBeInTheDocument();
  });

  it('renders correct initial values', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('12')).toBeInTheDocument();
    expect(screen.getByText('45')).toBeInTheDocument();
    expect(screen.getByText('156')).toBeInTheDocument();
    expect(screen.getByText('1,234')).toBeInTheDocument();
  });

  it('renders recent tasks card', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('最近任务')).toBeInTheDocument();
  });

  it('renders system health card', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('系统健康状态')).toBeInTheDocument();
  });
});
