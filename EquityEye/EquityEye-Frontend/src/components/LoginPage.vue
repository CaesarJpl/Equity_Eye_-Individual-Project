<template>
    <div class="login-page">
      <div class="content">
        <h1>Equity<br> Eye</h1>

        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">EMAIL:</label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email"
              placeholder="Enter your email" 
              required
            />
            <span class="error" v-if="errors.email">{{ errors.email }}</span>
          </div>

          <div class="input-group">
            <label for="password">PASSWORD:</label>
            <input 
              type="password" 
              id="password" 
              v-model="formData.password"
              placeholder="Enter your password" 
              required
            />
            <span class="error" v-if="errors.password">{{ errors.password }}</span>
          </div>

          <div class="forgot-password">
            <router-link to="/forgot-password">Forgot your password?</router-link>
          </div>

          <button 
            type="submit" 
            class="login-button"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Logging in...' : 'Log in' }}
          </button>

          <div class="register-link">
            <p>Don't have an account? <RouterLink to="/register">Register</RouterLink></p>
          </div>
        </form>
      </div>
    </div>
  </template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: "LoginPage",
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    return { router, authStore }
  },
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      errors: {
        email: '',
        password: ''
      },
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.isLoading = true
        this.errors = { email: '', password: '' }

        const response = await this.authStore.login(this.formData)
        
        if (response.success) {
          await this.router.push('/main')
        }
      } catch (error) {
        console.error('Login error:', error)
        if (error.response?.data?.field === 'email') {
          this.errors.email = error.response.data.message
        } else if (error.response?.data?.field === 'password') {
          this.errors.password = error.response.data.message
        } else {
          this.errors.email = 'Login failed. Please try again.'
        }
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

  <style scoped>
.start-page {
    display: flex;
    height: 100vh;
    background-color: #f0f0f0;
    align-items: center;
    justify-content: center;
  }
  
  .content {
    width: 100vw; 
    height: 100vh; 
    max-width: 1500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    justify-content: center; /* 水平居中子元素 */
    align-items: center; /* 垂直居中子元素 */
    
  }
  h1{
    display: flex;
    width: 365.533px;
    height: 104.643px;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #000;
    text-align: center;
    font-family: Inter;
    font-size: 70px;
    font-style: normal;
    font-weight: 300;
    line-height: 121.029%; /* 84.72px */
    margin-top: 0; /* 将标题紧贴页面顶部 */

  }

  .input-group {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin-bottom: 1.5rem;
}

label {
    display: flex;
    width: 228.01px;
    height: 30.743px;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #000;
    text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    font-family: Inter;
    font-size: 20px;
    font-style: normal;
    font-weight: 300;
    line-height: 121.029%; /* 24.206px */

    } 

input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 25px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  outline: none;
}

.forgot-password {
  width: 300px;
  text-align: left;
  margin-bottom: 2rem;
}

.forgot-password a {
    display: flex;
    width: 262.169px;
    height: 23.057px;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #811919;
    font-size: 16px;
    text-decoration: none;
    font-family: Inter;
}

.login-button {
    width: 144.104px;
    height: 46.114px;
    padding: 0.75rem;
    font-size: 1rem;
    border-radius: 32px;
    border: none;
    background: #D9D9D9;
    color: #4a4a4a;
    cursor: pointer;
    margin-bottom: 1.5rem;
    flex-shrink: 0;
}

.register-link {
  font-size: 0.9rem;
  color: #4a4a4a;
}

.register-link a {
  color: #b58d7b;
  text-decoration: none;
}

.error {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.3rem;
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

  </style>