<template>
  <div>
    <div class="main">
      <div v-if="postData && postData.posts">
        <div class="card" v-for="post in postData.posts" :key="post._id">
          <!-- <div class="image">
        <img src="" class="img-fluid rounded-top" alt="" />
      </div> -->
          <span class="title">{{ post.title }}</span>
          <span class="content">{{ post.content }}</span>
          <span class="author">{{ post.author }}</span>
        </div>
      </div>
    </div>
    <div class="pagination">
      <router-link
        :to="{
          name: `http://localhost:8080/?page=${currentPage}`,
          query: { page: currentPage - 1 },
        }"
        tag="button"
        :disabled="currentPage === 1"
        class="prevBtn"
        @click.native="changePage('prev')"
      >
        Previous
      </router-link>
      <span>{{ currentPage }}</span>
      <router-link
        :to="{
          name: `http://localhost:8080/?page=${currentPage}`,
          query: { page: currentPage + 1 },
        }"
        tag="button"
        :disabled="currentPage === totalPages"
        class="nextBtn"
        @click.native="changePage('next')"
      >
        Next
      </router-link>
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
      currentPage: 1,
      itemsPerPage: 3,
    };
  },
  computed: {
    totalPages() {
      if (this.postData && this.postData.posts) {
        return Math.ceil(this.postData.posts.length / this.itemsPerPage);
      }
      return 0;
    },
    paginatedPosts() {
      if (this.postData && this.postData.posts) {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.postData.posts.slice(startIndex, endIndex);
      }
      return [];
    },
  },
  methods: {
    changePage(direction) {
      if (direction === "prev" && this.currentPage > 1) {
        this.currentPage--;
      } else if (direction === "next" && this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
  },
};
</script>

<style src="../styles/post.css" scoped></style>
