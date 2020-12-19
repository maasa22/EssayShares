<template>
  <div class="container2">
    <h1>Page not found</h1>
    <nuxt-link :to="{ path: '.././timeline' }">
      <v-btn class="buttonToTop">go to top page</v-btn>
    </nuxt-link>
  </div>
</template>
<style scoped>
.container2 {
  margin: 0 auto;
  text-align: center;
}
.buttonToTop {
  margin: 50px auto;
}
a {
  text-decoration: none;
}
</style>
