<template>
    <div class="personal-info-page">
        <RouterLink to="/">
            <h1>Equity <br> Eye</h1>
        </RouterLink>

      <p class="intro-text">
        To help your investment better, we would like to get some information about you.
      </p>
      <p class="section-text">
        The following questions are about your personal information.
      </p>

      <form class="info-form" @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="date-of-birth">Date of Birth:</label>
          <input 
            type="date" 
            id="date-of-birth" 
            v-model="formData.dateOfBirth"
            required
          />
        </div>

        <div class="input-group">
          <label for="occupation">Your Occupation:</label>
          <input 
            type="text" 
            id="occupation" 
            v-model="formData.occupation"
            placeholder="Your Occupation" 
            required
          />
        </div>

        <div class="input-group">
          <label for="annual-income">Your Annual Income:</label>
          <input 
            type="text" 
            id="annual-income" 
            v-model="formData.annualIncome"
            placeholder="Your Annual Income" 
            required
          />
        </div>

        <button type="submit" class="next-button">Next</button>
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
          dateOfBirth: '',
          occupation: '',
          annualIncome: ''
        }
      }
    },
    methods: {
      async handleSubmit() {
        try {
          // 存储个人信息
          this.registerStore.setPersonalInfo({
            dateOfBirth: this.formData.dateOfBirth,
            occupation: this.formData.occupation,
            annualIncome: this.formData.annualIncome
          })
          
          await this.router.push('/kyc')
        } catch (error) {
          console.error('Error saving personal info:', error)
        }
      }
    }
  }
  </script>

  <style scoped>
  .personal-info-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    font-family: Arial, sans-serif;
    color: #333;
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
    text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    font-family: Inter;
    font-size: 91.772px;
    font-style: normal;
    font-weight: 300;
    line-height: 121.029%;
  }

  .intro-text, .section-text {
    font-size: 1rem;
    text-align: center;
    margin-bottom: 1rem;
  }

  .section-text {
    color: #b58d7b;
    font-weight: bold;
  }

  .info-form {
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
  }

  .input-group {
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
  }

  label {
    display: flex;
width: 228.01px;
height: 22.965px;
flex-direction: column;
justify-content: center;
flex-shrink: 0;
color: #000;
text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
font-family: Inter;
font-size: 15px;
font-style: normal;
font-weight: 300;
line-height: 121.029%; /* 18.154px */
  }

  input[type="text"],
  input[type="date"],
  input[type="tel"] {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    border-radius: 25px;
    border: 1px solid #ccc;
    background-color: #f0f0f0;
    outline: none;
  }

  .next-button {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: bold;
    border-radius: 25px;
    border: none;
    background-color: #e0e0e0;
    color: #333;
    cursor: pointer;
    margin-top: 2rem;
    text-align: center;
  }

  .personal-info-page a {
  text-decoration: none;
}
  </style>
