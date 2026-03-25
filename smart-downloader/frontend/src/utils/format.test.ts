import { formatFileSize } from './format';

describe('formatFileSize', () => {
  it('格式化字节', () => {
    expect(formatFileSize(500)).toBe('500 B');
  });

  it('格式化 KB', () => {
    expect(formatFileSize(1024)).toBe('1.00 KB');
    expect(formatFileSize(2048)).toBe('2.00 KB');
  });

  it('格式化 MB', () => {
    expect(formatFileSize(1024 * 1024)).toBe('1.00 MB');
    expect(formatFileSize(2.5 * 1024 * 1024)).toBe('2.50 MB');
  });

  it('格式化 GB', () => {
    expect(formatFileSize(1024 * 1024 * 1024)).toBe('1.00 GB');
    expect(formatFileSize(2.5 * 1024 * 1024 * 1024)).toBe('2.50 GB');
  });
});
