<template>

<div class="assetpage">
    <div class="header">
        <button class="back-button" @click="$router.push('/main')">
            Back
        </button> 
        <h1 class="title">Equity Eye</h1>
    </div>

    <!-- <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> -->

    <div class="asset-information">
        <div class="assets-datas">
            <p class="symbol">{{ obj.symbol }}</p>
            <p class="price">
                <span class ="currency">$</span>
                <span class ="numbers">{{ Close }}</span>
            </p>
            <p class="name" :title="obj.name">{{ truncatedName }}</p>
            <p class="name">industry:{{ obj.industry }}</p>
            <p class="name">sector: {{ obj.sector }}</p>
            <p class="name">website: {{ obj.website }}</p>
            <p class="name">style: {{ obj.style }}</p>
            <p class="name">num of employees: {{ obj.num_employees }}</p>
        </div>

        <div class="action-buttons">
            <div class="add-asset">
                <button
                  @click="toggleFavorite"
                  :class="{ 'added': isFavorite }"
                >
                  {{ isFavorite ? 'Remove' : 'Add' }}
                </button>
            </div>
            <button
              class="invest-button"
              @click="showInvestDialog('buy')"
            >
              Buy
            </button>
            <button
              class="sell-button"
              @click="showInvestDialog('sell')"
            >
              Sell
            </button>
        </div>
    </div>

    <div class="market-chart">
      <div class="tradingview-widget-container" style="height:100%;width:100%"></div>
      <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
    </div>

    <div class="stockChart">
        <CanvasJSStockChart v-if="flag" :options="options" :style="styleOptions" />
    </div>
  <div class="describe">
    <div class="news-header">
      <p class="describe-p">investment advice:</p>
    </div>
    <div class="describe-wrap" v-if="!isLoading">
      <div v-if="advice" class="advice-content">
        <div class="section" v-for="(section, index) in formattedAdvice" :key="index">
          <h3>{{ section.title }}</h3>
          <p>{{ section.content }}</p>
        </div>
      </div>
      <div v-else class="loading-placeholder">
        Loading investment advice...
      </div>
    </div>
    <div v-else class="loading-spinner">
      <div class="spinner"></div>
    </div>
  </div>
    <div class="describe">
      <div class="news-header">
        <p class="describe-p">News:</p>
        <div class="date-inputs">
          <div class="input-group">
            <label>From:</label>
            <input
              type="date"
              v-model="newsDateRange.from"
              :max="newsDateRange.to"
            >
          </div>
          <div class="input-group">
            <label>To:</label>
            <input
              type="date"
              v-model="newsDateRange.to"
              :min="newsDateRange.from"
              :max="today"
            >
          </div>
          <button
            @click="fetchNews"
            class="search-button"
            :disabled="isLoadingNews"
          >
            {{ isLoadingNews ? 'Loading...' : 'Search' }}
          </button>
        </div>
      </div>
      <div class="describe-wrap">
        <div v-if="isLoadingNews" class="loading-news">
          <div class="loading-spinner"></div>
          <span>Loading news...</span>
        </div>
        <div v-else-if="news.length" class="news-container">
          <div v-for="(item, index) in news" :key="index" class="news-item">
            <h3>{{ item.headline }}</h3>
            <p>{{ item.summary }}</p>
            <div class="news-meta">
              <span>{{ item.datetime }}</span>
              <a :href="item.url" target="_blank">Read more</a>
            </div>
          </div>
        </div>
        <div v-else class="no-news">
          No news available for the selected date range
        </div>
      </div>
    </div>
    <!-- 添加投资弹窗 -->
    <div class="invest-dialog" v-if="showDialog">
      <div class="dialog-content">
        <h3>{{ dialogAction === 'buy' ? 'Purchase' : 'Sell' }} {{ obj.symbol }}</h3>
        <p>Current Price: ${{ Close }}</p>
        <div class="input-group">
          <label>Quantity:</label>
          <input
            type="number"
            v-model="purchaseQuantity"
            min="1"
            @input="calculateTotal"
          >
        </div>
        <div class="total">
          Total: ${{ (purchaseQuantity * Close).toFixed(2) }}
        </div>
        <div class="dialog-buttons">
          <button @click="confirmTransaction">Confirm</button>
          <button class="cancel" @click="showDialog = false">Cancel</button>
        </div>
      </div>
    </div>
</div>
</template>

