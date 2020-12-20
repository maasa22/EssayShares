<template>
  <div>
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
        <h2>{{ loginUser.displayName }}</h2>
        <p>
          toefl writing current score: {{ loginUser.toeflWritingCurrentScore }}
        </p>
        <h2>Recent posts</h2>

        <div class="posts" v-for="essay in essays" :key="essay.id">
          <div class="post">
            <nuxt-link :to="{ path: '/essay/' + essay.essayId }">
              <v-card class="mx-auto" color="#26c6da" dark max-width="400">
                <v-card-title>
                  <v-icon large left>
                    mdi-chart-bubble
                  </v-icon>
                  <nuxt-link :to="{ path: '/topic/' + essay.topicNum }">
                    <span class="title font-weight-light hoge2"
                      >topic {{ essay.topicNum }}</span
                    >
                  </nuxt-link>
                </v-card-title>

                <v-card-text class="headline font-weight-bold">
                  "{{ essay.essay | formatEssay }}"
                </v-card-text>

                <v-card-actions>
                  <v-list-item class="grow">
                    <v-list-item-content>
                      <nuxt-link :to="{ path: '/user/' + essay.author }">
                        <v-list-item-title>{{
                          essay.displayName
                        }}</v-list-item-title>
                      </nuxt-link>
                      <v-list-item-title>
                        {{ essay.createdAt | formatDate }}</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                </v-card-actions>
              </v-card>
            </nuxt-link>
          </div>
        </div>

        <div class="containerCenter">
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
  </div>
</template>
<script>
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";

export default {
  mixins: [utils],
  data() {
    return {
      isWaiting: true,
      isLogin: false,
      essays: [],
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
    fetchEssays(id) {
      firebase
        .firestore()
        .collection("essays")
        .where("author", "==", id)
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let essay = doc.data();
            essay.displayName = this.loginUser.displayName;
            let essayId = doc.id;
            essay.essayId = essayId;
            this.essays.push(essay);
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    // fetchEssayAuthors(doc) {
    //   firebase
    //     .firestore()
    //     .collection("users")
    //     .doc(doc.data().author)
    //     .get()
    //     .then(doc2 => {
    //       if (!doc2.exists) {
    //         console.log("No such document!");
    //       } else {
    //         let essay = doc.data();
    //         let displayName = doc2.data().displayName;
    //         essay.displayName = displayName;
    //         let essayId = doc.id;
    //         essay.essayId = essayId;
    //         this.essays.push(essay);
    //         this.user = doc2.data();
    //       }
    //     })
    //     .catch(err => {
    //       console.log("Error getting document", err);
    //     });
    // },
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
            this.loginUser.id = doc.id;
            this.loginUser = doc.data();
            this.loginUser.google = this.loginUserGoogle;
            this.fetchEssays(doc.id);
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
