import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),

  actions: {
    async login(credentials) {
      const response = await axios.post('/api/login/', {
        email: credentials.email,
        password: credentials.password
      })

      if (response.data.success) {
        this.token = response.data.token
        this.user = response.data.user
        // 存储用户信息和token
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
      }

      return response.data
    },

    logout() {
      this.user = null
      this.token = null
      // 清除所有存储的信息
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // 检查是否已登录
    checkAuth() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      if (token && user) {
        this.token = token
        this.user = JSON.parse(user)
        return true
      }
      return false
    },

    // 设置请求头的通用方法
    getAuthHeaders() {
      return {
        Authorization: `Bearer ${this.token}`
      }
    }
  }
}) 
