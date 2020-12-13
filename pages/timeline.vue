<template>
  <div>
    <h1>Timeline</h1>
    <div class="container1">
      <!-- {{ essays }} -->
      <div class="posts" v-for="essay in essays" :key="essay.id">
        <div class="post">
          <p>{{ essay.author }}</p>
          <p>{{ essay.essay }}</p>
          <p>{{ essay.postDateTime }}</p>
          <p>{{ essay.topicNum }}</p>
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
      essays: [],
    };
  },
  methods: {
    fetchEssays() {
      //   this.essays = [];
      firebase
        .firestore()
        .collection("essays")
        .get()
        .then((snapshot) => {
          snapshot.forEach((doc) => {
            console.log(doc.id, "=>", doc.data());
            this.essays.push(doc.data());
          });
        })
        .catch((err) => {
          console.log("Error getting documents", err);
        });
    },
  },
  mounted() {
    this.fetchEssays();
  },
};
</script>

<style scoped>
</style>
