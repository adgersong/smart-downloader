import React, { useState } from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, Form, Input, Button, Upload, message, Space } from 'antd';
import { InboxOutlined, SendOutlined } from '@ant-design/icons';
import ScreenshotAnnotator from '@/components/ScreenshotAnnotator';
import request from '@/services/request';

const { TextArea } = Input;
const { Dragger } = Upload;

const WorkflowCreate: React.FC = () => {
  const [form] = Form.useForm();
  const [mode, setMode] = useState<'text' | 'screenshot'>('text');
  const [screenshotUrl, setScreenshotUrl] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [generatedYaml, setGeneratedYaml] = useState('');

  const handleTextGenerate = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      const response = await request.post('/workflows/generate/from-text', {
        system_id: 1,
        description: values.description,
      });
      setGeneratedYaml(response.yaml_config);
      message.success('流程生成成功');
    } catch (error: any) {
      message.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleScreenshotUpload = async (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setScreenshotUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);
    return false;
  };

  const handleScreenshotGenerate = async () => {
    try {
      setLoading(true);
      // TODO: 调用截图分析 API
      message.success('流程生成成功');
    } catch (error: any) {
      message.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageContainer title="创建流程">
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button
            type={mode === 'text' ? 'primary' : 'default'}
            onClick={() => setMode('text')}
          >
            文字描述
          </Button>
          <Button
            type={mode === 'screenshot' ? 'primary' : 'default'}
            onClick={() => setMode('screenshot')}
          >
            截图生成
          </Button>
        </Space>
      </Card>

      {mode === 'text' ? (
        <Card title="文字描述生成流程">
          <Form form={form} layout="vertical">
            <Form.Item
              label="流程描述"
              name="description"
              rules={[
                { required: true, message: '请输入流程描述' },
              ]}
              extra="例如：登录后点击报表菜单，选择日报，点击下载按钮"
            >
              <TextArea
                rows={6}
                placeholder="请输入自然语言描述..."
              />
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleTextGenerate}
                loading={loading}
              >
                生成流程
              </Button>
            </Form.Item>
          </Form>
          {generatedYaml && (
            <Card title="生成的 YAML 配置" style={{ marginTop: 16 }}>
              <pre
                style={{
                  background: '#1D1D1F',
                  padding: 16,
                  borderRadius: 8,
                  overflow: 'auto',
                }}
              >
                {generatedYaml}
              </pre>
            </Card>
          )}
        </Card>
      ) : (
        <Card title="截图生成流程">
          <Dragger
            accept="image/*"
            beforeUpload={handleScreenshotUpload}
            showUploadList={false}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">点击或拖拽上传截图</p>
            <p className="ant-upload-hint">支持 PNG、JPG 格式</p>
          </Dragger>
          {screenshotUrl && (
            <>
              <Card title="标注操作区域" style={{ marginTop: 16 }}>
                <ScreenshotAnnotator imageSrc={screenshotUrl} />
              </Card>
              <Button
                type="primary"
                onClick={handleScreenshotGenerate}
                loading={loading}
                style={{ marginTop: 16 }}
              >
                生成流程
              </Button>
            </>
          )}
        </Card>
      )}
    </PageContainer>
  );
};

export default WorkflowCreate;
