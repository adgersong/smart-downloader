import React from 'react';
import WorkflowCanvas from './WorkflowCanvas';

const WorkflowPage: React.FC = () => {
  return (
    <div style={{ height: 'calc(100vh - 88px)' }}>
      <WorkflowCanvas />
    </div>
  );
};

export default WorkflowPage;
