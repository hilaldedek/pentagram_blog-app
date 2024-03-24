<template>
  <div>
    <NavbarComponent />
    <div class="container">
      <div class="content">
        <h1 class="header">Pentagram</h1>
        <form class="content__form" @submit.prevent="login">
          <div class="content__inputs">
            <label>
              <input v-model="username" required="" type="text" />
              <span>Username</span>
            </label>
            <label>
              <input v-model="password" required="" type="password" />
              <span>Password</span>
            </label>
          </div>
          <button type="submit">Log In</button>
        </form>
        <div class="content__or-text">
          <span></span>
          <span>OR</span>
          <span></span>
        </div>
        <div class="regButton">
          <p>If you don't have an account</p>
          <router-link class="registerButton" to="/register"
            >Register</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  components: {
    NavbarComponent,
  },
  methods: {
    async login() {
      try {
        const response = await fetch("http://127.0.0.1:5000/user/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        if (response.ok) {
          if (localStorage.getItem("access_token")) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
          }
          localStorage.setItem(
            "access_token",
            responseData.tokens["access token"]
          );
          localStorage.setItem("username", this.username);
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error during login:", error);
      }
    },
  },
};
</script>

<style src="../styles/login.css" scoped></style>
