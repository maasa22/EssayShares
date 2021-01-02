<template>
  <div>
    <div v-if="!isWaiting">
      <h1 class="tabTitle">Topic {{ topicNum }}</h1>
      <!-- <p>{{ essayTitle }}</p> -->
      <p>{{ topic }}</p>

      <!-- hoge -->
      <div v-if="isEditingEssay">
        <v-textarea v-model="essay.essay" label="essay"></v-textarea>
        <v-btn text @click="updateEssay">
          Update
        </v-btn>
        <v-btn text class="cancel_btn" @click="cancelEditingEssay"
          >Cancel</v-btn
        >
        <v-dialog v-model="dialogDelete" persistent max-width="290">
          <template v-slot:activator="{ on, attrs }">
            <v-btn text v-bind="attrs" v-on="on">
              Delete
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">
              Delete
            </v-card-title>
            <v-card-text
              >When you tap this button, Delete will be completed.
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="dialogDelete = false">
                Cancel
              </v-btn>
              <v-btn color="green darken-1" text @click="deleteEssay">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
      <div v-else>
        <!-- hoge -->
        <nuxt-link :to="{ path: '/essay/' + essay.essayId }">
          <v-card class="mx-auto" color="#26c6da" dark>
            <v-card-title>
              <v-icon large left>
                mdi-chart-bubble
              </v-icon>
              <nuxt-link :to="{ path: '/topic/' + essay.topicNum }">
                <span class="title font-weight-light hoge2"
                  >topic {{ essay.topicNum }}</span
                >
              </nuxt-link>
              <v-spacer></v-spacer>
              <v-icon
                large
                color="primary"
                v-if="isMyEssay"
                @click="startEditingEssay"
              >
                mdi-pencil
              </v-icon>
            </v-card-title>
            <!-- <v-card-text class="headline font-weight-bold">
            "{{ essay.essay }}"
          </v-card-text> -->
            <v-card-text
              class="headline font-weight-bold"
              style="white-space:pre-wrap;"
            >
              "{{ essay.essay }}"
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
                    {{ essay.createdAt | formatDate }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-card-actions>
          </v-card>
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";
import essayTopicsJson from "static/csv/essayTopics";
import essayTopicsJsonR from "static/csv/essayTopicsR";

export default {
  mixins: [utils],
  data() {
    return {
      isWaiting: true,
      essayId: this.$route.path.split("essay/")[1],
      essayTopics: essayTopicsJson,
      essayTopicsR: essayTopicsJsonR,
      topic: "",
      essayTitle: "",
      topicNum: null,
      essay: {},
      isMyEssay: false,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore,
      isEditingEssay: false,
      dialogDelete: false
    };
  },
  mounted() {
    this.fetchEssays();
  },
  methods: {
    fetchEssays() {
      //   this.essays = [];
      firebase
        .firestore()
        .collection("essays")
        .doc(this.essayId)
        .get()
        .then(doc => {
          if (!doc.exists) {
            console.log("No such document!");
          } else {
            // this.essay = doc.data();
            this.fetchEssayAuthors(doc);
            this.fetchTopic(doc.data().topicNum);
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
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
            let essay = doc.data();
            let displayName = doc2.data().displayName;
            essay.displayName = displayName;
            let essayId = doc.id;
            essay.essayId = essayId;
            this.essay = essay;
            this.topicNum = essay.topicNum;
            // this.essayTitle = essayTopicsJson[essay.topicNum - 1].topic;
            // this.topicNum = essayTopicsJson[essay.topicNum - 1].topicNum;
            this.isWaiting = false;
            this.checkAuthStatus();
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
          this.loginUserGoogle = userAuth;
          this.fetchUserInfo();
        } else {
          this.isLogin = false;
          this.loginUserGoogle = [];
        }
        // this.isWaiting = false;
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
            this.checkIsMyEssay();
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    checkIsMyEssay() {
      if (this.loginUser.id == this.essay.author) {
        this.isMyEssay = true;
      }
    },
    startEditingEssay() {
      this.isEditingEssay = true;
    },
    async updateEssay() {
      // console.log(this.essay.essay);
      const data = {
        essay: this.essay.essay
      };
      const res = await firebase
        .firestore()
        .collection("essays")
        .doc(this.essay.essayId)
        .set(data, { merge: true });
      this.isEditingEssay = false;
    },
    cancelEditingEssay() {
      this.isEditingEssay = false;
    },
    async deleteEssay() {
      await firebase
        .firestore()
        .collection("essays")
        .doc(this.essay.essayId)
        .delete();
      this.$router.push("/timeline");
      console.log("hoge");
    }
  }
};
</script>
