import React from 'react';
import { Table as AntdTable, type TableProps as AntdTableProps } from 'antd';

interface TableProps<T = any> extends AntdTableProps<T> {}

/**
 * 基础表格组件 - 支持分页、排序、筛选
 */
export const Table = <T extends object>(props: TableProps<T>) => {
  return <AntdTable<T> {...props} />;
};
