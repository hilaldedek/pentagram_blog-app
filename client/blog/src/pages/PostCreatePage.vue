<template>
  <div>
    <NavbarComponent />
    <div class="container">
      <div class="content">
        <h1 class="header">Create Post</h1>
        <form class="content__form" @submit.prevent="createPost">
          <div class="content__inputs">
            <label class="title">
              <textarea
                v-model="title"
                required=""
                type="text"
                placeholder="Title"
              />
            </label>
            <label class="content">
              <textarea
                v-model="content"
                required=""
                type="text"
                placeholder="Content"
              />
            </label>
          </div>
          <button>Create</button>
        </form>
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";

export default {
  name: "PostCreatePage",
  data() {
    return {
      title: "",
      content: "",
    };
  },
  components: {
    NavbarComponent,
    FooterComponent,
  },
  methods: {
    async createPost() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://127.0.0.1:5000/post", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            "Access-Control-Allow-Origin": "http:/localhost:8080",
          },
          body: JSON.stringify({
            title: this.title,
            content: this.content,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        if (response.ok) {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error during creating post:", error);
      }
    },
  },
};
</script>

<style src="../styles/postCreate.css" scoped></style>
