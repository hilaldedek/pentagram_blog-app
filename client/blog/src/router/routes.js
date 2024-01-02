import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import PostCreatePage from "../pages/PostCreatePage.vue";
import PostDeleteUpdatePage from "../pages/PostDeleteUpdatePage.vue"
import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/post", name: "PostCreate", component: PostCreatePage },
  { path: "/post/:id", name: "PostDeleteUpdate", component: PostDeleteUpdatePage }
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
