<template>
  <v-network-graph v-model:selected-nodes="selectedNodes"
                   :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                   :configs="configs" ref="graph"/>
</template>

<script setup>
import * as vNG from "v-network-graph";
import {VNetworkGraph} from "v-network-graph";
import "v-network-graph/lib/style.css";
import {computed, defineProps, getCurrentInstance, reactive, ref, watch} from "vue";

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
  indicator:String,
  //props for JSON
  //startTime,endTime,attribute1,attribute2,attribute3,indicator,PCA
});

const selectedNodes = ref([]);

const initialConfigs = vNG.defineConfigs({
    node:{
      selectable : false, //default
      draggable: false,
      normal: {
        // type: (node) => node.name === 'new_pca_node' ? "rect":"circle",
        strokeColor: (node) => node.name === 'new_pca_node' ? "red":"white",
        strokeWidth: 2,
        radius: 6 * props.scaleRatio,
        // borderRadius: 6 * props.scaleRatio,
        // radius: (node) => node.name === "new_pcs_node"? 6 * props.scaleRatio: undefined,
        // width: 6 * props.scaleRatio,
        // height: 6 * props.scaleRatio,
        color: (node) => node.name === props.indicator?  "red":"blue",
      },
      selected: {
        type: "circle",
        strokeColor: "yellow",
        strokeWidth: 2,
        radius: 6 * props.scaleRatio,
        color: (node) => node.name === props.indicator?  "red":"blue",
      },
      focusring: {
        visible: false,
      },
      label: {
        visible: !props.overview,
        fontSize: 6,
        color: (node) => node.name === props.indicator?  "red":"black",
      }
    },
    edge:{
      normal:{
        width: (edge) => 2 * edge.width * props.scaleRatio,
        color: (edge) => edge.color,
        dasharray: (edge) => edge.dasharray, // currently not working
      }
    },
    view: {
      autoPanAndZoomOnLoad: props.overview? "fit-content":false,
      fitContentMargin: -100,
    }
  }
)
const configs = reactive(initialConfigs)
// configs.node.selectable = false; //default
// configs.node.selected.strokeColor = "yellow";
// configs.node.selected.strokeWidth = 2;
// configs.node.normal.strokeColor = "white"
// configs.node.normal.strokeWidth = 1;


// configs.view.scalingObjects = true;
// configs.view.autoPanAndZoomOnLoad = props.overview? "fit-content":false;
// configs.view.fitContentMargin = -100;
// configs.node.draggable = false;
// configs.node.normal.radius = defaultNodeRadius * props.scaleRatio;
// configs.edge.normal.width = (edge) => edge.width * props.scaleRatio;
// configs.edge.normal.color = (edge) => edge.color;
// configs.edge.normal.dasharray = (edge) => edge.dasharray; // currently not working
// configs.node.label.visible = !props.overview;
// configs.node.label.fontSize = 6;
// configs.node.normal.color = (node) => node.name === props.indicator?  "red":"blue"
// configs.node.label.color = (node) => node.name === props.indicator?  "red":"black"

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

const updateFocus = computed(() => {
  let focus_svg={};
  if(props.indicator && props.nodes && graph.value){
    Object.keys(props.nodes).forEach((key) => {
      if(props.nodes[key].name===props.indicator){
        focus_svg = props.layouts.nodes[key];
      }
    });
    return focus_svg;
  }
  return null;
});
// const updateSelection = computed(() => {
//   if(selectedNodes.value.length===0){
//     return ["",""];
//   }else{
//     const attribute1 = props.nodes[selectedNodes.value[0]].name
//     const attribute2 = props.nodes[selectedNodes.value[1]].name
//     console.log([attribute1,attribute2])
//     return [attribute1,attribute2]
//   }
// });
watch(updateFocus,(newVal)=>{
  if (props.overview && newVal !== null){
    console.log("new focus computed: ",newVal)
    const focus_svg = {x:newVal.x,y:newVal.y};
    console.log("focus_svg: ",focus_svg);
    //get focus and calculate newViewBox
    // let box = graph.value?.getViewBox();
    // const boxWidth = box.bottom-box.top;
    // const boxHeight = box.right-box.left;
    // box = {top:focus_svg.y-boxHeight/2,bottom:focus_svg.y+boxHeight/2,
    //                 left:focus_svg.x-boxWidth/2,right:focus_svg.x+boxWidth/2}
    // graph.value?.setViewBox(newBox);
    // graph.value?.panTo(focus_svg);
    const focus_dom = graph.value.translateFromSvgToDomCoordinates(focus_svg);
    console.log("focus_dom: ",focus_dom)
    instance.emit('update-focus', focus_dom);
  }
})

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
  // console.log(bufferedViewBox)
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