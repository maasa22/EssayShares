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
        <div v-if="isEditingDisplayName">
          <v-text-field
            v-model="displayName"
            label="Display Name"
          ></v-text-field>
          <v-btn @click="updateDisplayName">
            Update
          </v-btn>
          <v-btn class="cancel_btn" @click="cancelEditingDisplayName"
            >Cancel</v-btn
          >
        </div>
        <div v-else>
          <div class="displayName">
            {{ loginUser.displayName }}
            <v-icon
              @click="startEditingDisplayName"
              middle
              color="green darken-2"
              class="edit_icon"
            >
              mdi-pencil
            </v-icon>
          </div>
        </div>
        <div v-if="isEditingToeflWritingCurrentScore">
          <!-- <v-text-field
            v-model="toeflWritingCurrentScore"
            label="TOEFL best score"
          ></v-text-field> -->
          <v-select
            v-model="toeflWritingCurrentScore"
            :items="toeflWritingCurrentScoreOption"
            label="TOEFL Writing Current Score"
          ></v-select>
          <v-btn @click="updateToeflWritingCurrentScore">
            Update
          </v-btn>
          <v-btn
            class="cancel_btn"
            @click="cancelEditingToeflWritingCurrentScore"
            >Cancel</v-btn
          >
        </div>
        <div v-else>
          <div class="toeflWritingCurrentScore">
            TOEFL writing best score:
            {{ loginUser.toeflWritingCurrentScore }}
            <v-icon
              @click="startEditingToeflWritingCurrentScore"
              middle
              color="green darken-2"
              class="edit_icon"
            >
              mdi-pencil
            </v-icon>
          </div>
        </div>
        <!-- <h2>{{ loginUser.displayName }}</h2> -->
        <!-- <p>
          toefl writing current score: {{ loginUser.toeflWritingCurrentScore }}
        </p> -->
        <div>
          <nuxt-link to="/setting/"> Setting </nuxt-link>
        </div>
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
      </div>
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
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";

export default {
  mixins: [utils],
  data() {
    return {
      showLoadMore: false,
      showEmpty: false,
      essayUnit: 10,
      isWaiting: true,
      isLogin: false,
      essays: [],
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      dialog: false,
      displayName: "",
      isEditingDisplayName: false,
      toeflWritingCurrentScore: null,
      isEditingToeflWritingCurrentScore: false,
      toeflWritingCurrentScoreOption: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        "unset"
      ]
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
            this.fetchEssays(doc.id);
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    async fetchEssays(id) {
      await firebase
        .firestore()
        .collection("essays")
        .where("author", "==", id)
        .orderBy("createdAt", "desc")
        .limit(this.essayUnit)
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
      setTimeout(() => {
        this.showLoadMore = true;
      }, 1000);
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
    loadMore() {
      this.lastCreatedAt = this.essays[this.essays.length - 1].createdAt;
      firebase
        .firestore()
        .collection("essays")
        .where("author", "==", this.loginUser.id)
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
    startEditingDisplayName() {
      this.displayName = this.loginUser.displayName;
      this.isEditingDisplayName = true;
    },
    async updateDisplayName() {
      const data = {
        displayName: this.displayName
      };
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.loginUser.displayName = this.displayName;
      this.displayName = "";
      this.isEditingDisplayName = false;
    },
    cancelEditingDisplayName() {
      this.displayName = "";
      this.isEditingDisplayName = false;
    },
    startEditingToeflWritingCurrentScore() {
      this.toeflWritingCurrentScore = this.loginUser.toeflWritingCurrentScore;
      this.isEditingToeflWritingCurrentScore = true;
    },
    async updateToeflWritingCurrentScore() {
      const data = {
        toeflWritingCurrentScore: this.toeflWritingCurrentScore
      };
      const res = await firebase
        .firestore()
        .collection("users")
        .doc(this.loginUser.id)
        .set(data, { merge: true });
      this.loginUser.toeflWritingCurrentScore = this.toeflWritingCurrentScore;
      this.toeflWritingCurrentScore = null;
      this.isEditingToeflWritingCurrentScore = false;
    },
    cancelEditingToeflWritingCurrentScore() {
      this.toeflWritingCurrentScore = null;
      this.isEditingToeflWritingCurrentScore = false;
    }
  }
};
</script>
<style scoped>
.displayName {
  font-size: 24px;
}
</style>
