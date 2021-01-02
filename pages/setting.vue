<template>
  <div>
    <h1 class="tabTitle">Setting</h1>
    <div v-if="isWaiting">
      <p>loading...</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <GoogleLogin />
      </div>
      <div v-else>
        <ul>
          <li>
            <nuxt-link to="/about/">
              <v-btn text color="primary"> About page </v-btn>
            </nuxt-link>
          </li>
          <li>
            <!-- <a @click="logOut"
              ><v-btn text color="primary"> Sign Out </v-btn></a
            > -->
            <div>
              <v-dialog v-model="dialogLogOut" persistent max-width="290">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn text color="primary" v-bind="attrs" v-on="on">
                    Sign Out
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="headline">
                    Sign Out
                  </v-card-title>
                  <v-card-text
                    >When you tap this button, Sign Out will be completed.
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="green darken-1"
                      text
                      @click="dialogLogOut = false"
                    >
                      Cancel
                    </v-btn>
                    <v-btn color="green darken-1" text @click="logOut">
                      Sign Out
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>
          </li>
          <li>
            <div>
              <v-dialog v-model="dialogUnregister" persistent max-width="290">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn text color="primary" v-bind="attrs" v-on="on">
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
                    <v-btn
                      color="green darken-1"
                      text
                      @click="dialogUnregister = false"
                    >
                      Cancel
                    </v-btn>
                    <v-btn color="green darken-1" text @click="unregister">
                      Unregister
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>
          </li>
        </ul>
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
      loginUser: [], //ログインしているユーザーの情報 from firestore,
      dialogUnregister: false,
      dialogLogOut: false
    };
  },
  methods: {
    logOut() {
      console.log("hoge");
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
    },
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
      // console.log(this.loginUserGoogle.email);
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
            this.loginUser = doc.data();
            this.loginUser.id = doc.id;
            this.loginUser.google = this.loginUserGoogle;
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    }
  },
  mounted: function() {
    this.checkAuthStatus();
  }
};
</script>