<script>
  // import {loadFiles} from "../utils";
  import axios from 'axios';
  import { useAuthStore } from '../stores/auth'

  export default {
    setup() {
      const authStore = useAuthStore()
      return { authStore }  // 返回 authStore 以便在组件中使用
    },
    data() {
      return {
        Close: "",
        chart: null,
        flag: false,
        obj: JSON.parse(this.$route.query.obj),
        options: {
          exportEnabled: true,
          theme: "light2",
          title: {
            // text: "Vue.js StockChart with Date-Time Axis"
          },
          subtitles: [{
            text: JSON.parse(this.$route.query.obj).symbol   //直接取文件名
          }],
          charts: [{
            axisY: {
              title: "Price",
              prefix: "$",
              tickLength: 0
            },
            data: [{
              type: "candlestick",
              name: "Price (in USD)",
              yValueFormatString: "$#,###.##",
              dataPoints: ""
            }]
          }],
          navigator: {
            data: [{
              dataPoints: ""
            }],
            slider: {
              minimum: new Date(2020, 1, 1),
              maximum: new Date(2020, 11, 1)
            }
          }
        },
        styleOptions: {
          width: "100%",
          height: "460px"
        },
        isFavorite: false,
        showDialog: false,
        purchaseQuantity: 1,
        news: [],
        dialogAction: 'buy',
        newsDateRange: {
          from: '',
          to: ''
        },
        today: new Date().toISOString().split('T')[0],
        isLoadingNews: false,
        advice: null,
        isLoading: false,
        error: null
      }
    },
    mounted() {

      // 加载本地数据
      // loadFiles(JSON.parse(this.$route.query.obj).symbol).then((res)=>{
      //   var dps1 = [], dps2 = [];
      //   res.forEach(data => {
      //     dps1.push({ x: new Date(data["Date"]), y: [data["Open"], data["High"], data["Low"], data["Close"]] });
      //     dps2.push({ x: new Date(data["Date"]), y: data["Close"] });
      //     this.options.charts[0].data[0].dataPoints=dps1;
      //     this.options.navigator.data[0].dataPoints=dps2;
      //     this.flag=true;
      //   });

      // })


      // let params={
      //   filename:JSON.parse(this.$route.query.obj).symbol,
      // }
      axios.get('/api/stocksjson', {
        params: {
          filename: JSON.parse(this.$route.query.obj).symbol
        }
      })
      .then(response => {
        var res = response.data;
        // 处理响应数据
        if(res.code=="200"){
                this.Close=res.data[res.data.length-1].Close;
                var dps1 = [], dps2 = [];
                res.data.forEach(data => {
                  dps1.push({ x: new Date(data["Date"]), y: [data["Open"], data["High"], data["Low"], data["Close"]] });
                  dps2.push({ x: new Date(data["Date"]), y: data["Close"] });
                  this.options.charts[0].data[0].dataPoints=dps1;
                  this.options.navigator.data[0].dataPoints=dps2;
                  this.flag=true;
                });
        }
      })
      .catch(error => {
        console.error('There was an error!', error);
        // 处理错误情况
      });
      this.checkFavoriteStatus()

      // Initialize date range to last 7 days
      const today = new Date()
      const lastWeek = new Date(today)
      lastWeek.setDate(lastWeek.getDate() - 7)

      this.newsDateRange.to = today.toISOString().split('T')[0]
      this.newsDateRange.from = lastWeek.toISOString().split('T')[0]

      this.fetchNews()
      this.getInvestmentAdvice()//获取投资建议
    },
    methods: {
      async getInvestmentAdvice() {
        this.isLoading = true
        this.error = null
        
        try {
          const response = await axios.post('/api/investment-advice/', {
             stock_info: { 
              company_name: this.obj.name,
              stock_industry: this.obj.industry,
              stock_description: this.obj.description, 
              stock_news_summary: this.news,
              other_stock_data: this.obj, 

              // 添加其他相关股票信息
            }
          },{
            headers: this.authStore.getAuthHeaders()
          })
          
          if (response.data.success) {
            this.advice = response.data.data
          } else {
            this.error = response.data.message
          }
        } catch (error) {
          this.error = error.response?.data?.message || 'Failed to get investment advice'
        } finally {
          this.isLoading = false
        }
      },
      async checkFavoriteStatus() {
        try {
          const response = await axios.get('/api/users/favorites/', {
            headers: this.authStore.getAuthHeaders()
          })
          if (response.data.success) {
            this.isFavorite = response.data.data.some(
              stock => stock.symbol === this.obj.symbol
            )
          }
        } catch (error) {
          console.error('Error checking favorite status:', error)
        }
      },
      async toggleFavorite() {
        try {
          if (this.isFavorite) {
            // 取消收藏
            await axios.delete(`/api/users/favorites/?symbol=${this.obj.symbol}`, {
              headers: this.authStore.getAuthHeaders()
            })
            this.isFavorite = false
          } else {
            // 添加收藏
            await axios.post('/api/users/favorites/', {
              symbol: this.obj.symbol,
              name: this.obj.name
            }, {
              headers: this.authStore.getAuthHeaders()
            })
            this.isFavorite = true
          }
        } catch (error) {
          console.error('Error toggling favorite:', error)
        }
      },
      showInvestDialog(action) {
        this.dialogAction = action;
        this.showDialog = true;
        this.purchaseQuantity = 1;
      },

      calculateTotal() {
        if (this.purchaseQuantity < 1) {
          this.purchaseQuantity = 1;
        }
      },

      async confirmTransaction() {
        try {
          // 参数验证
          if (!this.obj.symbol) {
            alert('Invalid symbol');
            return;
          }

          if (!this.purchaseQuantity || this.purchaseQuantity <= 0) {
            alert('Please enter a valid quantity');
            return;
          }

          if (!this.Close || isNaN(this.Close)) {
            alert('Invalid price. Please try again later');
            return;
          }

          // 确保数字格式正确
          const quantity = parseInt(this.purchaseQuantity);
          const price = Number(this.Close);
          const total = quantity * price;

          // 再次验证计算结果
          if (isNaN(total) || total <= 0) {
            alert('Invalid total amount. Please check your inputs');
            return;
          }

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
            this.$router.push('/main');
          }
        } catch (error) {
          console.error('Error processing transaction:', error);
          if (error.response?.data?.message) {
            alert(error.response.data.message);
          } else {
            alert(`Failed to ${this.dialogAction}. Please check your inputs and try again.`);
          }
        }
      },
      async fetchNews() {
        this.isLoadingNews = true;
        try {
          const response = await axios.get('/api/company-news', {
            params: {
              symbol: this.obj.symbol,
              from_date: this.newsDateRange.from,
              to_date: this.newsDateRange.to
            }
          })
          if (response.data.code === 200) {
            this.news = response.data.data
          }
        } catch (error) {
          console.error('Error fetching news:', error)
        } finally {
          this.isLoadingNews = false;
        }
      }
    },
    computed: {
      truncatedName() {
        return this.obj.name.length > 20 ? this.obj.name.slice(0, 20) + '...' : this.obj.name
      },formattedAdvice() {
      if (!this.advice) return []
      
        // 将建议文本分割成不同部分
        const sections = this.advice.split('\n\n')
        return sections.map(section => {
          const [title, ...content] = section.split('\n')
          return {
            title: title.replace(/^\d+\.\s*/, ''),
            content: content.join('\n')
          }
        })
      }
    }
  }
