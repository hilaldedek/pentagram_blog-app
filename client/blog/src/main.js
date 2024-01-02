import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import PostComponent from '../src/components/PostComponent.vue'
import LoginPage from '../src/pages/LoginPage';
import RegisterPage from '../src/pages/RegisterPage';

const Home = {template:'<PostComponent/>'}
const Login = {template:'<LoginPage/>'}
const Register = {template:'<RegisterPage/>'}

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
]

const router = createRouter({
  history:createWebHistory(),
  routes,
})

const app = createApp(App);

app.component('PostComponent', PostComponent);
app.component('LoginPage', LoginPage);
app.component('RegisterPage', RegisterPage);

app.use(router)

app.mount('#app');
