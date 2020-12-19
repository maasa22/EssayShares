<template>
  <div>
    <div v-if="!isWaiting">
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
          </v-card-title>

          <v-card-text class="headline font-weight-bold">
            "{{ essay.essay }}"
          </v-card-text>

          <v-card-actions>
            <v-list-item class="grow">
              <v-list-item-content>
                <nuxt-link :to="{ path: '/user/' + essay.author }">
                  <v-list-item-title>{{ essay.displayName }}</v-list-item-title>
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
</template>

<script>
import firebase from "@/plugins/firebase";
import utils from "@/plugins/utils";

export default {
  mixins: [utils],
  data() {
    return {
      isWaiting: true,
      essayId: this.$route.path.split("essay/")[1],
      essay: {}
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
            this.isWaiting = false;
          }
        })
        .catch(err => {
          console.log("Error getting document", err);
        });
    }
  }
};
</script>
