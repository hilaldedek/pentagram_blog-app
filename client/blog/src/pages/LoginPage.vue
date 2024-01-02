<template>
    <div class="container">
        <div class="content">
          <h1 class="header">Pentagram</h1>
          <form class="content__form">
            <div class="content__inputs">
              <label>
                <input required="" type="text">
                <span>Username</span>
              </label>
              <label>
                <input required="" type="password">
                <span>Password</span>
              </label>
            </div>
            <button>Log In</button>
          </form>
          <div class="content__or-text">
            <span></span>
            <span>OR</span>
            <span></span>
          </div>
          <div >
            <button class="registerButton">Register</button>
          </div>
        </div>
      </div>
</template>

<script>
    export default {
        
    }
</script>

<style src="../styles/login.css" scoped>
</style>