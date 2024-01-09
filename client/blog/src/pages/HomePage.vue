<template>
  <div>
    <NavbarComponent />
    <PostComponent :postData="postData"/>
    <!-- <FooterComponent /> -->
  </div>
</template>

<script>
import PostComponent from "@/components/PostComponent.vue";
import NavbarComponent from "@/components/NavbarComponent.vue";
// import FooterComponent from "@/components/FooterComponent.vue";


/**
 * The HomePage component represents the main page of the application.
 *
 * This component includes a navbar (NavbarComponent), a list of posts (PostComponent), and a footer (FooterComponent).
 * Upon page load, it fetches post data from the backend and displays the list of posts.
 * Users can navigate between pages and perform page navigation actions.
 *
 * @name HomePage
 * @component
 */

export default {
  name: "HomePage",
  components: { NavbarComponent, PostComponent },
  data() {
    return {
      postData: null,
      currentPage: 1, // Add currentPage property to keep track of the current page
    };
  },
  mounted() {
    this.getData();
  },

  /**
     * Fetches post data from the backend and updates the postData property.
     *
     * @method
     * @name getData
     */

  methods: {
    
    getData() {
  // const page = this.currentPage;
  fetch('http://127.0.0.1:5000')
    .then(response => {
      if (!response.ok) {
        throw new Error('Veri alınamadı');
      }
      return response.json();
    })
    .then(data => {
      this.postData = data;
    })
    .catch(error => {
      console.error('Veri alınamadı:', error.message);
    });
},
    
}}
</script>

<style lang="scss" scoped></style>
