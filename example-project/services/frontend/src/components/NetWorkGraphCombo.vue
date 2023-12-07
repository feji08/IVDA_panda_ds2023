<template>
  <div>
    <v-row class="title mt-0.5 mb-0 ml-3">
      <h3>Pairwise Correlation Coefficients of Stock Attributes</h3>
    </v-row>
    <v-row class="custom-info mt-0.5 mb-0 ml-3" v-if="showAdditionalText">
      <p>Network graph updated based on new configurations!</p>
    </v-row>
    <div class="main-graph-container">
      <div class="network-graph-container">
        <NetWorkGraphDetail :nodes="nodes" :edges="edges" :layouts="layouts"
                            :detailViewBox="detailViewBox" :indicator="$props.selectedIndicator"
                            @updateSelection="handleUpdateSelection"/>
      </div>
      <div class="right-panel">
        <v-row class="mt-0.5 mb-0 ml-1">
          <LegendForGraph/>
        </v-row>
        <div class="network-graph-small">
          <NetWorkGraphSmall :nodes="nodes" :edges="edges" :layouts="layouts"
                             :indicator="$props.selectedIndicator"
                             @updateViewBox="handleUpdateViewBox"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NetWorkGraphDetail from './NetworkGraphDetail';
import NetWorkGraphSmall from "./NetWorkGraphSmall";
import LegendForGraph from "@/components/LegendForGraph.vue";

