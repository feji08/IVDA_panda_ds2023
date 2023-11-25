<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div class="network-graph-container">
      <NetWorkGraphDetail :nodes="nodes" :edges="edges" :layouts="layouts"
                          :detailViewBox="detailViewBox" :indicator="$props.selectedIndicator"
                          @updateSelection="handleUpdateSelection"/>
      <div class="network-graph-small">
        <NetWorkGraphSmall :nodes="nodes" :edges="edges" :layouts="layouts"
                           :indicator="$props.selectedIndicator"
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
      nodes:Object,
      edges:Object,
      layouts:Object,
      selection:[],//name needed instead of id
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
      Object.keys(selection).forEach((key) => {
        this.selection.push(this.nodes[selection[key]].name)
      });
      console.log(this.selection)
      this.$emit('updateSelection', this.selection);
      const postData = this.requestForNewNode();
      this.fetchData(postData,"/networkGraph/newNode");
    },
    updateDataConfigs() {
      // props -> dataConfigs
      this.dataConfigs = {
        indicator: this.selectedIndicator,
        algorithm: this.selectedAlgorithm,
      };
      const postData = this.requestForLayout();
      this.fetchData(postData,"/networkGraph/layout");
    },
    requestForLayout(){
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "price",
            "range": [10, 20]
          },
          "attribute2": {
            "name": "roe",
            "range": [0, 1]
          },
          "attribute3": {
            "name": "roic",
            "range": [0, 1]
          }
        }
      };
    },
    requestForNewNode(){
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "price",
            "range": [10, 20]
          },
          "attribute2": {
            "name": "roe",
            "range": [0, 1]
          },
          "attribute3": {
            "name": "roic",
            "range": [0, 1]
          }
        },
        "nodes": this.selection,
        "indicator": this.$props.selectedIndicator,
        "algorithm": this.$props.selectedAlgorithm
      };
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

        //parse nodes
        Object.keys(responseData.nodes).forEach((key) => {
          this.nodes[key] = {"name": responseData.nodes[key].name}
        });
        //edges
        Object.keys(responseData.edges).forEach((key) => {
          this.edges[key] = {"source": responseData.edges[key].source,
            "target": responseData.edges[key].target,
            "width": responseData.edges[key].width,
            "color": responseData.edges[key].width>0 ? "green": "red"
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
    this.fetchData(postData,"/networkGraph/layout")
  },
}

</script>

<style>
.network-graph-container {
  position: relative;
  height: 70vh;
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