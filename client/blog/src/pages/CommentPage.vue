<template>
  <div>
    <NavbarComponent />
    <div>
      <div v-if="getUsername" class="commentForm">
        <form action="" @submit.prevent="createComment">
          <div class="form">
            <input
              v-model="comment"
              type="text"
              name="text"
              class="input"
              placeholder="Write a comment"
            />
            <button class="button buttonDelete">
              <p class="button-content">Send</p>
            </button>
          </div>
        </form>
      </div>
      <div class="comments">
        <div v-if="comments.length === 0" class="createComment">
          <p>No comments yet. Come on leave a comment!</p>
        </div>
        <div class="mainCard">
          <h1 v-if="comments.length != 0" class="commentHeader">Comments</h1>
          <div class="card" v-for="comment in comments" :key="comment._id">
            <div v-if="comments.length > 0 && comments[0].comment != ''">
              <div class="textBox">
                <div class="textContent">
                  <p class="h1">{{ comment.comment }}</p>
                  <span class="span"></span>
                </div>
                <div class="person">
                  <img class="userImg" src="../assets/user.png" alt="" />
                  <p class="p">
                    {{ comment.person }}
                  </p>
                </div>

                <form
                  action=""
                  @submit.prevent="updateComment(comment._id)"
                  v-show="
                    comment.person === localStorageData &&
                    updateFormId === comment._id
                  "
                >
                  <input
                    v-model="updatedComment"
                    type="text"
                    name="updatedText"
                    class="input"
                    placeholder="Update your comment"
                  />
                  <button class="button buttonDelete UpdateSendButton">
                    <p class="button-content">Send</p>
                  </button>
                </form>
                <div class="buttonsDiv">
                  <button
                    v-if="comment.person === localStorageData"
                    @click="handleButtonClick(comment._id)"
                    class="btn"
                  >
                    <img src="../assets/refresh.png" alt="" class="btnImg" />
                  </button>
                  <form action="" @submit.prevent="deleteComment(comment._id)">
                    <button
                      v-if="comment.person === localStorageData"
                      class="btn"
                    >
                      <img src="../assets/delete.png" alt="" class="btnImg" />
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- <FooterComponent /> -->
  </div>
</template>

<script>
// import FooterComponent from "@/components/FooterComponent.vue";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  components: { NavbarComponent },
  props: {
    commentData: Object,
  },
  data() {
    return {
      comments: [],
      comment: "",
      updatedComment: "",
      updateFormId: "",
      localStorageData: localStorage.getItem("username") || null,
    };
  },
  mounted() {
    this.getCommentData();
  },
  methods: {
    handleButtonClick(commentId) {
      this.updateFormId = commentId;
    },
    async getCommentData() {
      try {
        const postId = this.$route.params.postId;
        const response = await fetch(
          `http://127.0.0.1:5000/comment-list/${postId}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const commentData = await response.json();
        this.comments = commentData;
      } catch (error) {
        console.error("Veri alınamadı:", error);
      }
    },
    async createComment() {
      try {
        const getToken = localStorage.getItem("access_token");
        const postId = this.$route.params.postId;
        const response = await fetch(
          `http://127.0.0.1:5000/post/${postId}/comment`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${getToken}`,
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http:/localhost:80",
            },
            body: JSON.stringify({
              comment: this.comment,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        if (response.ok) {
          window.location.reload();
        }
      } catch (error) {
        console.error("Veri alınamadı:", error);
      }
    },
    async updateComment(comment) {
      try {
        const getToken = localStorage.getItem("access_token");
        const commentId = comment;
        const response = await fetch(
          `http://127.0.0.1:5000/comment/${commentId}`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${getToken}`,
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http:/localhost:80",
            },
            body: JSON.stringify({
              comment: this.updatedComment,
            }),
          }
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        if (response.ok) {
          window.location.reload();
        }
      } catch (error) {
        console.error("Veri alınamadı:", error);
      }
    },
    async deleteComment(comment) {
      try {
        const getToken = localStorage.getItem("access_token");
        const commentId = comment;
        const response = await fetch(
          `http://127.0.0.1:5000/comment/${commentId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${getToken}`,
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http:/localhost:80",
            },
          }
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        if (response.ok) {
          window.location.reload();
        }
      } catch (error) {
        console.error("Veri alınamadı:", error);
      }
    },
  },
  computed: {
    getUsername() {
      return localStorage.getItem("username");
    },
  },
};
</script>

<style src="../styles/comment.css" scoped></style>
