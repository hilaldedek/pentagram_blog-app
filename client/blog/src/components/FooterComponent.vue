<template>
  <div class="bottom">
    <div toggleable="lg" type="dark" class="main">
      <p>Copyright © {{ currentYear }} All Rights Reserved</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentDate: new Date(),
      currentYear: 0,
    };
  },
  created() {
    this.currentYear = this.currentDate.getFullYear();
  },
};
</script>

<style src="../styles/footer.css" scoped></style>
