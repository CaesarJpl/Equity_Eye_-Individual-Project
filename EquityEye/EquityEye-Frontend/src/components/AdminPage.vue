<template>
  <div class="admin-page">
    <header class="admin-header">
      <h1>Admin Panel</h1>
      <div class="user-info">
        <span class="admin-email">{{ authStore.user?.email }}</span>
        <button @click="handleLogout" class="logout-button">Logout</button>
      </div>
    </header>

    <main class="admin-content">
      <div class="search-section">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by email or occupation..."
          @input="handleSearch"
        >
      </div>

      <div class="users-table">
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Date of Birth</th>
              <th>Occupation</th>
              <th>Annual Income</th>
              <th>Risk Level</th>
              <th>Registration Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.email }}</td>
              <td>{{ formatDate(user.date_of_birth) }}</td>
              <td>{{ user.occupation }}</td>
              <td>{{ user.annual_income }}</td>
              <td>{{ user.risk_level }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    return { router, authStore }
  },

  data() {
    return {
      users: [],
      searchQuery: ''
    }
  },

  mounted() {
    this.loadUsers()
  },

  methods: {
    async loadUsers() {
      try {
        const response = await axios.get('/api/admin/users/', {
          headers: this.authStore.getAuthHeaders(),
          params: {
            search: this.searchQuery
          }
        })
        if (response.data.success) {
          this.users = response.data.data
        }
      } catch (error) {
        console.error('Error loading users:', error)
        if (error.response?.status === 403) {
          // 如果不是管理员，重定向到首页
          this.router.push('/')
        }
      }
    },

    handleSearch: debounce(function() {
      this.loadUsers()
    }, 300),

    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },

    async handleLogout() {
      try {
        this.authStore.logout()
        await this.router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}

function debounce(fn, delay) {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn.apply(this, args), delay)
  }
}
</script>

<style scoped>
.admin-page {
  padding: 2rem;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.search-section {
  margin-bottom: 2rem;
}

.search-section input {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.users-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
}

tr:hover {
  background-color: #f9f9f9;
}

.logout-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: #f0f0f0;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background-color: #e0e0e0;
  color: #333;
}

.admin-email {
  margin-right: 1rem;
  color: #666;
}
</style> 