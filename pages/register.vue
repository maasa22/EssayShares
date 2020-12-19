<template>
  <div>
    <h1 class="tabTitle">User Registration</h1>
    <div v-if="isWaiting">
      <p>loading...</p>
    </div>
    <div v-else>
      <div v-if="!isLogin">
        <GoogleLogin />
      </div>
      <div v-else>
        <v-text-field
          v-model="displayName"
          label="Display name *less than 20 characters"
          required
        ></v-text-field>
        <v-select
          v-model="toeflCurrentScore"
          :items="toeflCurrentScoreOption"
          label="TOEFL Writing Current Score"
        ></v-select>
        <!-- <p>
          If you do not have TOEFL score, set your TOEIC score here to estimate
          your TOEFL Writing score.
        </p>
         -->
        <div v-if="isValidationError">
          <v-alert type="error">Input error</v-alert>
        </div>
        <div class="buttonRegister">
          <div>
            <v-btn x-large class="mr-4" @click="registerUser">Register</v-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
import { v4 as uuidv4 } from "uuid";

// import GoogleLogin from "~/components/GoogleLogin.vue";
export default {
  //   components: {
  //     GoogleLogin
  //   },
  data() {
    return {
      isWaiting: true,
      isLogin: false,
      loginUserGoogle: [], //ログインしているユーザーの情報 from google
      displayName: "",
      toeflCurrentScore: null,
      toeflCurrentScoreOption: [
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
      ],
      isValidationError: false
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
      let loginUser = firebase
        .firestore()
        .collection("users")
        .where("mail", "==", this.loginUserGoogle.email)
        .get()
        .then(snapshot => {
          if (snapshot.empty) {
          } else {
            this.$router.push("/profile");
          }
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    },
    async registerUser() {
      if (
        !this.displayName ||
        this.displayName.length > 20 ||
        !this.toeflCurrentScore
      ) {
        this.isValidationError = true;
      } else {
        this.isValidationError = false;
        const data = {
          displayName: this.displayName,
          toeflCurrentScore: this.toeflCurrentScore,
          mail: this.loginUserGoogle.email
        };
        // Add a new document in collection "cities" with ID 'LA'
        const res = await firebase
          .firestore()
          .collection("users")
          .doc(uuidv4())
          .set(data);
        this.$router.push("/timeline");
      }
    }
  }
};
</script>
