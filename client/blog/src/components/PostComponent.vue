<template>
  <div>
    <div class="main">
      <div v-if="postData && postData.posts">
        <div class="card" v-for="post in postData.posts" :key="post._id">
          <span class="title">{{ post.title }}</span>
          <span class="content">{{ post.content }}</span>
          <span class="author">Written by {{ post.author }}</span>
          <div v-for="counter in likeDislikeCommentData" :key="counter._id">
            <p>{{ counter.comment_count }} likes</p>
            <p>{{ counter.dislike_count }} dislikes</p>
            <p>{{ counter.like_count }} comment</p>
          </div>
          <button class="button buttonComment" @click="commentPost(post._id)">
            <p class="button-content">Comment</p>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    postData: Object,
  },
  data() {
    return {
      likeDislikeCommentData: [],
    };
  },
  methods: {
    commentPost(post) {
      this.$router.push({ path: `/comment/${post}`, params: { postId: post } });
    },
    async likeDislikeComment(post) {
      try {
        const postId = post;
        const response = await fetch(`http://127.0.0.1:5000/vote/${postId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http:/localhost:8080",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const LDCData = await response.json();
        this.likeDislikeCommentData = LDCData;
      } catch (error) {
        console.error("Veri alınamadı:", error);
      }
    },
  },
  mounted() {
    console.log("postData:", this.postData);
  },
};
</script>

<style src="../styles/post.css" scoped></style>
