import React from 'react';
import { ProLayout } from '@ant-design/pro-components';
import { Outlet, useLocation, history } from '@umijs/max';
import defaultSettings from '../../config/defaultSettings';

export default () => {
  const location = useLocation();
  
  return (
    <ProLayout
      {...defaultSettings}
      location={location}
      onMenuHeaderClick={() => history.push('/')}
      menuItemRender={(item, dom) => (
        <div onClick={() => item.path && history.push(item.path)}>
          {dom}
        </div>
      )}
    >
      <Outlet />
    </ProLayout>
  );
};
