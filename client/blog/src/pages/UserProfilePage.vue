<template>
  <div>
    <NavbarComponent />
    <div class="main">
      <div v-if="username" class="info">
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
          v-if="followStatus == 0 && !(username == localStorageData)"
          @click="Follow()"
        >
          <span class="text"> Follow</span>
        </div>
        <div
          class="tooltip-container"
          v-if="followStatus == 1 && !(username == localStorageData)"
          @click="Unfollow()"
        >
          <span class="text"> Unfollow</span>
        </div>
        <div class="tooltip-container" @click="userChat()">
          <span class="text">Message</span>
        </div>
      </div>
    </div>

    <div v-if="!username && localStorageData" class="messageDiv">
      <div class="userMessage">
        <div class="message">
          <p>User is not found!</p>
        </div>
      </div>
    </div>
    <div v-if="!localStorageData" class="messageDiv">
      <div class="userMessage">
        <div class="message">
          <p>Please login!</p>
        </div>
      </div>
    </div>
    <div>
      <div class="mainCard">
        <div v-if="posts">
          <div class="card" v-for="post in posts" :key="post._id">
            <span class="title">{{ post.title }}</span>
            <span class="content">{{ post.content }}</span>
            <div class="divTags">
              <div v-for="(tag, index) in post.tags" :key="index">
                <button class="buttonTags">{{ tag }}</button>
              </div>
            </div>

            <span class="date">{{ post.dateTime }}</span>
            <div class="voteSpan">
              <span class="likes">{{ post.like_counter }} likes</span>
              <span class="dislikes">{{ post.dislike_counter }} dislike</span>
            </div>

            <div class="vote" v-if="localStorageData">
              <div>
                <button
                  @click="toggleLike(post._id)"
                  class="voteBtn"
                  :class="{
                    'like-active': buttonStates[post._id] === 1,
                    'like-inactive': buttonStates[post._id] !== 1,
                  }"
                >
                  <img src="../assets/like.png" alt="" class="voteImg" />
                </button>
              </div>
              <div>
                <button
                  @click="toggleDislike(post._id)"
                  class="voteBtn"
                  :class="{
                    'dislike-active': buttonStates[post._id] === -1,
                    'dislike-inactive': buttonStates[post._id] !== -1,
                  }"
                >
                  <img src="../assets/dislike.png" alt="" class="voteImg" />
                </button>
              </div>
            </div>
            <button class="button buttonComment" @click="commentPost(post._id)">
              <p class="button-content">Comment</p>
            </button>
          </div>
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
      posts: [],
      buttonStates: {},
    };
  },
  mounted() {
    this.getUserInfo();
    this.UserPostsList();
  },
  methods: {
    userChat() {
      const username = this.$route.params.username;
      this.$router.push({
        path: `/chat/${username}`,
        params: { username: username },
      });
    },
    async UserPostsList() {
      const getToken = localStorage.getItem("access_token");
      const username = this.$route.params.username;
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/user/${username}/post`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${getToken}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        this.posts = responseData.posts;
        console.log(this.posts);
      } catch (error) {
        console.error("Error fetching user posts:", error);
      }
    },
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
          console.log("User PROFILE PAGE:", data);
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
    commentPost(post) {
      this.$router.push({ path: `/comment/${post}`, params: { postId: post } });
    },
    async toggleLike(postId) {
      this.updateButtonState(postId, this.buttonStates[postId] === 1 ? 0 : 1);
      await this.sendVote(postId, this.buttonStates[postId]);
    },
    async toggleDislike(postId) {
      this.updateButtonState(postId, this.buttonStates[postId] === -1 ? 0 : -1);
      await this.sendVote(postId, this.buttonStates[postId]);
    },
    updateButtonState(postId, newState) {
      this.$set(this.buttonStates, postId, newState);
    },
    async sendVote(postId, vote) {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://127.0.0.1:5000/post/${postId}/vote`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            vote: vote,
          }),
        }
      );
      window.location.reload();
      if (!response.ok) {
        console.error(`HTTP error! Status: ${response.status}`);
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

<style src="../styles/userProfile.css" scoped></style>
