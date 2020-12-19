<template>
  <div class="googleLogin">
    <div class="buttonLogin">
      <v-btn x-large @click="googleLogin"
        >Sign in with Google account <br />Or Sign up</v-btn
      >
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

a {
  text-decoration: none;
}

.buttonLogin {
  margin: 20px;
}
</style>
