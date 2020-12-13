<template>
  <div>
    <h1 class="tabTitle">Timeline</h1>
    <div class="container1">
      <!-- {{ essays }} -->
      <div class="posts" v-for="essay in essays" :key="essay.id">
        <div class="post">
          <v-card class="mx-auto" color="#26c6da" dark max-width="400">
            <v-card-title>
              <v-icon large left>
                mdi-chart-bubble
              </v-icon>
              <span class="title font-weight-light"
                >topic {{ essay.topicNum }}</span
              >
              <v-row align="center" justify="end">
                <v-icon class="mr-1">
                  mdi-square
                </v-icon>
                <span class="subheading mr-2">{{ essay.scoreSelf }}</span>
              </v-row>
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
                  <v-list-item-title>{{ essay.author }}</v-list-item-title>
                  <v-list-item-title>
                    {{ essay.postDateTime | formatDate }}</v-list-item-title
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
          <!-- <p>{{ essay.author }}</p>
          <p>{{ essay.essay }}</p>
          <p>{{ essay.postDateTime }}</p>
          <p>{{ essay.topicNum }}</p> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "@/plugins/firebase";
export default {
  data() {
    return {
      essays: []
    };
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
            console.log(doc.id, "=>", doc.data());
            this.essays.push(doc.data());
          });
        })
        .catch(err => {
          console.log("Error getting documents", err);
        });
    }
  },
  mounted() {
    this.fetchEssays();
  },
  filters: {
    formatDate: function(value) {
      let a = new Date(value.seconds * 1000);
      let year = ("0000" + a.getFullYear()).slice(-4);
      let month = ("00" + String(Number(a.getMonth()) + 1)).slice(-2);
      let date = ("00" + a.getDate()).slice(-2);
      let hour = ("00" + a.getHours()).slice(-2);
      let min = ("00" + a.getMinutes()).slice(-2);
      let sec = ("00" + a.getSeconds()).slice(-2);
      let time = year + "/" + month + "/" + date + " " + hour + ":" + min;
      return time;
    },
    formatEssay: function(value) {
      const shortEssayLength = 140;
      if (value.length <= shortEssayLength) {
        return value;
      } else {
        return value.substr(0, shortEssayLength - 1) + "...";
      }
    }
  }
};
</script>

<style scoped>
.tabTitle {
  margin: 0 auto;
  text-align: center;
}
.post {
  margin-bottom: 10px;
}
</style>