export default {
  components: {LegendForGraph, NetWorkGraphDetail, NetWorkGraphSmall},
  props: ["selectedIndicator","selectedAlgorithm","formattedTimeRange","SelectedCrossfilterDataRange"],
  data() {
    return {
      detailViewBox: null,
      nodes:Object,
      edges:Object,
      layouts:Object,
      selection:[],//name needed instead of id
      showAdditionalText: false,
    };
  },
  watch: {
    selectedIndicator: "updateDataConfigs",
    selectedAlgorithm: "updateDataConfigs",
    formattedTimeRange: "updateDataConfigs",
    SelectedCrossfilterDataRange: {
      handler: "updateDataConfigs",
      deep: true,
    },
  },
  methods:{
    handleUpdateViewBox(newViewBox){
      // console.log('NetWorkGraph received newViewBox: ', newViewBox);
      this.detailViewBox=newViewBox;
    },
    handleUpdateSelection(selection){
      //After grouping this can be handled
      Object.keys(selection).forEach((key) => {
        this.selection.push(this.nodes[selection[key]].name)
      });
      console.log(this.selection)
      this.$emit('updateSelection', this.selection);
      const postData = this.requestForNewNode();
      this.fetchData(postData,"/networkGraph/newNode");
    },
    updateDataConfigs() {
      const postData = this.requestForLayout();
      console.log("update dataConfigs",postData)
      this.fetchData(postData,"/networkGraph/layout");
      this.showAdditionalText = true;
      setTimeout(() => {
        this.showAdditionalText = false;
      }, 2000);
    },
    requestForLayout(){
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "assetTurnover",
            "range": [this.$props.SelectedCrossfilterDataRange[0], this.$props.SelectedCrossfilterDataRange[1]]
          },
          "attribute2": {
            "name": "revenue",
            "range": [this.$props.SelectedCrossfilterDataRange[2], this.$props.SelectedCrossfilterDataRange[3]]
          },
          "attribute3": {
            "name": "roe",
            "range": [this.$props.SelectedCrossfilterDataRange[4], this.$props.SelectedCrossfilterDataRange[5]]
          }
        }
      };
    },
    requestForNewNode(){
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "assetTurnover",
            "range": [this.$props.SelectedCrossfilterDataRange[0], this.$props.SelectedCrossfilterDataRange[1]]
          },
          "attribute2": {
            "name": "revenue",
            "range": [this.$props.SelectedCrossfilterDataRange[2], this.$props.SelectedCrossfilterDataRange[3]]
          },
          "attribute3": {
            "name": "roe",
            "range": [this.$props.SelectedCrossfilterDataRange[4], this.$props.SelectedCrossfilterDataRange[5]]
          }
        },
        "nodes": this.selection,
        "indicator": this.$props.selectedIndicator,
        "algorithm": this.$props.selectedAlgorithm
      };
    },
    mapWidthToColor(width) {
      const colorMap = {
        0.9: "#023E8A",
        0.8: "#0096C7",
        0.7: "#48CAE4",
        0.6: "#ADE8F4",
        0: "#caf0f8",
        "-0.6": "#F9BD9D",
        "-0.7": "#F8AB81",
        "-0.8": "#F58A51",
        "-0.9": "#F05D0E",
        default: "#660708"
      };
      const sortedKeys = Object.keys(colorMap).map(parseFloat).sort((a, b) => b - a);
      for (let i = 0; i < sortedKeys.length; i++) {
        const currentKey = sortedKeys[i];
        if (width >= currentKey) {
          return colorMap[currentKey];
        }
      }
      return colorMap.default;
    },
    async fetchData(postData,url) {
      try {
        var reqUrl = "http://127.0.0.1:5000"+url
        console.log("ReqURL " + reqUrl)

        const requestOptions = {
          method: 'POST',
          headers: {'Content-Type': 'application/json', // Specify the content type as JSON
          },
          body: JSON.stringify(postData), // Convert the postData object to a JSON string
        };

        // Make the POST request and wait for the response
        const response = await fetch(reqUrl, requestOptions);
        const responseData = await response.json();

        this.nodes = {};
        this.edges = {};
        this.layouts = {};

        const nameMap = {
          "researchAndDdevelopementToRevenue": "R&D to Rev",
          "researchAndDevelopmentExpenses": "R&D Expenses",
          // "cashFlowToDebtRatio": "CFDR",
          "operatingCashFlowPerShare": "OCFPS",
        };


        //parse nodes
        Object.keys(responseData.nodes).forEach((key) => {
          const longName = responseData.nodes[key].name;
          const shortName = nameMap[longName] || longName;
          this.nodes[key] = { "name": shortName };
        });
        //edges
        Object.keys(responseData.edges).forEach((key) => {
          this.edges[key] = {"source": responseData.edges[key].source,
            "target": responseData.edges[key].target,
            "width": Math.abs(responseData.edges[key].width), // which is used later in the tooltips
            "color": this.mapWidthToColor(responseData.edges[key].width)
          }
        });
        //layouts
        const layout_nodes = {}
        Object.keys(responseData.nodes).forEach((key) => {
          layout_nodes[key] = {"x": responseData.nodes[key].x*50,"y": responseData.nodes[key].y*50}
        });
        this.layouts = {"nodes": layout_nodes}
      } catch (error) {
        console.error('Error fetching data from the backend:', error);
      }
    }
  },
  mounted(){
    this.$emit('updateSelection', ["",""]);
    const postData = this.requestForLayout();
    console.log("mounted postData",postData)
    this.fetchData(postData,"/networkGraph/layout")
  },
}

</script>

<style>
.main-graph-container {
  display: flex;
}

.title {
  max-height: 10px;
}

.custom-info {
  position:absolute;
  margin-top: -10px;
  font-size: 12px;
  color: #F05D0E;
}

.network-graph-container {
  position: relative;
  height: 67vh;
  width: 75%;
  margin-top:6%;
  left: 8px;
  bottom: 8px;
  background: #f8f9fa;
  //border: 0.5px solid #adaaaa;
  border-radius: 0 0 0 5px;
}

.right-panel {
  position: relative;
  height: 73vh;
  width: 25%;
  margin-left: 0px;
//background: #fdfdfd;
//border: 0.5px solid #adaaaa;
  border-radius: 0 0 5px 0;
}

.network-graph-small {
  position: absolute;
  left: 10px;
  bottom: 10px;
  right: 10px;
  height: 35%;
  background: #fdfdfd;
  border: 0.5px solid #E9ECEF;
  border-radius: 0 0 3px 0;
}
</style>