import React from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, Col, Row, Statistic } from 'antd';
import {
  TeamOutlined,
  AppstoreOutlined,
  CheckCircleOutlined,
  FileOutlined,
} from '@ant-design/icons';

export default () => {
  return (
    <PageContainer title="仪表盘">
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card>
            <Statistic
              title="组织数"
              value={12}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#86868B' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="流程数"
              value={45}
              prefix={<AppstoreOutlined />}
              valueStyle={{ color: '#86868B' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="任务数"
              value={156}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#86868B' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="文件数"
              value={1234}
              prefix={<FileOutlined />}
              valueStyle={{ color: '#86868B' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="最近任务">
            <div>任务列表占位</div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="系统健康状态">
            <div>健康状态占位</div>
          </Card>
        </Col>
      </Row>
    </PageContainer>
  );
};
