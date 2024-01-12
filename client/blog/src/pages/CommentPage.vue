<template>
  <div>
    <NavbarComponent />
    <div>
      <div class="commentForm">
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
            <div class="likePost">
              <p>Do you like this post?</p>
              <div @click="toggleLike" class="heart-container" title="Like">
                <input type="checkbox" class="checkbox" id="Give-It-An-Id" />
                <div class="svg-container">
                  <svg
                    viewBox="0 0 24 24"
                    class="svg-outline"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
                    ></path>
                  </svg>
                  <svg
                    viewBox="0 0 24 24"
                    class="svg-filled"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"
                    ></path>
                  </svg>
                  <svg
                    class="svg-celebrate"
                    width="100"
                    height="100"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <polygon points="10,10 20,20"></polygon>
                    <polygon points="10,50 20,50"></polygon>
                    <polygon points="20,80 30,70"></polygon>
                    <polygon points="90,10 80,20"></polygon>
                    <polygon points="90,50 80,50"></polygon>
                    <polygon points="80,80 70,70"></polygon>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
      <div class="comments">
          <div v-if="comments.length === 0" class="createComment">
            <p>No comments yet. Come on leave a comment!</p>
          </div>
        <div class="card" v-for="comment in comments" :key="comment._id">
          <div class="textBox">
            <div class="textContent">
              <p class="h1">{{ comment.comment }}</p>
              <span class="span"></span>
            </div>
            <p class="p" v-if="comment.vote !== undefined">
              {{ comment.person }}
              {{ comment.vote ? "liked" : "disliked" }} this post
            </p>
            <p class="p" v-if="comment.vote == undefined">
              {{ comment.person }}
            </p>
            <form
              action=""
              @submit.prevent="updateComment(comment._id)"
              v-show="isClicked && comment.person === localStorageData"
            >
              <input
                v-model="updatedComment"
                type="text"
                name="updatedText"
                class="input"
                placeholder="Update your comment"
              />
              <button class="button buttonDelete">
                <p class="button-content">Send</p>
              </button>
            </form>

            <button
              v-if="comment.person === localStorageData"
              @click="handleButtonClick(comment._id)"
              class="btn"
            >
              <img src="../assets/refresh.png" alt="" class="btnImg" />
            </button>
            <form action="" @submit.prevent="deleteComment(comment._id)">
              <button v-if="comment.person === localStorageData" class="btn">
                <img src="../assets/delete.png" alt="" class="btnImg" />
              </button>
            </form>
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
      vote: "",
      updatedComment: "",
      isLiked: false,
      isClicked: false,
      localStorageData: localStorage.getItem("username") || null,
      activeCommentId: null,
    };
  },
  mounted() {
    this.getCommentData();
  },
  methods: {
    handleButtonClick(commentId) {
      this.isClicked = !this.isClicked;
      console.log("Clicked: " + this.isClicked + "CommentId: " + commentId);
      this.activeCommentId = commentId;
    },
    toggleLike() {
      this.isLiked = !this.isLiked;
      console.log("Liked: " + this.isLiked);
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
              "Access-Control-Allow-Origin": "http:/localhost:8080",
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
              "Access-Control-Allow-Origin": "http:/localhost:8080",
            },
            body: JSON.stringify({
              comment: this.comment,
              vote: this.isLiked,
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
              "Access-Control-Allow-Origin": "http:/localhost:8080",
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
              "Access-Control-Allow-Origin": "http:/localhost:8080",
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
};
</script>

<style src="../styles/comment.css" scoped></style>
