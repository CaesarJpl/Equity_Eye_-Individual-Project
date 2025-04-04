import { createRouter, createWebHistory } from 'vue-router'
import StartPage from '../components/StartPage.vue'
import LoginPage from '../components/LoginPage.vue'
import RegisterPage from '../components/RegisterPage.vue'
import RegPersonalinfoPage from '@/components/RegPersonalinfoPage.vue'
import KycPage from '@/components/KycPage.vue'
import MainPage from '@/components/MainPage.vue'
import AssetPage from '@/components/AssetPage.vue'
import AdminPage from '../components/AdminPage.vue'
import ForgotPasswordPage from '../components/ForgotPasswordPage.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: StartPage },      // 默认首页路由
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/regpersoninfo', component: RegPersonalinfoPage },
  { path: '/kyc', component: KycPage },
  { 
    path: '/main', 
    component: MainPage,
    meta: { requiresAuth: true }  // 添加需要认证的标记
  },
  { 
    path: '/asset', 
    component: AssetPage,
    meta: { requiresAuth: true }  // 资产页面也需要认证
  },
  { 
    path: '/admin', 
    component: AdminPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/forgot-password',
    component: ForgotPasswordPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局导航守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!authStore.user?.is_staff) {
      next('/')
      return
    }
  }
  
  // 检查该路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    if (!authStore.checkAuth()) {
      // 如果没有登录，重定向到首页
      next('/')
    } else {
      next() // 已登录，继续导航
    }
  } else {
    next() // 不需要认证的路由，直接通过
  }
})

export default router