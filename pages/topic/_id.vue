<template>
  <div>
    <h1 class="tabTitle">Topic {{ topicNum }}</h1>
    <div>
      <p>{{ topic }}</p>
      <!-- <p>{{ essayTopics[topicNum - 1]["topic"] }}</p> -->
    </div>
    <h2>Recent Posts</h2>
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
    <v-row @click="loadMore" v-show="showLoadMore" justify="center"
      ><v-btn> Load More </v-btn></v-row
    >
    <v-row v-show="showEmpty" justify="center"
      >You've seen all the documents.
    </v-row>
  </div>
</template>

<script>
import essayTopicsJson from "static/csv/essayTopics";
import essayTopicsJsonR from "static/csv/essayTopicsR";
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";

export default {
  mixins: [utils],
  data() {
    return {
      showLoadMore: false,
      showEmpty: false,
      essayUnit: 10,
      essays: [],
      topicNum: this.$route.path.split("topic/")[1],
      essayTopics: essayTopicsJson,
      essayTopicsR: essayTopicsJsonR,
      topic: "",
      isLogin: false,
      dialog: false
    };
  },
  mounted() {
    this.checkAuthStatus();
    this.fetchEssays();
    this.fetchTopic(this.topicNum);
  },
  methods: {
    async fetchEssays() {
      //   this.essays = [];
      // console.log(parseInt(this.topicNum));
      await firebase
        .firestore()
        .collection("essays")
        .where("topicNum", "==", this.topicNum)
        .orderBy("createdAt", "desc")
        .limit(this.essayUnit)
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.fetchEssayAuthors(doc);
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
      setTimeout(() => {
        this.showLoadMore = true;
      }, 1000);
    },
    fetchEssayAuthors(doc) {
      firebase
        .firestore()
        .collection("users")
        .doc(doc.data().author)
        .get()
        .then(doc2 => {
          if (!doc2.exists) {
            console.log("No such document!");
          } else {
            let displayName = doc2.data().displayName;
            let essay = doc.data();
            let essayId = doc.id;
            essay.essayId = essayId;
            essay.displayName = displayName;
            this.essays.push(essay);
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    },
    fetchTopic(topicNum) {
      // topicが1~185かチェック。
      let result = this.essayTopics.filter(function(value) {
        return value.topicNum == topicNum;
      });
      if (result.length != 0) {
        this.topic = result[0].topic;
      }
      // topicが他かチェック。
      let resultR = this.essayTopicsR.filter(function(value) {
        return value.topicNum == topicNum;
      });
      if (resultR.length != 0) {
        this.topic = resultR[0].topic;
      }
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
    loadMore() {
      if (this.essays.length == 0) {
        this.showLoadMore = false;
        this.showEmpty = true;
      } else {
        this.lastCreatedAt = this.essays[this.essays.length - 1].createdAt;
        firebase
          .firestore()
          .collection("essays")
          .where("topicNum", "==", this.topicNum)
          .orderBy("createdAt", "desc")
          .startAfter(this.lastCreatedAt)
          .limit(this.essayUnit)
          .get()
          .then(snapshot => {
            if (snapshot.empty) {
              this.showLoadMore = false;
              this.showEmpty = true;
            }
            snapshot.forEach(doc => {
              this.fetchEssayAuthors(doc);
            });
          })
          .catch(err => {
            console.log("Error getting documents", err);
          });
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
