<template>
  <v-network-graph v-model:selected-nodes="selectedNodes"
                   :nodes="nodes" :edges="edges" :layouts="layouts"
                   :configs="configs" ref="graph"/>
</template>

<script setup>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import * as vNG from "v-network-graph";
import {onMounted, ref, reactive, defineProps, computed, watch, getCurrentInstance} from "vue";

const graph = ref(null);
const instance = getCurrentInstance();

const nodes = ref({});
const edges = ref({});
const layouts = ref({});

const props = defineProps({
  overview: Boolean,
  selectable:Boolean,
  scaleRatio: Number,
  rectangle: Object,
  viewBox: Object,
  dataConfigs: Object,
  //props for JSON
  //startTime,endTime,attribute1,attribute2,attribute3,indicator,PCA
});

const selectedNodes = ref([]);
const configs = reactive(vNG.getFullConfigs())
configs.node.selectable = false; //default

const defaultNodeRadius = 3;
configs.view.scalingObjects = true;
configs.view.autoPanAndZoomOnLoad = props.overview? "fit-content":false;
configs.view.fitContentMargin = 15;
configs.node.draggable = false;
configs.node.normal.radius = defaultNodeRadius * props.scaleRatio;
configs.edge.normal.width = (edge) => edge.width * props.scaleRatio;
configs.edge.normal.color = (edge) => edge.color;
configs.edge.normal.dasharray = (edge) => edge.dasharray; // currently not working
configs.node.label.visible = !props.overview;
configs.node.label.fontSize = 2;

const fetchData = async (postData) => {
  try {
    // req URL to retrieve single company from backend
    var reqUrl = "http://127.0.0.1:5000/networkGraph/layout"
    console.log("ReqURL " + reqUrl)

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Specify the content type as JSON
      },
      body: JSON.stringify(postData), // Convert the postData object to a JSON string
    };

    // Make the POST request and wait for the response
    const response = await fetch(reqUrl, requestOptions);
    const responseData = await response.json();

    nodes.value = {};
    edges.value = {};
    layouts.value = {};

    //parse nodes
    Object.keys(responseData.nodes).forEach((key) => {
      nodes.value[key] = {"name": responseData.nodes[key].name}
    });
    //edges
    Object.keys(responseData.edges).forEach((key) => {
      edges.value[key] = {"source": responseData.edges[key].source,
                          "target": responseData.edges[key].target,
                          "width": responseData.edges[key].width,
                          "color": responseData.edges[key].width>0 ? "green": "red"
                          }
    });
    //layouts
    const layout_nodes = {}
    Object.keys(responseData.nodes).forEach((key) => {
      layout_nodes[key] = {"x": responseData.nodes[key].x*40,"y": responseData.nodes[key].y*40}
    });
    layouts.value = {"nodes": layout_nodes}
  } catch (error) {
    console.error('Error fetching data from the backend:', error);
  }
};

const updateViewBox = computed(() => {
  if(props.overview && graph.value && props.rectangle){
    const lt_point = {x:props.rectangle.left,y:props.rectangle.top};
    const rb_point = {x:props.rectangle.right,y:props.rectangle.bottom};
    const lt_svg = graph.value.translateFromDomToSvgCoordinates(lt_point);
    const rb_svg = graph.value.translateFromDomToSvgCoordinates(rb_point);
    return {left:lt_svg.x,
      right:rb_svg.x,
      top:lt_svg.y,
      bottom:rb_svg.y}
  }
  return null;
});

onMounted(() => {
  const postData = {
    "time": ["2010-01", "2022-10"],
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
  }
  fetchData(postData);
  // updateViewBox.value;// manually trigger update
});

watch(updateViewBox, (newVal) => {
  if (newVal !== null) {
    instance.emit('update-viewBox', newVal);
  }
});

watch(() => props.viewBox, (newVal) => {
  const bufferPercentage =0.15;
  const bufferX = (newVal.right - newVal.left) * bufferPercentage;
  const bufferY = (newVal.bottom - newVal.top) * bufferPercentage;
  const bufferedViewBox = {
    left: newVal.left - bufferX,
    right: newVal.right + bufferX,
    top: newVal.top - bufferY,
    bottom: newVal.bottom + bufferY
  };
  console.log(bufferedViewBox)
  graph.value?.setViewBox(bufferedViewBox)
});

watch(selectedNodes, (newVal) => {
  instance.emit('update-selection', newVal);
});

watch(() => props.dataConfigs, (newVal) => {
  const postData = {
    "time": ["2010-01", "2022-10"],
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
  }
  postData.time = newVal.time;
  postData.indicator = newVal.indicator;
  postData.Algorithm = newVal.algorithm;
  fetchData(postData);
});

watch(() => props.selectable, (newVal) =>{
    configs.node.selectable = newVal? 2:false;
  }
)

</script>

<style>
</style>