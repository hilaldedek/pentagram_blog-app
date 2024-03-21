<template>
  <div>
    <NavbarComponent />
    <div class="main">
      <div class="info">
        <h2 class="authorName">{{ username }}</h2>
        <div class="follow">
          <div>
            <h3>Followers</h3>
            <h3 class="center">{{ followers }}</h3>
          </div>
          <div>
            <h3>Follow</h3>
            <h3 class="center">{{ follow }}</h3>
          </div>
        </div>
      </div>
      <div class="followButton">
        <div
          class="tooltip-container"
          v-if="followStatus == 0"
          @click="Follow()"
        >
          <span class="text">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 95 114"
              class="svgIcon"
            >
              <rect fill="black" rx="28.5" height="57" width="57" x="19"></rect>
              <path
                fill="black"
                d="M0 109.5C0 83.2665 21.2665 62 47.5 62V62C73.7335 62 95 83.2665 95 109.5V114H0V109.5Z"
              ></path>
            </svg>
            Follow</span
          >
        </div>
        <div
          class="tooltip-container2"
          v-if="followStatus == 1"
          @click="Unfollow()"
        >
          <span class="text2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 95 114"
              class="svgIcon2"
            >
              <rect fill="black" rx="28.5" height="57" width="57" x="19"></rect>
              <path
                fill="black"
                d="M0 109.5C0 83.2665 21.2665 62 47.5 62V62C73.7335 62 95 83.2665 95 109.5V114H0V109.5Z"
              ></path>
            </svg>
            Unfollow</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "UserProfilePage",
  components: { NavbarComponent },
  data() {
    return {
      postData: null,
      follow: null,
      followers: null,
      username: "",
      followStatus: null,
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      const getToken = localStorage.getItem("access_token");
      const username = this.$route.params.username;
      fetch(`http://127.0.0.1:5000/user/${username}/follow`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${getToken}`,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          this.follow = data.followInfo[0].follow;
          this.followers = data.followInfo[0].followers;
          this.username = data.followInfo[0].username;
          this.followStatus = data.followInfo[0].followStatus;
        })
        .catch((error) => {
          console.error("Error fetching user info:", error);
        });
    },
    async Follow() {
      try {
        const username = this.$route.params.username;
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://127.0.0.1:5000/user/${username}/follow`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
              "Access-Control-Allow-Origin": "*",
            },
          }
        );
        window.location.reload();
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      } catch (error) {
        console.error("Error during creating post:", error);
      }
    },
    async Unfollow() {
      try {
        const username = this.$route.params.username;
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://127.0.0.1:5000/user/${username}/follow`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
              "Access-Control-Allow-Origin": "*",
            },
          }
        );
        window.location.reload();
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      } catch (error) {
        console.error("Error during creating post:", error);
      }
    },
  },
};
</script>

<style src="../styles/userProfile.css" scoped></style>
