<template>
  <div class="navbar">
    <div class="main">
      <h1 class="header"><router-link to="/">Pentagram</router-link></h1>
      <div v-if="!localStorageData">
        <router-link to="/login" class="buttonStyle"
          >Login/Register</router-link
        >
      </div>
      <div v-if="localStorageData" class="search">
        <input
          v-model="searchInput"
          type="text"
          class="search__input"
          placeholder="Search an user"
        />
        <button @click="getUserInfo" class="search__button">
          <svg class="search__icon" aria-hidden="true" viewBox="0 0 24 24">
            <g>
              <path
                d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"
              ></path>
            </g>
          </svg>
        </button>
      </div>
      <div v-if="localStorageData" class="messageAndDropdown">
        <router-link to="/notification">
          <button  class="messageButton">
          <svg class="bell" viewBox="0 0 448 512">
            <path
              d="M224 0c-17.7 0-32 14.3-32 32V49.9C119.5 61.4 64 124.2 64 200v33.4c0 45.4-15.5 89.5-43.8 124.9L5.3 377c-5.8 7.2-6.9 17.1-2.9 25.4S14.8 416 24 416H424c9.2 0 17.6-5.3 21.6-13.6s2.9-18.2-2.9-25.4l-14.9-18.6C399.5 322.9 384 278.8 384 233.4V200c0-75.8-55.5-138.6-128-150.1V32c0-17.7-14.3-32-32-32zm0 96h8c57.4 0 104 46.6 104 104v33.4c0 47.9 13.9 94.6 39.7 134.6H72.3C98.1 328 112 281.3 112 233.4V200c0-57.4 46.6-104 104-104h8zm64 352H224 160c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7s18.7-28.3 18.7-45.3z"
            ></path>
          </svg>
          Notification
          <div class="arrow">›</div>
          <div class="dot"></div>
        </button>
        </router-link>
        
        <div v-if="localStorageData" class="paste-button">
          <button class="button">{{ localStorageData }} &nbsp; ▼</button>
          <div class="dropdown-content">
            <router-link to="/profile" id="top">Profile</router-link>
            <router-link to="/post" id="middle">Create Post</router-link>
            <button @click="logout" class="router-link-like">Logout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      searchInput: "",
    };
  },
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
              "Access-Control-Allow-Origin": "*",
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
    getUserInfo() {
      console.log(this.searchInput);
      this.$router.push({ path: `/user/${this.searchInput}` });
      window.location.reload();
    },
  },
  computed: {
    localStorageData() {
      return localStorage.getItem(`username`);
    },
  },
};
</script>

<style src="../styles/navbar.css" scoped></style>
