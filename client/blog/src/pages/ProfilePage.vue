<template>
  <div>
    <NavbarComponent />
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
          <span class="dateTime">{{ formatDateTime(post.dateTime) }}</span>
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
    };
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
        this.posts = responseData.posts;
        console.log(responseData);
      } catch (error) {
        console.error("Error fetching user posts:", error);
      }
    },
    formatDateTime(dateTime) {
      const options = {
        day: "numeric",
        month: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "numeric",
      };
      return new Date(dateTime).toLocaleString("tr-TR", options);
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
