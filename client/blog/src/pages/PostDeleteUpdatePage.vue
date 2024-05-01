<template>
  <div>
    <NavbarComponent />
    <div class="container">
      <div class="content">
        <h1 class="header">Post Update</h1>
        <form class="content__form" @submit.prevent="updatePost">
          <div class="content__inputs">
            <label class="title">
              <textarea
                v-model="title"
                required=""
                type="text"
                placeholder="title"
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
          <div class="buttons">
            <button type="submit" class="update">Update</button>
          </div>
        </form>
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
              <div class="close">Close</div>
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
  components: {
    NavbarComponent,
  },
  mounted() {
    this.getData();
  },
  data() {
    return {
      title: "",
      content: "",
      tags: [],
      tagInput: "",
      postData: [],
    };
  },
  methods: {
    async updatePost() {
      const getToken = localStorage.getItem("access_token");
      console.log("update: ", this.tags);
      const postId = this.$route.params.postId;
      const response = await fetch(`http://127.0.0.1:5000/post/${postId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${getToken}`,
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
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
        this.$router.push("/profile");
      }
    },
    async getData() {
      const postId = this.$route.params.postId;
      const getToken = localStorage.getItem("access_token");
      try {
        const response = await fetch(`http://127.0.0.1:5000/post/${postId}`, {
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
        this.title = responseData.posts[0].title;
        this.content = responseData.posts[0].content;
        this.tags = responseData.posts[0].tags;
        console.log(this.tags);
      } catch (error) {
        console.error("Error fetching user posts:", error);
      }
    },
    addTag() {
      if (this.tagInput.trim() !== "") {
        this.tags.push(this.tagInput);
        this.tagInput = "";
      }
    },
    removeTag(index) {
      console.log(index);
      this.tags.splice(index, 1);
      console.log(this.tags);
    },
  },
};
</script>

<style src="../styles/postDeleteUpdate.css" scoped></style>