</script>
<style>
.assetpage {
  width:1200px;
  margin:0 auto;
}
p {
    font-family: Roboto, Arial;
}

.asset-information{
    display:block;
    /* width: 700px; */
    /* margin-left: 35%; */
    padding:20px 60px;

}

.assets-datas{
    display: inline-block;
    width: 700px;
}
.add-asset{
    /* right: 0;  */
    /* margin-right: 10px; */
    float: right;
}

.title{
    text-align: center;

}
.price{
    margin-bottom: 0.1em;
}

.currency{
    display: inline-block;
}

.numbers{
    display: inline-block;
    font-size: 1.5em;
    font-weight: bold;
}
.symbol{
    display: inline-block;
}
.name {
  margin-top: 0.1em;
  margin-bottom: 0.1em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: help;
}

.change{
    display: inline-block;
    margin-top: 0.1em;
}
.stockChart {
  margin-top:20px;
}

.describe {
  width:100%;
  margin-top:40px;
}
 
.describe-wrap {
  display: block;
  min-height: 300px;
  background: #ddd;
  padding: 20px;
  border-radius: 20px;
}

.add-asset button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-asset button.added {
  background-color: #f44336;
}

.add-asset button:hover {
  opacity: 0.9;
}

.action-buttons {
  display: flex;
  gap: 10px;
  float: right;
}

.invest-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #2196F3;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.invest-button:hover {
  opacity: 0.9;
}

.invest-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
}

.input-group {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.total {
  font-size: 1.2em;
  font-weight: bold;
  margin: 15px 0;
}

.dialog-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.dialog-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.dialog-buttons button:first-child {
  background-color: #4CAF50;
  color: white;
}

.dialog-buttons button.cancel {
  background-color: #f44336;
  color: white;
}

.header {
    position: relative;
    text-align: center;
    margin-bottom: 20px;
}

.back-button {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background-color: #666;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.back-button:hover {
    background-color: #555;
}

.news-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.news-item {
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.news-item h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  color: #666;
  font-size: 0.9em;
}

.news-meta a {
  color: #2196F3;
  text-decoration: none;
}

.news-meta a:hover {
  text-decoration: underline;
}

.no-news {
  text-align: center;
  color: #666;
  padding: 20px;
}

.sell-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #f44336;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sell-button:hover {
  opacity: 0.9;
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.date-inputs {
  display: flex;
  gap: 15px;
  align-items: center;
}

.date-inputs .input-group {
  display: flex;
  align-items: center;
  flex-direction: row;
  gap: 8px;
}

.date-inputs input[type="date"] {
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button {
  padding: 8px 16px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.search-button:hover {
  opacity: 0.9;
}

.search-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-news {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


.advice-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.section:last-child {
  border-bottom: none;
}

.section h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.1em;
}

.section p {
  color: #666;
  line-height: 1.6;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #b58d7b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #dc3545;
  padding: 10px;
  text-align: center;
}

.loading-placeholder {
  text-align: center;
  color: #666;
  padding: 20px;
}
</style>
