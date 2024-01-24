import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue"
import UserPostsPage from "../pages/UserPostsPage.vue"
import Vue from 'vue';
import VueRouter from 'vue-router';
    
    Vue.use(VueRouter);
    
    const routes = [
        { path: '/',name:"Home", component: HomePage },
        { path: '/login',name:"Login", component: LoginPage },
        { path: '/register',name:"Register", component: RegisterPage },
        { path: '/user/post/:id',name:"UserPosts", component: UserPostsPage },
    ];
    
    const router = new VueRouter({
      routes,
    });
    
    export default router;