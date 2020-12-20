<template>
  <div>
    <h1 class="tabTitle">TOEFL 185 Topics</h1>
    <v-container>
      <v-row class="grey lighten-3">
        <v-col
          cols="6"
          sm="4"
          md="4"
          lg="2"
          xl="2"
          class="color1"
          v-for="topicNum in topicNums"
          :key="topicNum.id"
        >
          <nuxt-link :to="{ path: '/topic/' + topicNum }">
            <v-card
              class="mx-auto"
              color="#26c6da"
              dark
              max-width="400"
              style="height: 140px"
            >
              <div>
                <p class="topicNum">topic {{ topicNum }}</p>
              </div>
              <div>
                <p class="topic">
                  <!-- university purpose hoge hoge hoge hoge hoge hoge hoge hoge hoge
                hoge hoge hoge -->
                  {{ essayTopics[topicNum - 1]["topic"] }}
                </p>
              </div>
            </v-card>
          </nuxt-link>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import essayTopicsJson from "static/csv/essayTopics";
export default {
  data() {
    return {
      topicNums: Array(185)
        .fill(0)
        .map((v, i) => i + 1), // [1,2,3,4,,,185], なぜか [1]*185でも上手くいく模様。
      essayTopics: essayTopicsJson
    };
  },
  mounted() {}
};
</script>
<style scoped>
.topicNum {
  text-align: left;
  font-size: 20px;
  padding: 10px 0px 0px 10px;
}

.topic {
  font-size: 14px;
  height: 60px;
  padding: 0px 8px 0px 8px;
  /* 複数行で3点リーダー */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}
</style>
