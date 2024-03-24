<template>
  <div>
    <NavbarComponent />
    <div v-if="username" class="infoDiv">
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
    </div>
    <div class="main">
      <div v-if="posts.length === 0" class="createPost">
        <p>You don't have any posts.</p>
        <router-link to="/post" class="buttonStyle">Create Post</router-link>
      </div>
      <div>
        <div v-for="post in posts" :key="post._id" class="card">
          <span class="title">{{ post.title }}</span>
          <span class="content">{{ post.content }}</span>
          <span class="author">{{ post.author }}</span>
          <span class="dateTime">{{ post.dateTime }}</span>
          <div>
            <div class="UDButtons">
              <button @click="updatePost(post)" class="button buttonUpdate">
                <p class="button-content">Update</p>
              </button>
              <button class="button buttonDelete" @click="deletePost(post._id)">
                <p class="button-content">Delete</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  components: { NavbarComponent },
  data() {
    return {
      posts: [],
      follow: null,
      followers: null,
      username: "",
    };
  },
  mounted() {
    this.getUserInfo();
  },
  created() {
    this.fetchUserPosts();
  },
  methods: {
    async fetchUserPosts() {
      const getToken = localStorage.getItem("access_token");
      try {
        const response = await fetch("http://127.0.0.1:5000/user/post", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${getToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        this.posts = responseData;
      } catch (error) {
        console.error("Error fetching user posts:", error);
      }
    },
    getUserInfo() {
      const getToken = localStorage.getItem("access_token");
      const username = localStorage.getItem("username");
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
          console.log("RESPONSE: ", response);
          return response.json();
        })
        .then((data) => {
          console.log("PROFILE PAGE:", data);
          this.follow = data.followInfo[0].follow;
          this.followers = data.followInfo[0].followers;
          this.username = data.followInfo[0].username;
        })
        .catch((error) => {
          console.error("Error fetching user info:", error);
        });
    },
    updatePost(post) {
      this.$router.push({
        path: `/post/${post._id}`,
        props: { postContent: post.content, postTitle: post.title },
      });
    },
    async deletePost(post) {
      const getToken = localStorage.getItem("access_token");
      const postId = post;
      const response = await fetch(`http://127.0.0.1:5000/post/${postId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${getToken}`,
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      if (response.ok) {
        window.location.reload();
      }
    },
  },
};
</script>

<style src="../styles/profile.css" scoped></style>
