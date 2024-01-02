<template>
  <div id="app">
    <navbar-component></navbar-component>
    <router-view></router-view>
    <footer-component></footer-component>
  </div>
</template>

<script>
import NavbarComponent from "./components/NavbarComponent.vue";
import FooterComponent from "./components/FooterComponent.vue";
// import PostComponent from "./components/PostComponent.vue";
// import LoginPage from "./pages/LoginPage.vue";
// import RegisterPage from "./pages/RegisterPage.vue";
// import HomePage from "../pages/HomePage.vue";

// import UserPostsPage from "../pages/UserPostsPage.vue"
export default {
  name: 'App',
  components:
    { 'navbarComponent': NavbarComponent,
      'footerComponent': FooterComponent,

      // "registerPage":RegisterPage,
      // "postComponent":PostComponent
  }
  
};
</script>

<style src="./styles/app.css" scoped>
</style>
