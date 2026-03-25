import { create } from 'zustand';

interface UserState {
  userInfo: {
    id: number;
    username: string;
    email: string;
    role: string;
    org_id: number;
    org_name: string;
  } | null;
  isAuthenticated: boolean;
  setUserInfo: (user: UserState['userInfo']) => void;
  clearUserInfo: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  userInfo: null,
  isAuthenticated: false,
  setUserInfo: (user) =>
    set({
      userInfo: user,
      isAuthenticated: !!user,
    }),
  clearUserInfo: () =>
    set({
      userInfo: null,
      isAuthenticated: false,
    }),
}));
