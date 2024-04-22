import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import PostCreatePage from "../pages/PostCreatePage.vue";
import ProfilePage from "../pages/ProfilePage.vue";
import PostDeleteUpdatePage from "../pages/PostDeleteUpdatePage.vue";
import CommentPage from "../pages/CommentPage.vue";
import UserProfilePage from "../pages/UserProfilePage.vue";
import Vue from "vue";
import VueRouter from "vue-router";
import ChatPage from "@/pages/ChatPage.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", name: "Home", component: HomePage, props: true },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/post", name: "PostCreate", component: PostCreatePage },
  { path: "/profile", name: "Profile", component: ProfilePage },
  {
    path: "/post/:postId",
    name: "PostDeleteUpdate",
    component: PostDeleteUpdatePage,
    props: true,
  },
  {
    path: "/comment/:postId",
    name: "CommentPage",
    component: CommentPage,
  },
  {
    path: "/user/:username",
    name: "UserProfilePage",
    component: UserProfilePage,
  },
  {
    path: "/chat/:username",
    name: "ChatPage",
    component: ChatPage,
  },

];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
