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
        <p class="wordCount">{{ wordCount }} words</p>
      </div>
      <div>
        <v-btn @click="postEssay">Post</v-btn>
      </div>
      <!-- tweetする（checkbox） -->
      <div v-if="isValidationError">
        <v-alert type="error">Input error</v-alert>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";
import essayTopicsJson from "static/csv/essayTopics";
import essayTopicsJsonR from "static/csv/essayTopicsR";

export default {
  data() {
    return {
      //topicNum: null,
      topicNum: this.$route.path.split("post/")[1],
      topicNumOption: [],
      essay: "",
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      loginUser: [], //ログインしているユーザーの情報 from firestore
      isValidationError: false,
      essayTopics: essayTopicsJson,
      essayTopicsR: essayTopicsJsonR,
      postLink: "#"
    };
  },
  mounted() {
    this.checkAuthStatus();
    this.fetchTopicNumOption();
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
    fetchTopicNumOption() {
      // let topics = [...Array(186).keys()].slice(1); // 1~185
      let topics = essayTopicsJson.map(v => v.topicNum);
      let topicsR = essayTopicsJsonR.map(v => v.topicNum);
      this.topicNumOption = topics.concat(topicsR);
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
        // safariだとwindow.openはブロックされる模様。
        // const url =
        //   "https://twitter.com/share?text=TOEFLライティングを1つ書きました！&hashtags=essayShares";
        // window.open(url, "_blank");
        this.$router.push("/timeline");
      }
    },

    isWord(str) {
      var alphaNumericFound = false;
      for (var i = 0; i < str.length; i++) {
        var code = str.charCodeAt(i);
        if (
          (code > 47 && code < 58) || // numeric (0-9)
          (code > 64 && code < 91) || // upper alpha (A-Z)
          (code > 96 && code < 123)
        ) {
          // lower alpha (a-z)
          alphaNumericFound = true;
          return alphaNumericFound;
        }
      }
      return alphaNumericFound;
    },
    hoge() {
      console.log("hoge!");
    }
  },
  computed: {
    wordCount() {
      let wordCount = 0;
      let text = this.essay.split(" ");
      for (let i = 0; i < text.length; i++) {
        if (text[i] !== " " && this.isWord(text[i])) {
          wordCount++;
        }
      }
      return wordCount;
    }
  }
};
</script>
<style scoped>
.wordCount {
  text-align: right;
  padding: 0px 30px 0px 0px;
  margin: -20px 0px 0px 0px;
}
</style>
