import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'  // 导入配置好的路由
import CanvasJSStockChart from '@canvasjs/vue-stockcharts'
import RegisterPage from './components/RegisterPage.vue'
import RegPersonalinfoPage from './components/RegPersonalinfoPage.vue'
import KycPage from './components/KycPage.vue'
import MainPage from './components/MainPage.vue'

//createApp(App).use(router).mount('#app')

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(CanvasJSStockChart)
app.use(router)

// const router = createRouter({
//   history: createWebHistory(),
//   routes: [
//     {
//       path: '/',
//       redirect: '/main'
//     },
//     { path: '/register', component: RegisterPage },
//     { path: '/regpersoninfo', component: RegPersonalinfoPage },
//     { path: '/kyc', component: KycPage },
//     { path: '/main', component: MainPage },
//     // ... 其他路由
//   ]
// })

app.mount('#app')       

