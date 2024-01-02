<template>
  <div>
    <NavbarComponent />
    <div class="container">
      <div class="content">
        <h1 class="header">Post Delete/Update</h1>
        <form class="content__form">
          <div class="content__inputs">
            <label class="title">
              <textarea required="" type="text" placeholder="Title" />
            </label>
            <label class="content">
              <textarea required="" type="text" placeholder="Content" />
            </label>
          </div>
          <div class="buttons">
            <button class="delete">Delete</button>
            <button class="update">Update</button>
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
};
</script>

<style src="../styles/postDeleteUpdate.css" scoped></style>
