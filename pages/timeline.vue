<template>
  <div>
    <h1 class="tabTitle">Timeline</h1>
    <div class="container1">
      <!-- {{ essays }} -->
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
                <!-- <v-row align="center" justify="end">
                <v-icon class="mr-1">
                  mdi-square
                </v-icon>
                <span class="subheading mr-2">{{ essay.scoreSelf }}</span>
              </v-row> -->
              </v-card-title>

              <v-card-text class="headline font-weight-bold">
                "{{ essay.essay | formatEssay }}"
              </v-card-text>

              <v-card-actions>
                <v-list-item class="grow">
                  <!-- <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            alt=""
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar> -->

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

                  <!-- <v-row
          align="center"
          justify="end"
        >
          <v-icon class="mr-1">
            mdi-heart
          </v-icon>
          <span class="subheading mr-2">14</span>
          <span class="mr-1">·</span>
          <v-icon class="mr-1">
            mdi-share-variant
          </v-icon>
          <span class="subheading">13</span>
        </v-row> -->
                </v-list-item>
              </v-card-actions>
            </v-card>
          </nuxt-link>
          <!-- <p>{{ essay.author }}</p>
          <p>{{ essay.essay }}</p>
          <p>{{ essay.createdAt }}</p>
          <p>{{ essay.topicNum }}</p> -->
        </div>
      </div>
      <v-btn
        class="buttonPost mx-2"
        fab
        dark
        large
        color="teal"
        @click="gotoPostPage"
      >
        <v-icon dark>
          mdi-pencil
        </v-icon>
      </v-btn>

      <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="290">
          <v-card>
            <v-card-title class="headline">
              Let's sign in with google account
            </v-card-title>
            <v-card-text
              >You have not signed in with this service. Let's sign in with
              google account in order to post your essays.</v-card-text
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="googleLogin">
                Sign in/Sign up
              </v-btn>
              <v-btn color="green darken-1" text @click="dialog = false">
                Cancel
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
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
      essays: [],
      isLogin: false,
      dialog: false
    };
  },
  mounted() {
    this.checkAuthStatus();
    this.fetchEssays();
  },
  methods: {
    fetchEssays() {
      //   this.essays = [];
      firebase
        .firestore()
        .collection("essays")
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            // console.log("hoge");
            // console.log(doc.id);
            // console.log(doc.data());
            this.fetchEssayAuthors(doc);
            // console.log(doc.id, "=>", doc.data());
            // this.essays.push(doc.data());
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    fetchEssayAuthors(doc) {
      // console.log("hoge");
      // console.log(doc.id);
      // console.log(doc.data());
      console.log(doc.data().author);
      firebase
        .firestore()
        .collection("users")
        .doc(doc.data().author)
        //.doc("hogehoge")
        .get()
        .then(doc2 => {
          if (!doc2.exists) {
            console.log("No such document!");
          } else {
            // console.log("Document data:", doc2.data());
            let essay = doc.data();
            let displayName = doc2.data().displayName;
            essay.displayName = displayName;
            let essayId = doc.id;
            essay.essayId = essayId;
            this.essays.push(essay);
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });

      // .then(snapshot => {
      //   snapshot.forEach(doc2 => {
      //     let displayName = doc2.data().displayName;
      //     let essay = doc.data();
      //     essay.displayName = displayName;
      //     console.log(essay);
      //     this.essays.push(essay);
      //   });
      // })
      // .catch(err => {
      //   console.log("Error getting documents", err);
      // });
    },
    checkAuthStatus() {
      firebase.auth().onAuthStateChanged(userAuth => {
        if (userAuth) {
          this.isLogin = true;
        } else {
          this.isLogin = false;
        }
      });
    },
    gotoPostPage() {
      if (this.isLogin == true) {
        this.$router.push("/post");
      } else {
        this.dialog = true;
        console.log("open dialogue");
      }
    },
    googleLogin() {
      this.dialog = false;
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
      this.$router.push("/post");
    }
  }
};
</script>

<style scoped>
.buttonPost {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}
</style>
