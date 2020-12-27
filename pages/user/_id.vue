<template>
  <div>
    <h1 class="tabTitle">{{ user.displayName }}</h1>
    <p>toefl score: {{ user.toeflWritingCurrentScore }}</p>
    <h2>Recent Posts</h2>
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
</template>
<script>
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";

export default {
  mixins: [utils],
  data() {
    return {
      essays: [],
      author: this.$route.path.split("user/")[1],
      user: {}
    };
  },
  mounted() {
    this.fetchEssays();
  },
  methods: {
    fetchEssays() {
      firebase
        .firestore()
        .collection("essays")
        .where("author", "==", this.author)
        .orderBy("createdAt", "desc")
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.fetchEssayAuthors(doc);
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
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
            this.essays.push(essay);
            this.user = doc2.data();
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    }
  }
};
</script>
