import { defineStore } from 'pinia'
import axios from 'axios'

export const useRegisterStore = defineStore('register', {
  state: () => ({
    // 第一步：基本信息
    basicInfo: {
      email: '',
      password: ''
    },
    // 第二步：个人信息
    personalInfo: {
      dateOfBirth: '',
      occupation: '',
      annualIncome: ''
    },
    // 第三步：KYC信息
    kycInfo: {
      riskLevel: '',
      lossTolerance: '',
      marketReaction: '',
      preferredAssets: [],
      investmentExperience: '',
      preferredSectors: []
    }
  }),
  
  actions: {
    setBasicInfo(info) {
      this.basicInfo = info
    },
    
    setPersonalInfo(info) {
      this.personalInfo = info
    },
    
    setKycInfo(info) {
      this.kycInfo = info
    },
    
    async submitRegistration() {
      const response = await axios.post('/api/register/', {
        email: this.basicInfo.email,
        password: this.basicInfo.password,
        date_of_birth: this.personalInfo.dateOfBirth,
        occupation: this.personalInfo.occupation,
        annual_income: this.personalInfo.annualIncome,
        risk_level: this.kycInfo.riskLevel,
        loss_tolerance: this.kycInfo.lossTolerance,
        market_reaction: this.kycInfo.marketReaction,
        preferred_sectors: this.kycInfo.preferredSectors,
        investment_experience: this.kycInfo.investmentExperience
      })
      return response.data
    }
  }
}) 
