import * as organizationApi from './organization';
import request from './request';

jest.mock('./request', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
}));

describe('Organization Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('gets organization list with pagination', async () => {
    const mockResponse = {
      items: [
        { id: 1, name: 'Org 1' },
        { id: 2, name: 'Org 2' },
      ],
      pagination: {
        page: 1,
        size: 20,
        total: 2,
        total_pages: 1,
      },
    };
    (request.get as jest.Mock).mockResolvedValue(mockResponse);

    const result = await organizationApi.getOrganizations({ page: 1, size: 20 });

    expect(request.get).toHaveBeenCalledWith('/organizations', {
      params: { page: 1, size: 20 },
    });
    expect(result).toEqual(mockResponse);
  });

  it('gets organization by id', async () => {
    const mockOrg = { id: 1, name: 'Test Org' };
    (request.get as jest.Mock).mockResolvedValue(mockOrg);

    const result = await organizationApi.getOrganization(1);

    expect(request.get).toHaveBeenCalledWith('/organizations/1');
    expect(result).toEqual(mockOrg);
  });

  it('creates organization', async () => {
    const mockOrg = { id: 1, name: 'New Org' };
    (request.post as jest.Mock).mockResolvedValue(mockOrg);

    const result = await organizationApi.createOrganization({ name: 'New Org' });

    expect(request.post).toHaveBeenCalledWith('/organizations', {
      name: 'New Org',
    });
    expect(result).toEqual(mockOrg);
  });

  it('updates organization', async () => {
    const mockOrg = { id: 1, name: 'Updated Org' };
    (request.put as jest.Mock).mockResolvedValue(mockOrg);

    const result = await organizationApi.updateOrganization(1, {
      name: 'Updated Org',
    });

    expect(request.put).toHaveBeenCalledWith('/organizations/1', {
      name: 'Updated Org',
    });
    expect(result).toEqual(mockOrg);
  });

  it('deletes organization', async () => {
    (request.delete as jest.Mock).mockResolvedValue({});

    await organizationApi.deleteOrganization(1);

    expect(request.delete).toHaveBeenCalledWith('/organizations/1');
  });
});
