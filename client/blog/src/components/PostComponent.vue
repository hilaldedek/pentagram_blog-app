<template>
  <div>
    <div class="main">
      <div v-if="postData && postData.posts">
        <div class="card" v-for="post in postData.posts" :key="post._id">
          <span class="title">{{ post.title }}</span>
          <span class="content">{{ post.content }}</span>
          <span class="author">Written by {{ post.author }}</span>
          <span class="date">{{ formatDateTime(post.dateTime) }}</span>
          <div class="voteSpan">
            <span class="likes">{{ post.like_counter }} likes</span>
            <span class="dislikes">{{ post.dislike_counter }} dislike</span>
          </div>

          <div class="vote" v-if="localStorageData">
            <div>
              <button
                @click="toggleLike(post._id)"
                class="voteBtn"
                :class="{
                  'like-active': buttonStates[post._id] === 1,
                  'like-inactive': buttonStates[post._id] !== 1,
                }"
              >
                <img src="../assets/like.png" alt="" class="voteImg" />
              </button>
            </div>
            <div>
              <button
                @click="toggleDislike(post._id)"
                class="voteBtn"
                :class="{
                  'dislike-active': buttonStates[post._id] === -1,
                  'dislike-inactive': buttonStates[post._id] !== -1,
                }"
              >
                <img src="../assets/dislike.png" alt="" class="voteImg" />
              </button>
            </div>
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
      buttonStates: {},
    };
  },
  methods: {
    formatDateTime(dateTime) {
      const date = new Date(dateTime);
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      const hours = date.getHours();
      const minutes = date.getMinutes();

      return `${day}.${month}.${year} ${hours}:${minutes}`;
    },
    commentPost(post) {
      this.$router.push({ path: `/comment/${post}`, params: { postId: post } });
    },
    async toggleLike(postId) {
      this.updateButtonState(postId, this.buttonStates[postId] === 1 ? 0 : 1);
      await this.sendVote(postId, this.buttonStates[postId]);
    },
    async toggleDislike(postId) {
      this.updateButtonState(postId, this.buttonStates[postId] === -1 ? 0 : -1);
      await this.sendVote(postId, this.buttonStates[postId]);
    },
    updateButtonState(postId, newState) {
      this.$set(this.buttonStates, postId, newState);
    },
    async sendVote(postId, vote) {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://127.0.0.1:5000/post/${postId}/vote`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            vote: vote,
          }),
        }
      );
      window.location.reload();
      if (!response.ok) {
        console.error(`HTTP error! Status: ${response.status}`);
      }
    },
  },
  computed: {
    localStorageData() {
      return localStorage.getItem("username");
    },
  },
};
</script>

<style src="../styles/post.css" scoped></style>
