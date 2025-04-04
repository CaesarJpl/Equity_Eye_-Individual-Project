<template>
  <div class="forgot-password-container">
    <div class="forgot-password-box">
      <h2>Reset Password</h2>
      
      <!-- 第一步：输入邮箱 -->
      <div v-if="step === 1" class="form-step">
        <p>Enter your email address to receive a verification code.</p>
        <input 
          type="email" 
          v-model="email" 
          placeholder="Email"
          class="input-field"
        >
        <div class="error-message" v-if="errors.email">
          {{ errors.email }}
        </div>
        <button 
          @click="sendVerificationCode" 
          :disabled="isLoading"
          class="submit-button"
        >
          {{ isLoading ? 'Sending...' : 'Send Code' }}
        </button>
      </div>

      <!-- 第二步：输入验证码和新密码 -->
      <div v-if="step === 2" class="form-step">
        <p>Enter the verification code sent to your email.</p>
        <input 
          type="text" 
          v-model="verificationCode" 
          placeholder="Verification Code"
          class="input-field"
        >
        <div class="error-message" v-if="errors.code">
          {{ errors.code }}
        </div>

        <input 
          type="password" 
          v-model="newPassword" 
          placeholder="New Password"
          class="input-field"
        >
        <div class="password-requirements" v-if="showPasswordRequirements">
          Password must:
          <ul>
            <li :class="{ met: hasMinLength }">Be at least 7 characters long</li>
            <li :class="{ met: hasUpperCase }">Contain at least one uppercase letter</li>
            <li :class="{ met: hasLowerCase }">Contain at least one lowercase letter</li>
            <li :class="{ met: hasNumber }">Contain at least one number</li>
          </ul>
        </div>
        <div class="error-message" v-if="errors.password">
          {{ errors.password }}
        </div>

        <input 
          type="password" 
          v-model="confirmPassword" 
          placeholder="Confirm Password"
          class="input-field"
        >
        <div class="error-message" v-if="errors.confirmPassword">
          {{ errors.confirmPassword }}
        </div>

        <button 
          @click="resetPassword" 
          :disabled="isLoading || !isPasswordValid"
          class="submit-button"
        >
          {{ isLoading ? 'Resetting...' : 'Reset Password' }}
        </button>
      </div>

      <!-- 成功提示 -->
      <div v-if="step === 3" class="success-message">
        <p>Password has been reset successfully!</p>
        <button @click="$router.push('/login')" class="submit-button">
          Back to Login
        </button>
      </div>

      <div class="back-to-login">
        <a @click="$router.push('/login')">Back to Login</a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      step: 1,
      email: '',
      verificationCode: '',
      newPassword: '',
      confirmPassword: '',
      isLoading: false,
      showPasswordRequirements: false,
      errors: {
        email: '',
        code: '',
        password: '',
        confirmPassword: ''
      }
    }
  },

  computed: {
    hasMinLength() {
      return this.newPassword.length >= 7
    },
    hasUpperCase() {
      return /[A-Z]/.test(this.newPassword)
    },
    hasLowerCase() {
      return /[a-z]/.test(this.newPassword)
    },
    hasNumber() {
      return /[0-9]/.test(this.newPassword)
    },
    isPasswordValid() {
      return this.hasMinLength && this.hasUpperCase && this.hasLowerCase && this.hasNumber
    }
  },

  watch: {
    newPassword() {
      this.showPasswordRequirements = true
      this.validatePassword()
    },
    confirmPassword() {
      this.validateConfirmPassword()
    }
  },

  methods: {
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.email) {
        this.errors.email = 'Email is required'
        return false
      }
      if (!emailRegex.test(this.email)) {
        this.errors.email = 'Please enter a valid email address'
        return false
      }
      this.errors.email = ''
      return true
    },

    validatePassword() {
      if (!this.newPassword) {
        this.errors.password = 'Password is required'
        return false
      }
      if (!this.isPasswordValid) {
        this.errors.password = 'Password does not meet requirements'
        return false
      }
      this.errors.password = ''
      return true
    },

    validateConfirmPassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.errors.confirmPassword = 'Passwords do not match'
        return false
      }
      this.errors.confirmPassword = ''
      return true
    },

    validateCode() {
      if (!this.verificationCode) {
        this.errors.code = 'Verification code is required'
        return false
      }
      if (!/^\d{6}$/.test(this.verificationCode)) {
        this.errors.code = 'Please enter a valid 6-digit code'
        return false
      }
      this.errors.code = ''
      return true
    },

    async sendVerificationCode() {
      if (!this.validateEmail()) {
        return
      }

      this.isLoading = true

      try {
        const response = await axios.post('/api/users/forgot-password/', {
          email: this.email
        })

        if (response.data.success) {
          this.step = 2
        }
      } catch (error) {
        this.errors.email = error.response?.data?.message || 'Failed to send verification code'
      } finally {
        this.isLoading = false
      }
    },

    async resetPassword() {
      if (!this.validateCode() || !this.validatePassword() || !this.validateConfirmPassword()) {
        return
      }

      this.isLoading = true

      try {
        const response = await axios.post('/api/users/reset-password/', {
          email: this.email,
          code: this.verificationCode,
          new_password: this.newPassword
        })

        if (response.data.success) {
          this.step = 3
        }
      } catch (error) {
        this.errors.code = error.response?.data?.message || 'Failed to reset password'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.forgot-password-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.form-step {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-field {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-button {
  background-color: #b58d7b;
  color: white;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #a07a68;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: -0.5rem;
}

.success-message {
  text-align: center;
  color: #28a745;
}

.back-to-login {
  text-align: center;
  margin-top: 1rem;
}

.back-to-login a {
  color: #666;
  text-decoration: none;
  cursor: pointer;
}

.back-to-login a:hover {
  color: #333;
}

.password-requirements {
  font-size: 0.875rem;
  color: #666;
  margin: 0.5rem 0;
}

.password-requirements ul {
  list-style: none;
  padding-left: 1rem;
  margin: 0.5rem 0;
}

.password-requirements li {
  margin: 0.25rem 0;
  color: #dc3545;
}

.password-requirements li.met {
  color: #28a745;
}

.password-requirements li::before {
  content: '•';
  margin-right: 0.5rem;
}
</style> 