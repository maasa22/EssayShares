<template>
  <div>
    <h1 class="tabTitle">Profile</h1>
    <div v-if="isWaiting">
      <p>読み込み中</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <!-- <button @click="googleLogin">Googleでログイン</button> -->
        <GoogleLogin />
      </div>
      <div v-else>
        <div>
          <v-btn @click="logOut">ログアウト</v-btn>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import firebase from "@/plugins/firebase";

export default {
  data() {
    return {
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [] //ログインしているユーザーの情報 from google
    };
  },
  mounted: function() {
    this.checkAuthStatus();
  },
  methods: {
    checkAuthStatus() {
      firebase.auth().onAuthStateChanged(userAuth => {
        this.isWaiting = false;
        if (userAuth) {
          this.isLogin = true;
          this.loginUserGoogle = userAuth;
          this.fetchUserInfo();
        } else {
          this.isLogin = false;
          this.loginUserGoogle = [];
        }
      });
    },
    fetchUserInfo() {
      console.log(this.loginUserGoogle.email);
      let loginUser = firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
            //if a user has not registered, go to register page
            console.log("No matching documents.");
            this.$router.push("/register");
          }
          snapshot.forEach(doc => {
            // ログインユーザーのID
            this.loginUser.id = doc.id;
            this.user_id = doc.id;
            this.user = doc.data();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    logOut() {
      firebase.auth().signOut();
    }
  }
};
</script>
