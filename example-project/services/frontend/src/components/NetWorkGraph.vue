<template>
  <v-network-graph v-model:selected-nodes="selectedNodes"
                   :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                   :configs="configs" ref="graph"/>
</template>

<script setup>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import * as vNG from "v-network-graph";
import {onMounted, ref, reactive, defineProps, computed, watch, getCurrentInstance} from "vue";

const graph = ref(null);
const instance = getCurrentInstance();

const props = defineProps({
  overview: Boolean,
  selectable:Boolean,
  scaleRatio: Number,
  rectangle: Object,
  viewBox: Object,
  netWork:Object,
  nodes:JSON,
  edges: JSON,
  layouts: JSON,
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

watch(() => props.selectable, (newVal) =>{
    configs.node.selectable = newVal? 2:false;
  }
)

</script>

<style>
</style>