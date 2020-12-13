<template>
  <div>
    <h1 class="tabTitle">Essay</h1>
    <v-container>
      <v-row class="grey lighten-3">
        <v-col
          cols="3"
          sm="3"
          md="3"
          lg="2"
          xl="2"
          class="color1"
          v-for="feed in feeds"
          :key="feed.id"
        >
          <v-card
            class="mx-auto"
            color="#26c6da"
            dark
            max-width="400"
            style="height: 120px"
          >
            <div>
              <p class="topicNum">topic{{ feed }}</p>
            </div>
            <div>
              <p class="topic">
                university purpose hoge hoge hoge hoge hoge hoge hoge hoge hoge
                hoge hoge hoge
              </p>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
export default {
  data() {
    return {
      feeds: [1] * 35
    };
  }
};
</script>
<style scoped>
.tabTitle {
  margin: 0 auto;
  text-align: center;
}

.topicNum {
  text-align: left;
  font-size: 20px;
  height: 40px;
  padding: 10px;
}

.topic {
  font-size: 14px;
  height: 50px;
  padding: 10px;
  overflow: hidden;
  /* white-space: nowrap; */
  text-overflow: ellipsis;
}
/* .color1 {
  background-color: #bbdefb;
} */
</style>
