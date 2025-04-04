<template>
    <div id="app">
      <!-- Header -->
      <header class="header">
        <h1>Equity Eye</h1>

      </header>
      <div class="user-info">
        <span v-if="authStore.user" class="user-email">{{ authStore.user.email }}</span>
        <button
            v-if="authStore.user"
            @click="handleLogout"
            class="logout-button"
        >
          Logout
        </button>
      </div>
      <div class="main-content">
 
        <div class="left-section">
          

          <!-- Add new Investments section -->
          <section class="investments">
            <div class="investments-header">
              <h2 class="section-title">My Investments</h2>
              <div class="total-investment">
                Total Investment: ${{ totalInvestment }}
              </div>
            </div>
            <div class="investment-grid">
              <div
                v-for="investment in investments"
                :key="investment.id"
                class="investment-card"
                @click="routerlink(investment)"
              >
                <div class="card-header">
                  <h4>{{ investment.symbol }}</h4>
                  <p class="stock-name" :title="getStockName(investment.symbol)">{{ getStockName(investment.symbol) }}</p>
                </div>
                <div class="card-info">
                  <p>Quantity: {{ investment.quantity }}</p>
                  <p>Price: ${{ investment.price }}</p>
                  <p>Total: ${{ investment.total }}</p>
                  <p class="date">{{ new Date(investment.created_at).toLocaleDateString() }}</p>
                </div>
              </div>
            </div>
            <!-- Show message if no investments -->
            <div v-if="investments.length === 0" class="no-investments">
              <p>No investments yet.</p>
              <p>Start trading to see your investments here.</p>
            </div>
          </section>

          <section class="favorites">
            <h2 class="section-title">My Favorites</h2>
            <div class="favorites-list">
              <div
                v-for="stock in favoriteStocks"
                :key="stock.symbol"
                class="favorite-item"
                @click="routerlink(stock)"
              >
                <div class="favorite-content">
                  <div class="symbol">{{ stock.symbol }}</div>
                  <div class="name" :title="stock.name">{{ stock.name }}</div>
                </div>
              </div>
            </div>
          </section>
        </div>

   
        <div class="divider"></div>


        <div class="right-section">
          <section class="financial-products">
            <div class="search-bar">
              <input type="text" v-model="searchText" placeholder="Search" @keyup.enter="searchFun"  />
              <button @click="searchFun">🔍</button>
            </div>

            <div class="selectWrap" v-if="!searchFlag">
              <select class="select" @change="selectFun" v-model="selecttext">
                <option value="">All Industries</option>
                <option 
                  v-for="(obj,index) in filteredIndustries" 
                  :key="'s'+index"
                >
                  {{obj[0].industry}}
                </option>
              </select>
            </div>

            <div class="product-categories" v-if="!searchFlag">
       
              <div v-if="selecttext" class="category-section">
                <h3 class="product-h3" v-if="stockDataSelectList[0] && stockDataSelectList[0][0]">
                  {{stockDataSelectList[0][0].industry}}:
                </h3>
                <div class="product-grid">
                  <div
                    v-for="stock in stockDataSelectList[0]"
                    :key="stock.symbol"
                    class="stock-card"
                    @click="routerlink(stock)"
                  >
                    <h4>{{ stock.symbol }}</h4>
                    <p class="stock-sector">{{ stock.sector }}</p>
                  </div>
                </div>
              </div>
    
              <div v-else class="category-section">
                <h3 class="product-h3">All Stocks:</h3>
                <div class="product-grid">
                  <div
                    v-for="stock in allStocks"
                    :key="stock.symbol"
                    class="stock-card"
                    @click="routerlink(stock)"
                  >
                    <h4>{{ stock.symbol }}</h4>
                    <p class="stock-sector">{{ stock.sector }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div v-else >
                <div class="product-ICON">
                  <span class="product-lt" @click="back"> &lt; </span>
                  <span class="product-span">NAME</span>
                  <span class="product-span">SYMBOL</span>
                  <span class="product-span">CHANGE</span>
                </div>
                <div class="product-search">
                  <p class="search-p" v-for=" (obj,index) in searchList" @click="routerlink(obj)" :key="'k'+index"  >
                    <span>{{ obj.name }}</span>
                    <span>{{ obj.growth }}</span>
                  </p>
                </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </template>

  <script>
  import stockData from '../../data/stock_data.json'
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
        searchText:"",
        searchFlag:false,
        selecttext:"",
        stockData: stockData,
        stockDataList:[],                                      
        stockDataSelectList:[],                                     
        searchList:[],                                                  
        favoriteStocks: [],
        investments: [],
        userPreferredSectors: [],
        filteredStockData: []   
      }
    },
    mounted() {
      this.loadUserProfile(); 
      this.loadFavorites();
      this.loadInvestments();
    },
    methods: {
      isPositiveChange(change) {
        return change.startsWith('+')
      },
  
      routerlink(obj) {
        this.$router.push({
            path:"/asset",
            query:{obj:JSON.stringify(obj)}
        })
      },
      searchFun() {
        let searchListarr=[];
        this.stockData.forEach((element,index)=>{
          if(element.name&& element.name.toLowerCase().indexOf(this.searchText.toLowerCase())>=0){
            searchListarr.push(element);
          }
        })
        this.searchList=searchListarr;
        this.searchFlag=true;
      },
      back() {
        this.searchFlag=false;
      },
      selectFun(data, value) {
        this.stockDataSelectList = [];
     
        if (!this.selecttext) {
          this.stockDataSelectList = this.stockDataList;
          return;
        }
    
        const selectedIndustry = this.stockDataList.find(arr => 
          arr && arr[0] && arr[0].industry === this.selecttext
        );
        if (selectedIndustry) {
          this.stockDataSelectList.push(selectedIndustry);
        }
      },
      initDate() {
       
        const stockDataListArr = [];
        const industryMap = new Map();

     
        this.filteredStockData.forEach((stock) => {
          const industry = stock.industry || 'Other';
          if (!industryMap.has(industry)) {
            industryMap.set(industry, stockDataListArr.length);
            stockDataListArr.push([]);
          }
          stockDataListArr[industryMap.get(industry)].push(stock);
        });

        this.stockDataList = stockDataListArr;
     
        this.stockDataSelectList = stockDataListArr;
      },
      async handleLogout() {
        try {
          this.authStore.logout()
          await this.router.push('/login')
        } catch (error) {
          console.error('Logout error:', error)
        }
      },
      async loadFavorites() {
        try {
          const response = await axios.get('/api/users/favorites/', {
            headers: this.authStore.getAuthHeaders()
          });
          if (response.data.success) {
            this.favoriteStocks = response.data.data;
          }
        } catch (error) {
          console.error('Error loading favorites:', error);
        }
      },
      async loadInvestments() {
        try {
          const response = await axios.get('/api/users/investments/', {
            headers: this.authStore.getAuthHeaders()
          });
          if (response.data.success) {
            this.investments = [];
            response.data.data.forEach(item => {
              const stock = this.stockData.find(s => s.symbol === item.symbol); 
              this.investments.push({
                ...item,
                ...stock
              });
            });
            //  = response.data.data;
          }
        } catch (error) {
          console.error('Error loading investments:', error);
        }
      },
      getStockName(symbol) {
        const stock = this.stockData.find(s => s.symbol === symbol);
        return stock ? stock.name : symbol;
      },
      async confirmTransaction() {
        try {
      
          const quantity = parseInt(this.purchaseQuantity);
          const price = Number(this.Close);
          const total = quantity * price;

          const response = await axios.post('/api/users/investments/', {
            symbol: this.obj.symbol,
            quantity: quantity.toString(),  
            price: price.toString(),       
            action: this.dialogAction,
            total: total.toString()       
          }, {
            headers: this.authStore.getAuthHeaders()
          });

          if (response.data.success) {
            alert(`${this.dialogAction === 'buy' ? 'Purchase' : 'Sale'} successful!`);
            this.showDialog = false;
            this.loadInvestments(); 
            this.$router.push('/main');
          }
        } catch (error) {
          console.error('Error processing transaction:', error);
          if (error.response?.data?.message) {
            alert(error.response.data.message);
          } else {
            alert(`Failed to ${this.dialogAction}. Please try again.`);
          }
        }
      },
      async loadUserProfile() {
        try {
          const response = await axios.get('/api/users/profile/', {
            headers: this.authStore.getAuthHeaders()
          });
          if (response.data.success) {
            this.userPreferredSectors = response.data.data.preferred_sectors;
        
            this.selecttext = "";
            this.filterStocksByPreference();
          }
        } catch (error) {
          console.error('Error loading user profile:', error);
        }
      },
      filterStocksByPreference() {
   
        if (!this.userPreferredSectors || this.userPreferredSectors.length === 0) {
          this.filteredStockData = this.stockData;
        } else {
     
          this.filteredStockData = this.stockData.filter(stock => 
            this.userPreferredSectors.includes(stock.sector)
          );
        }

  

        this.initDate();
        this.selectFun();
      },
    },
    computed: {
      filteredIndustries() { 
          return this.stockDataList.filter(obj => obj && obj[0] && obj[0].industry); 
      },

      allStocks() {
        return this.stockDataList.reduce((acc, group) => {
          if (group && Array.isArray(group)) {
            acc.push(...group);
          }
          return acc;
        }, []);
      },
      totalInvestment() {
        return this.investments.reduce((sum, inv) => sum + inv.total, 0).toFixed(2);
      }
    }
  }
  </script>

  <style scoped>
  #app {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    min-height: 100vh;
  }

  .header {
    width: 100%;
    max-width: 1200px; 
    margin: 0 auto;
    padding: 1rem 2rem;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .main-content {
    width: 100%;
    max-width: 1200px; 
    margin: 0 auto;
    padding: 1rem;
    box-sizing: border-box;
    display: flex;
    gap: 2rem;
  }

  .left-section,
  .right-section {
    flex: 1;
    width: 50%;
    min-width: 0;
  }

  .portfolio, .financial-products {
    width: 100%;
    padding: 1rem;
    box-sizing: border-box;
    overflow: hidden;
  }
  .product-h3 {
    text-align: left;
  }
  .portfolio-stats h2 {
    font-size: 1.5rem;
    margin: 0;
  }

  .search-bar {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }

  .search-bar input {
    flex: 1;
    padding: 0.5rem;
    margin-right: 0.5rem;
  }
  .product-card {
    border: 1px solid #ddd;
    padding: 0.5rem;
    margin-bottom: 1rem;
  }

  .positive {
    color: green;
  }

  .negative {
    color: red;
  }
  .product-search {
    border:1px solid #ddd;
    padding: 0.5rem;
    height:330px;
    border-radius: 0.5rem;
    margin-top:20px;
    overflow: hidden;
    overflow-y: scroll;
  }
  .product-ICON {
    overflow: hidden;
  }
  .product-ICON .product-lt {
    display: block;
    width:30px;
    height:30px;
    line-height: 28px;
    text-align: center;
    border-radius: 15px;
    float:left;
    color:#fff;
    background: rgb(55, 136, 209);
    cursor: pointer;
  }
  .product-span {
    display:block;
    width:90px;
    height:30px;
    float:left;
    margin-left:40px;
    line-height: 28px;
    text-align: center;
    border-radius: 15px;
    background: #ddd;
  }
  .product-ul-wrap {
    width: 100%;
    height: auto;
    overflow: visible;
  }
  .product-ul {
    display: block;
    padding: 0;
    margin: 0;
  }
  .product-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    height: 500px;
    overflow: scroll;
  }
  .stock-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 70px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .stock-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  .stock-card h4 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    font-weight: bold;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: help;
    padding: 0 5px;
  }
  .stock-price {
    margin: 4px 0;
    font-size: 0.9rem;
    color: #2196F3;
    font-weight: 500;
  }
  .stock-sector {
    margin: 4px 0;
    font-size: 0.8rem;
    color: #666;
  }
  .search-p {
    display: flex;
    justify-content:center;
    cursor: pointer;
  }
  .search-p span {
    width:200px;
  }
  .selectWrap {
    overflow: hidden;
  }
  .select {
    float:left;
  }
  @media (min-width: 1200px) {
    .header,
    .main-content {
      width: 1200px;
    }
  }
  @media (max-width: 1200px) {
    .main-content {
      flex-direction: column;
      padding: 0.5rem;
    }

    .left-section,
    .right-section {
      width: 100%;
      max-width: 100%;
    }

    .product-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  @media (max-width: 768px) {
    .product-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 480px) {
    .product-grid {
      grid-template-columns: 1fr;
    }
  }

  .user-info {
    width: 1200px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 1rem;
  }

  .user-email {
    font-size: 0.9rem;
    color: #666;
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

  .product-h3 {
    text-align: left;
    margin: 20px 0 10px;
    color: #333;
    font-size: 1.2rem;
    padding-left: 10px;
    border-left: 4px solid #b58d7b;
  }

  .category-section {
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #b58d7b;
  }

  .no-favorites {
    text-align: center;
    padding: 2rem;
    color: #666;
    background-color: #f5f5f5;
    border-radius: 8px;
    margin-top: 1rem;
  }

  .no-favorites p {
    margin: 0.5rem 0;
  }

  .no-favorites p:first-child {
    font-weight: bold;
    color: #333;
  }

  .favorites {
    padding: 1rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  /* 添加分界线样式 */
  .divider {
    width: 2px; /* 增加宽度使其更明显 */
    background-color: #e0e0e0;
    \\position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    transform: translateX(-50%);
    margin: 1rem 0;
  }

  .investments {
    margin-top: 2rem;
    padding: 1rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .investment-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    padding: 10px;
    max-height: 300px;
    overflow-y: auto;
  }

  .investment-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 150px;
    display: flex;
    flex-direction: column;
  }

  .card-header {
    margin-bottom: 10px;
  }

  .card-header h4 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: bold;
    color: #333;
  }

  .card-header .stock-name {
    margin: 5px 0;
    font-size: 0.9rem;
    color: #666;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: help;
    line-height: 1.2;
    max-height: 2.4em;
  }

  .card-info {
    border-top: 1px solid #eee;
    padding-top: 10px;
    margin-top: auto;
  }

  .card-info p {
    margin: 5px 0;
    font-size: 0.9rem;
    color: #666;
  }

  .card-info .date {
    font-size: 0.8rem;
    color: #999;
    text-align: right;
    margin-top: 8px;
  }

  .investment-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .no-investments {
    text-align: center;
    padding: 2rem;
    color: #666;
    background-color: #f5f5f5;
    border-radius: 8px;
    margin-top: 1rem;
  }

  .no-investments p {
    margin: 0.5rem 0;
  }

  .no-investments p:first-child {
    font-weight: bold;
    color: #333;
  }

  .investments-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .total-investment {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    padding: 8px 16px;
    background-color: #f8f9fa;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }

  .favorites .stock-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .favorites .stock-card h4 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    font-weight: bold;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: help;
    padding: 0 5px;
  }

  .favorites .stock-card p {
    margin: 4px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: help;
  }

  .favorites-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    height: 300px;
    overflow-y: auto;
  }

  .favorite-item {
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    height: 80px;
    overflow: hidden;
  }

  .favorite-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .favorite-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .favorite-content .symbol {
    font-weight: bold;
    color: #333;
    font-size: 1.1rem;
    margin-bottom: 5px;
  }

  .favorite-content .name {
    color: #666;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: help;
  }
  </style>
