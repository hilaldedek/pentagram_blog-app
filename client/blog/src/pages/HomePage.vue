<template>
    <div>
        <NavbarComponent/>
        <PostComponent/>
        <FooterComponent/>
    </div>
</template>

<script>
import PostComponent from '@/components/PostComponent.vue';
import NavbarComponent from '@/components/NavbarComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';

    export default {
    name: "HomePage",
    components: { NavbarComponent,PostComponent,FooterComponent}
};
</script>

<style lang="scss" scoped>

</style>