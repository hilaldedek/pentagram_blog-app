<template>
  <div>
    <NavbarComponent />
    <div class="container">
      <div class="content">
        <h1 class="header">Pentagram</h1>
        <form class="content__form" @submit.prevent="register">
          <div class="content__inputs">
            <label>
              <input v-model="username" required="" type="text" />
              <span>Username</span>
            </label>
            <label>
              <input v-model="email" required="" type="email" />
              <span>Email</span>
            </label>
            <label>
              <input v-model="password" required="" type="password" />
              <span>Password</span>
            </label>
          </div>
          <button>Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "../components/NavbarComponent.vue";

export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  components: {
    NavbarComponent,
  },
  methods: {
    async register() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/user/auth/register",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http:/localhost:8080",
            },
            body: JSON.stringify({
              username: this.username,
              email: this.email,
              password: this.password,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        if (response.ok) {
          this.$router.push("/login");
        }
      } catch (error) {
        console.error("Error during login:", error);
      }
    },
  },
};
</script>

<style src="../styles/register.css" scoped></style>
