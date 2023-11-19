<template>
  <v-network-graph v-model:selected-nodes="selectedNodes"
                   :nodes="nodes" :edges="edges" :layouts="layouts"
                   :configs="configs" ref="graph"/>
</template>

<script setup>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import * as vNG from "v-network-graph"
import {onMounted, ref, reactive, defineProps, computed, watch, getCurrentInstance} from "vue";

const graph = ref(null);
const instance = getCurrentInstance();

const props = defineProps({
  overview: Boolean,
  scaleRatio: Number,
  rectangle: Object,
  viewBox: Object,
  //props for JSON
  //startTime,endTime,attribute1,attribute2,attribute3,indicator,PCA
});

const selectedNodes = ref([]);
const configs = reactive(vNG.getFullConfigs())
configs.node.selectable = 2;

const defaultNodeRadius = 8;
configs.view.scalingObjects = true;
configs.view.autoPanAndZoomOnLoad = "fit-content";
configs.node.normal.radius = defaultNodeRadius * props.scaleRatio;
configs.edge.normal.width = (edge) => edge.width * props.scaleRatio;
configs.edge.normal.color = (edge) => edge.color;
configs.edge.normal.dasharray = (edge) => edge.dasharray; // currently not working
configs.node.label.visible = !props.overview;

// fake data
const nodes = {
  node1: { name: "Node 1" },
  node2: { name: "Node 2" },
  node3: { name: "Node 3" },
  node4: { name: "Node 4" },
};
const edges = {
  edge1: { source: "node1", target: "node2", width: 1, color: "orange", dasharray: "4 6"},
  edge2: { source: "node2", target: "node3", width: 5, color: "gray", dasharray: "4 6"},
  edge3: { source: "node3", target: "node4", width: 1, color: "black", dasharray: "4 6"},
};

const layouts = {
  nodes: {
    node1: { x: 0, y: 0 },
    node2: { x: 50, y: 50 },
    node3: { x: 100, y: 0 },
    node4: { x: 150, y: 50 },
  },
};
const fetchData = async () => {
  try {
    // // req URL to retrieve single company from backend
    // var reqUrl = "/networkGraph/layout"
    // console.log("ReqURL " + reqUrl)
    // // await response and data
    // const response = await fetch(reqUrl)
    // const responseData = await response.json();
    //
    // //parse nodes
    // responseData.nodes.forEach((node) => {
    //   this.nodes[node.id] = { name: node.name };
    // });
    // //edges
    // responseData.edges.forEach((edge) => {
    //   this.edges[edge.id] = { source: edge.source, target: edge.target };
    // });
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
      bottom:lt_svg.y}
  }
  return null;
});

onMounted(() => {
  fetchData();
});

watch(updateViewBox, (newVal) => {
  if (newVal !== null) {
    instance.emit('update-viewBox', newVal);
  }
});

watch(() => props.viewBox, (newVal) => {
  graph.value?.setViewBox(newVal)
});

</script>

<style>
</style>