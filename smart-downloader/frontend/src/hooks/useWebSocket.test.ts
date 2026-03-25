import { renderHook, act } from '@testing-library/react';
import { useWebSocket } from './useWebSocket';

const mockWebSocket = jest.fn();
global.WebSocket = mockWebSocket as any;

describe('useWebSocket Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('creates WebSocket connection on mount', () => {
    const mockWs = {
      readyState: WebSocket.OPEN,
      onopen: null,
      onclose: null,
      onmessage: null,
      onerror: null,
      close: jest.fn(),
      send: jest.fn(),
    };
    mockWebSocket.mockImplementation(() => mockWs);

    renderHook(() => useWebSocket(123));

    expect(mockWebSocket).toHaveBeenCalledWith(expect.stringContaining('/ws/tasks/123'));
  });

  it('calls onConnected callback when WebSocket opens', () => {
    const mockWs = {
      readyState: WebSocket.OPEN,
      onopen: null,
      onclose: null,
      onmessage: null,
      onerror: null,
      close: jest.fn(),
      send: jest.fn(),
    };
    mockWebSocket.mockImplementation(() => mockWs);

    const onConnected = jest.fn();
    renderHook(() => useWebSocket(123, { onConnected }));

    act(() => {
      if (mockWs.onopen) {
        mockWs.onopen();
      }
    });

    expect(onConnected).toHaveBeenCalled();
  });

  it('calls onMessage callback when message received', () => {
    const mockWs = {
      readyState: WebSocket.OPEN,
      onopen: null,
      onclose: null,
      onmessage: null,
      onerror: null,
      close: jest.fn(),
      send: jest.fn(),
    };
    mockWebSocket.mockImplementation(() => mockWs);

    const onMessage = jest.fn();
    renderHook(() => useWebSocket(123, { onMessage }));

    const testData = { type: 'log', data: { message: 'test' } };
    
    act(() => {
      if (mockWs.onmessage) {
        mockWs.onmessage({ data: JSON.stringify(testData) });
      }
    });

    expect(onMessage).toHaveBeenCalledWith(testData);
  });

  it('attempts to reconnect on disconnect', () => {
    const mockWs = {
      readyState: WebSocket.OPEN,
      onopen: null,
      onclose: null,
      onmessage: null,
      onerror: null,
      close: jest.fn(),
      send: jest.fn(),
    };
    mockWebSocket.mockImplementation(() => mockWs);

    renderHook(() => useWebSocket(123));

    act(() => {
      if (mockWs.onclose) {
        mockWs.onclose();
      }
    });

    jest.advanceTimersByTime(3000);

    expect(mockWebSocket).toHaveBeenCalledTimes(2);
  });

  it('disconnect cleans up WebSocket connection', () => {
    const mockWs = {
      readyState: WebSocket.OPEN,
      onopen: null,
      onclose: null,
      onmessage: null,
      onerror: null,
      close: jest.fn(),
      send: jest.fn(),
    };
    mockWebSocket.mockImplementation(() => mockWs);

    const { result } = renderHook(() => useWebSocket(123));

    act(() => {
      result.current.disconnect();
    });

    expect(mockWs.close).toHaveBeenCalled();
  });
});
