<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div class="network-graph-container">
      <NetWorkGraphDetail :dataConfigs="dataConfigs" :detailViewBox="detailViewBox"
                          @updateSelection="handleUpdateSelection"/>
      <div class="network-graph-small">
        <NetWorkGraphSmall :dataConfigs="dataConfigs"
                           @updateViewBox="handleUpdateViewBox"/>
      </div>
    </div>
  </div>
</template>

<script>
import NetWorkGraphDetail from './NetworkGraphDetail';
import NetWorkGraphSmall from "./NetWorkGraphSmall";

export default {
  components: {NetWorkGraphDetail, NetWorkGraphSmall},
  props: ["selectedIndicator","selectedAlgorithm","formattedTimeRange"],
  data() {
    return {
      detailViewBox: null,
      dataConfigs: Object,
    };
  },
  watch: {
    selectedIndicator: "updateDataConfigs",
    selectedAlgorithm: "updateDataConfigs",
    formattedTimeRange: "updateDataConfigs",
  },
  methods:{
    handleUpdateViewBox(newViewBox){
      // console.log('NetWorkGraph received newViewBox: ', newViewBox);
      this.detailViewBox=newViewBox;
    },
    handleUpdateSelection(selection){
      //After grouping this can be handled
      console.log(selection)
    },
    updateDataConfigs() {
      // props -> dataConfigs
      this.dataConfigs = {
        "indicator": this.selectedIndicator,
        "algorithm": this.selectedAlgorithm,
        "time": this.formattedTimeRange,
      };
    }
  },
}
</script>

<style>
.network-graph-container {
  position: relative;
  height: 300px;
  border: 1px solid #adaaaa;
}

.network-graph-small {
  position: absolute;
  bottom: 0;
  right: 0;
  height: 30%;
  width: 30%;
  background: #fdfdfd;
  border: 2px solid #adaaaa;
}
</style>