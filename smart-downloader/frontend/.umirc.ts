import { defineConfig } from 'umi';

export default defineConfig({
  routes: [
    { path: '/login', component: './Login' },
    { 
      path: '/', 
      component: '../layouts/SecurityLayout',
      routes: [
        { path: '/', redirect: '/dashboard' },
        { path: '/dashboard', component: './Dashboard' },
        { path: '/organization', component: './Organization' },
        { path: '/system', component: './System' },
        { path: '/task', component: './Task' },
        { path: '/file', component: './File' },
      ]
    },
  ],
  npmClient: 'npm',
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
});
