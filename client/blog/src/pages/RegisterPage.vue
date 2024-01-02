<template>
  <div>
    <NavbarComponent/>
    <div class="container">
      <div class="content">
        <h1 class="header">Pentagram</h1>
        <form class="content__form">
          <div class="content__inputs">
            <label>
              <input required="" type="text" />
              <span>Username</span>
            </label>
            <label>
              <input required="" type="email" />
              <span>Email</span>
            </label>
            <label>
              <input required="" type="password" />
              <span>Password</span>
            </label>
          </div>
          <button>Register</button>
        </form>
      </div>
    </div>
    <FooterComponent/>
  </div>
</template>

<script>
import NavbarComponent from "../components/NavbarComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";

export default {
  name: "RegisterPage",
  components: {
    NavbarComponent,
    FooterComponent,
  },
};
</script>

<style src="../styles/register.css" scoped></style>
