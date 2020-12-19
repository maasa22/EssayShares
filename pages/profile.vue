<template>
  <div class="profile">
    <h1 class="tabTitle">Profile</h1>
    <div v-if="isWaiting">
      <p>loading...</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <GoogleLogin />
      </div>
      <div v-else>
        <!-- <p>{{ loginUser.google.email }}</p> -->
        <p>display name: {{ loginUser.displayName }}</p>
        <p>mail: {{ loginUser.mail }}</p>
        <p>
          toefl writing current score: {{ loginUser.toeflWritingCurrentScore }}
        </p>
        <div>
          <v-btn @click="logOut">Sign Out</v-btn>
        </div>
        <div>
          <v-dialog v-model="dialog" persistent max-width="290">
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-bind="attrs" v-on="on">
                Unregister
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="headline">
                Unregistration
              </v-card-title>
              <v-card-text
                >When you tap this button, unregistration will be completed.
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="dialog = false">
                  Cancel
                </v-btn>
                <v-btn color="green darken-1" text @click="unregister">
                  Unregister
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      dialog: false
    };
  },
  mounted: function() {
    this.checkAuthStatus();
  },
  methods: {
    checkAuthStatus() {
      firebase.auth().onAuthStateChanged(userAuth => {
        if (userAuth) {
          this.isLogin = true;
          this.loginUserGoogle = userAuth;
          this.fetchUserInfo();
        } else {
          this.isLogin = false;
          this.loginUserGoogle = [];
        }
        this.isWaiting = false;
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
            this.$router.push("/register");
          }
          snapshot.forEach(doc => {
            this.loginUser.id = doc.id;
            this.loginUser = doc.data();
            this.loginUser.google = this.loginUserGoogle;
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    logOut() {
      firebase.auth().signOut();
    },
    unregister() {
      firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
          }
          snapshot.forEach(doc => {
            console.log(doc.id);
            console.log(doc.data());
            firebase
              .firestore()
              .collection("users")
              .doc(doc.id)
              .delete();
            this.$router.push("/timeline");
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    }
  }
};
</script>
<style scoped>
.profile {
  margin: 0 auto;
  text-align: center;
}
</style>
