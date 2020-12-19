
export default {
    filters: {
    formatDate: function(value) {
      let a = new Date(value.seconds * 1000);
      let year = ("0000" + a.getFullYear()).slice(-4);
      let month = ("00" + String(Number(a.getMonth()) + 1)).slice(-2);
      let date = ("00" + a.getDate()).slice(-2);
      let hour = ("00" + a.getHours()).slice(-2);
      let min = ("00" + a.getMinutes()).slice(-2);
      let sec = ("00" + a.getSeconds()).slice(-2);
      // let time = year + "/" + month + "/" + date + " " + hour + ":" + min;
      let time = month + "/" + date + " " + hour + ":" + min;
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
}
