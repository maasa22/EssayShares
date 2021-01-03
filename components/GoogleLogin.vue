<template>
  <div class="googleLogin">
    <div class="buttonLogin">
      <v-btn x-large @click="googleLogin"
        >Sign in with Google account <br />Or Sign up</v-btn
      >
      <v-row justify="center">
        <nuxt-link to="/about/">
          <v-btn text color="primary"> About page </v-btn>
        </nuxt-link>
      </v-row>
    </div>
  </div>
</template>
<script>
import firebase from "@/plugins/firebase";
export default {
  methods: {
    googleLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
    }
  }
};
</script>
<style scoped>
.googleLogin {
  margin: 0 auto;
  text-align: center;
}

.buttonLogin {
  margin: 20px;
}
</style>
