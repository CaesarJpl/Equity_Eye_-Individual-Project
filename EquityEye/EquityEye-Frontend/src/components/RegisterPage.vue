<template>
    <div class="register-page">
      <h1>Equity <br> Eye</h1>

      <form @submit.prevent="handleRegister">
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
            @input="checkPassword"
            placeholder="Enter your password"
            required
          />
          <span class="error" v-if="errors.password">{{ errors.password }}</span>
        </div>

        <div class="input-group">
          <label for="repassword">CONFIRM PASSWORD:</label>
          <input
            type="password"
            id="repassword"
            v-model="formData.repassword"
            @input="checkPassword"
            placeholder="Confirm your password"
            required
          />
          <span class="error" v-if="errors.repassword">{{ errors.repassword }}</span>
        </div>

        <div class="password-requirements">
          <p>Your password must contain at least:</p>
          <ul>
            <li :class="{ valid: passwordChecks.length }">7 characters</li>
            <li :class="{ valid: passwordChecks.hasNumber }">1 number</li>
            <li :class="{ valid: passwordChecks.hasUpper }">1 uppercase letter</li>
            <li :class="{ valid: passwordChecks.hasLower }">1 lowercase letter</li>
            <li :class="{ valid: passwordChecks.isMatch }">Passwords match</li>
          </ul>
        </div>

        <!-- <div class="terms">
          <input
            type="checkbox"
            id="terms"
            v-model="formData.acceptTerms"
            required
          />
          <label for="terms" class="terms-text">
            I accept <a href="#">terms and conditions</a>,
            <a href="#">privacy policy</a>,
            <a href="#">cookies policy</a>
          </label>
        </div> -->

        <button
          type="submit"
          class="create-account-button"
          :disabled="!isFormValid || isLoading"
        >
          {{ isLoading ? 'Loading...' : 'Next' }}
        </button>

        <div class="login-link">
          <p>Already have an account? <RouterLink to="/login">Log in</RouterLink></p>
        </div>
      </form>
    </div>
  </template>

<script>
import { useRegisterStore } from '../stores/register'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const registerStore = useRegisterStore()
    return { router, registerStore }
  },
  data() {
    return {
      formData: {
        email: '',
        password: '',
        repassword: '',
        acceptTerms: true
      },
      errors: {
        email: '',
        password: '',
        repassword: ''
      },
      passwordChecks: {
        length: false,
        hasNumber: false,
        hasUpper: false,
        hasLower: false,
        isMatch: false
      },
      isLoading: false
    }
  },
  computed: {
    isFormValid() {
      const { length, hasNumber, hasUpper, hasLower, isMatch } = this.passwordChecks
      return this.formData.email &&
             length && hasNumber && hasUpper && hasLower &&
             isMatch &&
             this.formData.acceptTerms
    }
  },
  methods: {
    checkPassword() {
      const password = this.formData.password
      this.passwordChecks = {
        length: password.length >= 7,
        hasNumber: /\d/.test(password),
        hasUpper: /[A-Z]/.test(password),
        hasLower: /[a-z]/.test(password),
        isMatch: this.formData.password === this.formData.repassword
      }

      if (this.formData.password && this.formData.repassword && !this.passwordChecks.isMatch) {
        this.errors.repassword = 'Passwords do not match'
      } else {
        this.errors.repassword = ''
      }
    },
    async handleRegister() {
      try {
        if (!this.isFormValid) return
        
        if (this.formData.password !== this.formData.repassword) {
          this.errors.repassword = 'Passwords do not match'
          return
        }

        this.isLoading = true
        this.errors = { email: '', password: '', repassword: '' }

        this.registerStore.setBasicInfo({
          email: this.formData.email,
          password: this.formData.password
        })

        await this.router.push('/regpersoninfo')
      } catch (error) {
        console.error('Registration error:', error)
        this.errors.email = 'Registration failed. Please try again.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  padding: 2rem;
}

h1 {
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
    margin-top: -20; /* 将标题紧贴页面顶部 */
}

.input-group {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin-bottom: 1.5rem;
}

label {
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 0.5rem;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 25px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  outline: none;
}

.password-requirements {
  width: 300px;
  font-size: 0.9rem;
  color: #b58d7b;
  margin-bottom: 2rem;
}

.password-requirements ul {
  padding-left: 1.5rem;
  list-style-type: circle;
}

.terms {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 2rem;
  width: 300px;
}

.terms a {
  color: #4F41F4; /* 蓝色链接颜色 */
  text-decoration: none;
  margin: 0 0.2rem;
}

.create-account-button {
  width: 300px;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 25px;
  border: none;
  background-color: #e0e0e0;
  color: #4a4a4a;
  cursor: pointer;
  margin-top: 1rem;
  margin-bottom: 2rem;
}

.login-link {
  font-size: 0.9rem;
}

.login-link a {
  color: #b58d7b;
  text-decoration: none;
}

.register-page a {
  text-decoration: none;
}

.create-account-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.3rem;
}

.password-requirements li {
  color: #999;
  position: relative;
  padding-left: 5px;
}

.password-requirements li.valid {
  color: #4CAF50;
}

.password-requirements li.valid::before {
  content: '✓';
  position: absolute;
  left: -15px;
  color: #4CAF50;
}

/* 修改链接样式，使用 RouterLink */
a {
  color: inherit;
  text-decoration: none;
}
</style>
