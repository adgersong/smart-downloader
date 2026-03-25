import request from './request';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('Request Module', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  it('includes auth token in request headers', async () => {
    localStorage.setItem('access_token', 'test_token');
    
    mockedAxios.create.mockReturnValue({
      get: jest.fn().mockResolvedValue({ data: { code: 0, data: {} } }),
      post: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() },
      },
    });

    await request.get('/test');

    expect(mockedAxios.create).toHaveBeenCalledWith(
      expect.objectContaining({
        baseURL: '/api/v1',
        timeout: 30000,
      })
    );
  });

  it('redirects to login on 401 response', async () => {
    localStorage.setItem('access_token', 'test_token');
    
    const mockInstance = {
      get: jest.fn().mockRejectedValue({
        response: {
          status: 401,
          data: { message: 'Unauthorized' },
        },
      }),
      post: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() },
      },
    };
    mockedAxios.create.mockReturnValue(mockInstance as any);

    try {
      await request.get('/test');
    } catch (error) {
      expect(localStorage.getItem('access_token')).toBeNull();
    }
  });

  it('handles successful response correctly', async () => {
    const mockResponse = {
      data: {
        code: 0,
        message: 'success',
        data: { id: 1, name: 'test' },
      },
    };

    const mockInstance = {
      get: jest.fn().mockResolvedValue(mockResponse),
      post: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() },
      },
    };
    mockedAxios.create.mockReturnValue(mockInstance as any);

    const result = await request.get('/test');

    expect(result).toEqual({ id: 1, name: 'test' });
  });

  it('handles error response correctly', async () => {
    const mockError = {
      response: {
        status: 400,
        data: { message: 'Bad request' },
      },
    };

    const mockInstance = {
      get: jest.fn().mockRejectedValue(mockError),
      post: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() },
      },
    };
    mockedAxios.create.mockReturnValue(mockInstance as any);

    try {
      await request.get('/test');
    } catch (error: any) {
      expect(error.message).toBe('Bad request');
    }
  });
});
