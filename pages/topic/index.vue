<template>
  <div>
    <h1 class="tabTitle">Recommend Topics</h1>
    <v-container>
      <v-row class="grey lighten-3">
        <v-col
          cols="6"
          sm="4"
          md="4"
          lg="2"
          xl="2"
          class="color1"
          v-for="essayTopic in recommendEssayTopics"
          :key="essayTopic.id"
        >
          <nuxt-link :to="{ path: '/topic/' + essayTopic.topicNum }">
            <v-card
              class="mx-auto"
              color="#26c6da"
              dark
              max-width="400"
              style="height: 140px"
            >
              <div>
                <p class="topicNum">topic {{ essayTopic.topicNum }}</p>
              </div>
              <div>
                <p class="topic">
                  {{ essayTopic.topic }}
                </p>
              </div>
            </v-card>
          </nuxt-link>
        </v-col>
      </v-row>
    </v-container>
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
          v-for="essayTopic in essayTopics"
          :key="essayTopic.id"
        >
          <nuxt-link :to="{ path: '/topic/' + essayTopic.topicNum }">
            <v-card
              class="mx-auto"
              color="#26c6da"
              dark
              max-width="400"
              style="height: 140px"
            >
              <div>
                <p class="topicNum">topic {{ essayTopic.topicNum }}</p>
              </div>
              <div>
                <p class="topic">
                  {{ essayTopic.topic }}
                </p>
              </div>
            </v-card>
          </nuxt-link>
        </v-col>
      </v-row>
    </v-container>
    <h1 class="tabTitle">Conversational Topics</h1>
    <!-- <p>{{ essayTopicsR }}</p> -->
    <v-container>
      <v-row class="grey lighten-3">
        <v-col
          cols="6"
          sm="4"
          md="4"
          lg="2"
          xl="2"
          class="color1"
          v-for="essayTopic in essayTopicsR"
          :key="essayTopic.id"
        >
          <nuxt-link :to="{ path: '/topic/' + essayTopic.topicNum }">
            <v-card
              class="mx-auto"
              color="#26c6da"
              dark
              max-width="400"
              style="height: 140px"
            >
              <div>
                <p class="topicNum">topic {{ essayTopic.topicNum }}</p>
              </div>
              <div>
                <p class="topic">
                  {{ essayTopic.topic }}
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
import essayTopicsJsonR from "static/csv/essayTopicsR";
export default {
  data() {
    return {
      topicNums: Array(185)
        .fill(0)
        .map((v, i) => i + 1), // [1,2,3,4,,,185], なぜか [1]*185でも上手くいく模様。
      essayTopics: essayTopicsJson,
      essayTopicsR: essayTopicsJsonR,
      recommendEssayTopics: [
        essayTopicsJsonR[1], //C2
        essayTopicsJsonR[2], //C3
        essayTopicsJsonR[3], //C4
        essayTopicsJsonR[4], //C5
        essayTopicsJsonR[5], //C6
        essayTopicsJson[0], //1
        essayTopicsJson[2] //3
      ]
      // topicNumsR: essayTopicsJsonR.map(v => v.topicNum)
    };
  },
  methods: {
    shuffle(array) {
      for (let i = array.length - 1; i >= 0; i--) {
        let rand = Math.floor(Math.random() * (i + 1));
        // 配列の数値を入れ替える
        [array[i], array[rand]] = [array[rand], array[i]];
      }
      return array;
    }
  },
  created() {
    this.recommendEssayTopics = this.shuffle(this.recommendEssayTopics).slice(
      0,
      6
    );
  }
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
