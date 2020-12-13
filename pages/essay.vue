<template>
  <div>
    <h1 class="tabTitle">Essay</h1>
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
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import essayTopicsJson from "../static/csv/essayTopics";
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
.tabTitle {
  margin: 0 auto;
  text-align: center;
}

.topicNum {
  text-align: left;
  font-size: 20px;
  padding: 10px 0px 0px 10px;
}

.topic {
  font-size: 14px;
  height: 60px;
  padding: 0px 8px 0px 8px;
  overflow: hidden;
  /* white-space: nowrap; */
  text-overflow: ellipsis;
}
/* .color1 {
  background-color: #bbdefb;
} */
</style>
