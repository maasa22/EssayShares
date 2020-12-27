<template>
  <div>
    <h1 class="tabTitle">Post your essay</h1>
    <div class="containerCenter">
      <v-select
        v-model="topicNum"
        :items="topicNumOption"
        label="topic number"
      ></v-select>
      <v-container fluid>
        <v-textarea
          v-model="essay"
          filled
          label="your essay"
          auto-grow
          value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
        ></v-textarea>
      </v-container>
      <div>
        <v-btn @click="postEssay">Post</v-btn>
      </div>
      <div v-if="isValidationError">
        <v-alert type="error">Input error</v-alert>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";

export default {
  data() {
    return {
      topicNum: null,
      topicNumOption: [...Array(186).keys()].slice(1),
      essay: "",
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      isValidationError: false
    };
  },
  mounted() {
    this.checkAuthStatus();
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
            // console.log(doc.id, "=>", doc.data());
            this.essays.push(doc.data());
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
      });
    },
    fetchUserInfo() {
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
    },
    async postEssay() {
      if (!this.topicNum || !this.essay) {
        this.isValidationError = true;
      } else {
        this.isValidationError = false;
        const data = {
          topicNum: this.topicNum.toString(),
          essay: this.essay,
          author: this.loginUser.id,
          createdAt: new Date()
        };
        const res = await firebase
          .firestore()
          .collection("essays")
          .doc(uuidv4())
          .set(data);
        this.$router.push("/timeline");
      }
    }
  }
};
</script>
