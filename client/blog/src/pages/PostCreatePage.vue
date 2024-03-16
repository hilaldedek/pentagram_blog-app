<template>
  <div>
    <NavbarComponent />
    <div class="main">
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
                  class="titleInput"
                />
              </label>
              <label class="content">
                <textarea
                  v-model="content"
                  required=""
                  type="text"
                  placeholder="Content"
                  class="contentInput"
                />
              </label>
            </div>
            <button type="submit">Create</button>
          </form>
        </div>
      </div>
      <div>
        <form class="content__form" @submit.prevent="addTag">
          <div class="tag">
            <div class="content__inputs">
              <label class="tagInput">
                <textarea
                  v-model="tagInput"
                  required=""
                  type="text"
                  placeholder="Tags"
                  class="titleInput"
                />
              </label>
            </div>
            <button type="submit">Add</button>
          </div>
        </form>
        <ul class="ul">
          <div v-for="(tag, index) in tags" :key="index" class="tagsInput">
            <h2>{{ tag }}</h2>
            <button class="button" @click="removeTag(index)">
              <span class="X"></span>
              <span class="Y"></span>
            </button>
          </div>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "PostCreatePage",
  data() {
    return {
      title: "",
      content: "",
      tags: [],
      tagInput: "",
    };
  },
  components: {
    NavbarComponent,
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
            tags: this.tags,
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
    addTag() {
      if (this.tagInput.trim() !== "") {
        this.tags.push(this.tagInput);
        this.tagInput = "";
      }
    },
    removeTag(index) {
      this.tags.splice(index, 1);
    },
  },
};
</script>

<style src="../styles/postCreate.css" scoped></style>
