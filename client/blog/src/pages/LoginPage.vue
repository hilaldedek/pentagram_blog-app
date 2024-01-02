<template>
  <div>
    <NavbarComponent/>
    <div class="container">
    <div class="content">
      <h1 class="header">Pentagram</h1>
      <form class="content__form">
        <div class="content__inputs">
          <label>
            <input required="" type="text" />
            <span>Username</span>
          </label>
          <label>
            <input required="" type="password" />
            <span>Password</span>
          </label>
        </div>
        <button>Log In</button>
      </form>
      <div class="content__or-text">
        <span></span>
        <span>OR</span>
        <span></span>
      </div>
      <div class="regButton">
        <router-link class="registerButton" to="/register" >Register</router-link>
      </div>
    </div>
  </div>
  <FooterComponent/>
  </div>
  
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";

export default {
  name: "LoginPage",
  components: {
    NavbarComponent,
    FooterComponent,
  },
};
</script>

<style src="../styles/login.css" scoped></style>
