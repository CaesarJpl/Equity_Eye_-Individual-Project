<template>
    <div class="kyc-page">
      <RouterLink to="/">
        <h1>Equity <br> Eye</h1>
      </RouterLink>

      <p class="section-text">
        The following questions are about your investment experience and preferences.
      </p>

      <form class="preference-form" @submit.prevent="handleSubmit">
        <div class="question-group">
          <p>1. What level of investment risk are you comfortable with?</p>
          <label>
            <input type="radio" v-model="formData.riskLevel" value="conservative" required />
            Conservative (Low risk, focusing on capital preservation)
          </label>
          <label>
            <input type="radio" v-model="formData.riskLevel" value="moderate" />
            Moderate (Balanced risk and return)
          </label>
          <label>
            <input type="radio" v-model="formData.riskLevel" value="aggressive" />
            Aggressive (High risk, seeking higher returns)
          </label>
        </div>

        <div class="question-group">
          <p>2. How much short-term loss can you tolerate in your investment portfolio?</p>
          <label>
            <input type="radio" v-model="formData.lossTolerance" value="5%" required />
            Less than 5%
          </label>
          <label>
            <input type="radio" v-model="formData.lossTolerance" value="5-10%" />
            Between 5% and 10%
          </label>
          <label>
            <input type="radio" v-model="formData.lossTolerance" value="20%+" />
            More than 20%
          </label>
        </div>

        <div class="question-group">
          <p>3. How do you usually react to market volatility?</p>
          <label>
            <input type="radio" v-model="formData.marketReaction" value="calm" required />
            Stay calm and do not take immediate action.
          </label>
          <label>
            <input type="radio" v-model="formData.marketReaction" value="monitor" />
            Wait and monitor the situation before making decisions.
          </label>
          <label>
            <input type="radio" v-model="formData.marketReaction" value="change" />
            Tend to make immediate changes to the portfolio.
          </label>
        </div>

        <div class="question-group">
          <p>4. Which sectors do you prefer to invest in? (Select up to 5 sectors)</p>
          <label v-for="sector in sectors" :key="sector">
            <input 
              type="checkbox" 
              :value="sector"
              v-model="formData.preferredSectors"
              :disabled="formData.preferredSectors.length >= 5 && !formData.preferredSectors.includes(sector)"
            />
            {{ sector }}
          </label>
          <p v-if="formData.preferredSectors.length >= 5" class="warning-text">
            Maximum 5 sectors can be selected
          </p>
        </div>

        <div class="question-group">
          <p>5. How many years of investment experience do you have?</p>
          <label>
            <input type="radio" v-model="formData.investmentExperience" value="0-1" required />
            0-1 years
          </label>
          <label>
            <input type="radio" v-model="formData.investmentExperience" value="1-5" />
            1-5 years
          </label>
          <label>
            <input type="radio" v-model="formData.investmentExperience" value="5-10" />
            5-10 years
          </label>
          <label>
            <input type="radio" v-model="formData.investmentExperience" value="10+" />
            More than 10 years
          </label>
        </div>

        <div class="button-container">
            <button type="submit" class="finish-button">Finish</button>
            <RouterLink to="/regpersoninfo" class="back-link">Go back to last step</RouterLink>
        </div>
      </form>
    </div>
  </template>

  <script>
  import { useRegisterStore } from '../stores/register'
  import { useRouter } from 'vue-router'
  import stockData from '../../data/stock_data.json'  

  export default {
    setup() {
      const router = useRouter()
      const registerStore = useRegisterStore()
      return { router, registerStore }
    },
    data() {

      const uniqueSectors = [...new Set(stockData.map(stock => stock.sector))].filter(Boolean)

      return {
        formData: {
          riskLevel: '',
          lossTolerance: '',
          marketReaction: '',
          preferredAssets: [],
          preferredSectors: [], 
          investmentExperience: ''
        },
        sectors: uniqueSectors, 
        assets: [
          { value: 'stocks', label: 'Stocks' },
          { value: 'bonds', label: 'Bonds' },
          { value: 'mutual-funds', label: 'Mutual Funds' },
          { value: 'real-estate', label: 'Real Estate' },
          { value: 'forex', label: 'Foreign Exchange (Forex)' },
          { value: 'crypto', label: 'Cryptocurrencies' }
        ],
        isLoading: false
      }
    },
    methods: {
      async handleSubmit() {
        try {
          this.isLoading = true
          

          if (!this.formData.preferredSectors || this.formData.preferredSectors.length === 0) {
            alert('Please select at least one sector');
            return;
          }
          

          this.registerStore.setKycInfo(this.formData)
          

          const response = await this.registerStore.submitRegistration()
          
          if (response.success) {
            alert('Registration successful! Please log in with your email and password.')
            await this.router.push('/login')
          }
        } catch (error) {
          console.error('Error submitting registration:', error)
          
          if (error.response?.data?.errors) {
            const errorMessages = Object.entries(error.response.data.errors)
              .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
              .join('\n')
            alert(`Registration failed:\n${errorMessages}`)
          } else {
            alert('Registration failed. Please try again.')
          }
        } finally {
          this.isLoading = false
        }
      }
    }
  }
  </script>

  <style scoped>
  .kyc-page {
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
font-family: Inter;
font-size: 70px;
font-style: normal;
font-weight: 300;
line-height: 121.029%; /* 84.72px */
  }

  .section-text {
    display: flex;
width: 756.618px;
height: 34.159px;
flex-direction: column;
justify-content: center;
flex-shrink: 0;
color: #B76767;
text-align: center;
font-family: Inter;
font-size: 32px;
font-style: normal;
font-weight: 300;
line-height: 121.029%; /* 38.729px */
  }

  .preference-form {
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
  }

  .question-group {
    margin-bottom: 1.5rem;
  }

  .question-group p {
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  label {
    display: block;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
  }

  input[type="text"] {
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: #f0f0f0;
    margin-top: 0.5rem;
  }

  .button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
}

.finish-button {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 25px;
  border: none;
  background-color: #e0e0e0;
  color: #702525;
  cursor: pointer;
  text-align: center;
  margin-bottom: 1rem;
}

.back-link {
  font-size: 1rem;
  color: #4F41F4;
  text-decoration: none;
  font-weight: bold;
}

.back-link:hover {
  text-decoration: underline;
}
  .kyc-page a {
  text-decoration: none;
}

.warning-text {
  color: #ff4444;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
  </style>
