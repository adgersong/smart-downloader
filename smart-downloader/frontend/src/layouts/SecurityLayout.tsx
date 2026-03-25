import React, { useEffect, useState } from 'react';
import { Outlet, useLocation, history } from '@umijs/max';
import { Spin } from 'antd';

export default () => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token && location.pathname !== '/login') {
      history.push('/login');
    }
    setIsLoading(false);
  }, [location.pathname]);

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  return <Outlet />;
};
