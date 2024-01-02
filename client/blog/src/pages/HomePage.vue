<template>
  <div>
    <NavbarComponent />
    <PostComponent :postData="postData"/>
    <FooterComponent />
  </div>
</template>

<script>
import PostComponent from "@/components/PostComponent.vue";
import NavbarComponent from "@/components/NavbarComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";
import axios from "axios";

export default {
  name: "HomePage",
  components: { NavbarComponent, PostComponent, FooterComponent },
  data() {
    return {
      postData: null,
      currentPage: 1, // Add currentPage property to keep track of the current page
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    
    fetchData() {
      const page = this.currentPage;
      axios.get(`http://127.0.0.1:5000/?page=${page}`)
        .then(response => {
          this.postData = response.data; // Bu, gelen veriyi postData değişkenine atar
        })
        .catch(error => {
          console.error("Veri alınamadı:", error);
        });
    },
    nextPage() {
      this.currentPage++; // Increment current page
      this.fetchData(); // Fetch data for the new page
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--; // Decrement current page, but not below 1
        this.fetchData(); // Fetch data for the new page
      }
  },
}}
</script>

<style lang="scss" scoped></style>
