import { Node, Edge } from '@xyflow/react';
import { ActionNodeData } from './ActionNode';

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

export interface ValidationError {
  nodeId: string;
  message: string;
  severity: 'error';
}

export interface ValidationWarning {
  nodeId: string;
  message: string;
  severity: 'warning';
}

export function validateWorkflow(nodes: Node[], edges: Edge[]): ValidationResult {
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];

  if (nodes.length === 0) {
    errors.push({
      nodeId: 'canvas',
      message: '流程至少需要包含一个节点',
      severity: 'error',
    });
  }

  const nodeMap = new Map<string, Node>();
  nodes.forEach((node) => nodeMap.set(node.id, node));

  const hasStartNode = nodes.some(
    (node) => (node.data as ActionNodeData).actionType === 'login'
  );

  if (!hasStartNode) {
    warnings.push({
      nodeId: 'canvas',
      message: '建议以登录节点开始流程',
      severity: 'warning',
    });
  }

  nodes.forEach((node) => {
    const data = node.data as ActionNodeData;

    if (!data.label || data.label.trim() === '') {
      errors.push({
        nodeId: node.id,
        message: '节点标签不能为空',
        severity: 'error',
      });
    }

    if (node.type === 'action') {
      validateActionNode(node, data, errors, warnings);
    }

    const hasOutgoingEdge = edges.some((edge) => edge.source === node.id);
    const hasIncomingEdge = edges.some((edge) => edge.target === node.id);

    if (!hasOutgoingEdge && node.id !== '1') {
      warnings.push({
        nodeId: node.id,
        message: '节点没有后续连接，流程可能不完整',
        severity: 'warning',
      });
    }

    if (!hasIncomingEdge && node.id !== '1') {
      warnings.push({
        nodeId: node.id,
        message: '节点没有前置连接，可能无法执行',
        severity: 'warning',
      });
    }
  });

  const isolatedNodes = findIsolatedNodes(nodes, edges);
  isolatedNodes.forEach((nodeId) => {
    warnings.push({
      nodeId,
      message: '孤立节点，未与其他节点连接',
      severity: 'warning',
    });
  });

  const hasCycle = detectCycle(nodes, edges);
  if (hasCycle) {
    warnings.push({
      nodeId: 'canvas',
      message: '流程中存在循环，可能导致无限执行',
      severity: 'warning',
    });
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

function validateActionNode(
  node: Node,
  data: ActionNodeData,
  errors: ValidationError[],
  warnings: ValidationWarning[]
) {
  switch (data.actionType) {
    case 'login':
      if (!data.username && !data.password) {
        warnings.push({
          nodeId: node.id,
          message: '登录节点未配置用户名或密码',
          severity: 'warning',
        });
      }
      break;

    case 'navigate':
      if (!data.url) {
        errors.push({
          nodeId: node.id,
          message: '导航节点需要配置 URL',
          severity: 'error',
        });
      } else if (!isValidUrl(data.url)) {
        errors.push({
          nodeId: node.id,
          message: 'URL 格式不正确',
          severity: 'error',
        });
      }
      break;

    case 'click':
      if (!data.selector) {
        errors.push({
          nodeId: node.id,
          message: '点击节点需要配置选择器',
          severity: 'error',
        });
      }
      break;

    case 'type':
      if (!data.selector) {
        errors.push({
          nodeId: node.id,
          message: '输入节点需要配置选择器',
          severity: 'error',
        });
      }
      if (!data.value) {
        warnings.push({
          nodeId: node.id,
          message: '输入节点未配置输入值',
          severity: 'warning',
        });
      }
      break;

    case 'wait':
      if (!data.waitTime) {
        warnings.push({
          nodeId: node.id,
          message: '等待节点未配置等待时间',
          severity: 'warning',
        });
      } else if (data.waitTime > 60000) {
        warnings.push({
          nodeId: node.id,
          message: '等待时间超过 60 秒，可能导致流程执行缓慢',
          severity: 'warning',
        });
      }
      break;

    case 'download':
      if (!data.selector) {
        warnings.push({
          nodeId: node.id,
          message: '下载节点建议配置选择器以定位下载按钮',
          severity: 'warning',
        });
      }
      break;

    default:
      warnings.push({
        nodeId: node.id,
        message: `未知动作类型：${data.actionType}`,
        severity: 'warning',
      });
  }
}

function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

function findIsolatedNodes(nodes: Node[], edges: Edge[]): string[] {
  const connectedNodeIds = new Set<string>();
  
  edges.forEach((edge) => {
    connectedNodeIds.add(edge.source);
    connectedNodeIds.add(edge.target);
  });

  return nodes
    .filter((node) => !connectedNodeIds.has(node.id))
    .map((node) => node.id);
}

function detectCycle(nodes: Node[], edges: Edge[]): boolean {
  const graph = new Map<string, string[]>();
  
  nodes.forEach((node) => {
    graph.set(node.id, []);
  });

  edges.forEach((edge) => {
    const sources = graph.get(edge.source) || [];
    sources.push(edge.target);
    graph.set(edge.source, sources);
  });

  const visited = new Set<string>();
  const recursionStack = new Set<string>();

  function dfs(nodeId: string): boolean {
    if (recursionStack.has(nodeId)) {
      return true;
    }
    if (visited.has(nodeId)) {
      return false;
    }

    visited.add(nodeId);
    recursionStack.add(nodeId);

    const neighbors = graph.get(nodeId) || [];
    for (const neighbor of neighbors) {
      if (dfs(neighbor)) {
        return true;
      }
    }

    recursionStack.delete(nodeId);
    return false;
  }

  for (const nodeId of graph.keys()) {
    if (dfs(nodeId)) {
      return true;
    }
  }

  return false;
}

export function getValidationSummary(result: ValidationResult): string {
  if (result.valid && result.warnings.length === 0) {
    return '✅ 流程验证通过';
  }
  if (result.valid) {
    return `⚠️ 流程有效，但有 ${result.warnings.length} 个警告`;
  }
  return `❌ 流程无效，存在 ${result.errors.length} 个错误`;
}
