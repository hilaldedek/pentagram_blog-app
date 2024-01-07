<template>
  <div>
    <NavbarComponent />
    <div class="main">
      <div>
        <div v-for="post in posts" :key="post._id" class="card">
          <!-- <div class="image">
              <img src="" class="img-fluid rounded-top" alt="" />
            </div> -->
          <span class="title">{{ post.title }}</span>
          <span class="content">{{ post.content }}</span>
          <span class="author">{{ post.author }}</span>
          <span class="dateTime">{{ formatDateTime(post.dateTime) }}</span>
          <div>
            <div>
              <button @click="updatePost(post._id)" class="bookmarkBtn">
                <span class="IconContainer"> </span>
                <p class="text">Update</p>
              </button>
              <button class="bookmarkBtn">
                <span class="IconContainerDel"></span>
                <p class="text">Delete</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script>
import FooterComponent from "@/components/FooterComponent.vue";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  components: { NavbarComponent, FooterComponent },
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
            "Authorization": `Bearer ${getToken}`,
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
      this.$router.push({ path: `/post/${post}`, params: { postId: post }});

},
  },
};
</script>

<style src="../styles/profile.css" scoped></style>
