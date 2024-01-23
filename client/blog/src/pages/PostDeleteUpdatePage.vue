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
          <div class="buttons">
            <button type="submit" class="update">Update</button>
          </div>
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
  components: {
    NavbarComponent,
    FooterComponent,
  },
  props: ['postContent', 'postTitle'],
  mounted() {
    // Hedef sayfa yüklendiğinde props değerlerine erişebilirsiniz.
    console.log(this.postContent, this.postTitle);
  },
  data() {
    return {
      title: "",
      content: "",
    };
  },
  methods: {
    async updatePost() {
      const getToken = localStorage.getItem("access_token");
      const postId = this.$route.params.postId;
      const response = await fetch(`http://127.0.0.1:5000/post/${postId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${getToken}`,
          "Content-Type": "application/json",
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
        this.$router.push("/profile");
      }
    },
  },
};
</script>

<style src="../styles/postDeleteUpdate.css" scoped></style>
