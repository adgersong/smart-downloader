module.exports = {
  history: {
    push: jest.fn(),
    replace: jest.fn(),
  },
  useModel: jest.fn(() => ({
    initialState: {},
    loading: false,
  })),
  Helmet: ({ children }) => children,
};
