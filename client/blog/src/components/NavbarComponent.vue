<template>
  <div class="navbar">
    <div class="main">
      <h1 class="header"><router-link to="/">Pentagram</router-link></h1>
      <div v-if="!localStorageData">
        <router-link to="/login" class="buttonStyle"
          >Login/Register</router-link
        >
      </div>
      <div v-if="localStorageData">
        <router-link to="/post" class="buttonStyle">Create Post</router-link>
      </div>
      <div v-if="localStorageData">
        <router-link to="/profile" class="buttonStyle">Profile</router-link>
      </div>
      <div v-if="localStorageData">
        <button @click="logout" class="buttonStyle">Logout</button>
      </div>
      <div class="userSection" v-if="localStorageData">
        <h2 class="user">{{ localStorageData }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    async postData() {
      try {
        const getToken = localStorage.getItem("access_token");
        const response = await axios.post(
          "http://127.0.0.1:5000/user/auth/logout",
          {
            token: getToken,
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http://localhost:80",
            },
          }
        );
        console.log(response);
        localStorage.removeItem("access_token");
        this.$router.push("/");
      } catch (error) {
        console.error("Error during login:", error);
      }
    },

    async logout() {
      const token = localStorage.getItem("access_token");
      try {
        const response = await fetch("http://127.0.0.1:5000/user/auth/logout", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("username");
          if (this.$route.path !== "/") {
            this.$router.push("/");
          }
          window.location.reload();
        } else {
          const data = await response.json();
          console.error("Logout error:", data);
          alert("Logout failed");
        }
      } catch (error) {
        console.error("Logout error:", error);
        alert("Logout failed");
      }
    },
  },
  computed: {
    localStorageData() {
      return localStorage.getItem("username");
    },
  },
};
</script>

<style src="../styles/navbar.css" scoped></style>
