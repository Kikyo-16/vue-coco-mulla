import { createApp } from 'vue'
//import App from './App.vue'

//createApp(App).mount('#app')

//import * as VueRouter from 'vue-router';
import App from './App.vue'
//import DemoPage from "@/components/DemoPage";


/*const routes = [
  { path: '/', component: App },
  { path: '/demo', component: DemoPage },
]

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes,
})*/

const app = createApp(App);
//app.use(router)
app.mount('#app');

