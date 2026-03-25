# 智下载前端

基于 Ant Design Pro 5.x + React Flow 的浏览器自动化管理后台。

## 技术栈

- **框架**: Umi 4 + React 18
- **UI 组件**: Ant Design 5 + ProComponents
- **流程图**: React Flow 11
- **截图标注**: React Konva
- **状态管理**: Zustand
- **HTTP 客户端**: Axios

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 目录结构

```
src/
├── pages/              # 页面
│   ├── Dashboard/      # 仪表盘
│   ├── Organization/   # 组织管理
│   ├── System/         # 业务系统
│   ├── Workflow/       # 流程管理
│   ├── Task/           # 任务管理
│   └── File/           # 文件管理
├── components/         # 组件
│   ├── WorkflowCanvas/ # 流程画布
│   ├── ScreenshotAnnotator/ # 截图标注
│   └── TaskMonitor/    # 任务监控
├── services/           # API 服务
├── stores/             # 状态管理
├── utils/              # 工具函数
└── types/              # TypeScript 类型定义
```

## 开发规范

- 使用 TypeScript 编写代码
- 遵循 ESLint + Prettier 规范
- 组件使用函数式 + Hooks
- 状态管理使用 Zustand

## 相关链接

- [Ant Design 5](https://ant.design/)
- [ProComponents](https://pro-components.antdigital.dev/)
- [React Flow](https://reactflow.dev/)
- [UmiJS 4](https://umijs.org/)
