<template>
  <div class="tooltip-wrapper">
    <v-network-graph v-model:selected-nodes="selectedNodes"
                   :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                   :configs="configs" ref="graph"
                   :event-handlers="eventHandlers"/>
    <div
        ref="tooltip"
        class="tooltip"
        :style="{ ...tooltipPos, opacity: tooltipOpacity }"
    >
      <div>Attribute Name:
        {{ targetNodeId!==""&& props.nodes[targetNodeId].name ? props.nodes[targetNodeId].name : "" }}
      </div><br>
      <div v-if="related_nodes.length > 0">
        <div>Related Attributes:</div>
        <ul>
          <li v-for="(node, index) in related_nodes" :key="index">
            {{ props.nodes[node].name }} - Coef: {{ related_coef[index].toFixed(2) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="control-panel" v-if="!props.overview">
    <button class="button zoom-in" @click="zoomIn">Zoom In</button>
    <button class="button zoom-out" @click="zoomOut">Zoom Out</button>
  </div>
</template>

<script setup>
import * as vNG from "v-network-graph";
import {VNetworkGraph} from "v-network-graph";
import "v-network-graph/lib/style.css";
import {computed, defineProps, getCurrentInstance, reactive, ref, watch} from "vue";

const graph = ref(null);
const tooltip = ref(null);
const layouts = ref(props.layouts);
const targetNodeId = ref("")
const tooltipOpacity = ref(0) // 0 or 1
const tooltipPos = ref({ left: "0px", top: "0px" })
const instance = getCurrentInstance();
const NODE_RADIUS = 8;

const targetNodePos = computed(() => {
  const layoutValue = layouts.value;
  if (layoutValue && layoutValue.nodes) {
    const nodePos = layoutValue.nodes[targetNodeId.value];
    return nodePos || { x: 0, y: 0 };
  } else {
    return { x: 0, y: 0 };
  }
});

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
        radius: NODE_RADIUS * props.scaleRatio,
        // borderRadius: 6 * props.scaleRatio,
        // radius: (node) => node.name === "new_pcs_node"? 6 * props.scaleRatio: undefined,
        // width: 6 * props.scaleRatio,
        // height: 6 * props.scaleRatio,
        color: (node) => node.name === props.indicator?  "#f14249":"#2c60d0",
      },
      selected: {
        type: "circle",
        strokeColor: "#f35b04",
        strokeWidth: 2,
        radius: NODE_RADIUS * props.scaleRatio,
        color: (node) => node.name === props.indicator?  "red":"#f7b801",
      },
      focusring: {
        visible: false,
      },
      label: {
        visible: !props.overview,
        fontSize: 12,
        color: (node) => node.name === props.indicator?  "red":"black",
      }
    },
    edge:{
      normal:{
        width: (edge) => 3 * edge.width * props.scaleRatio,
        color: (edge) => edge.color,
        dasharray: (edge) => edge.dasharray, // currently not working
      }
    },
    view: {
      autoPanAndZoomOnLoad: props.overview? "fit-content":false,
      panEnabled: !props.overview,
      zoomEnabled: !props.overview,
      fitContentMargin: 5,
      autoPanOnResize: true,
      layoutHandler: new vNG.GridLayout({ grid: 15 }),
    },
    grid: {
      visible: !props.overview,
    }
  }
)
const configs = reactive(initialConfigs)

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
  const bufferPercentage =0.05;
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
);

watch(
    () => [targetNodePos.value, tooltipOpacity.value],
    () => {
      if (!graph.value || !tooltip.value) return

      // translate coordinates: SVG -> DOM
      const domPoint = graph.value.translateFromSvgToDomCoordinates(targetNodePos.value)
      // calculates top-left position of the tooltip.
      tooltipPos.value = {
        left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
        top: domPoint.y - NODE_RADIUS - tooltip.value.offsetHeight - 10 + "px",
      }
    },
    { deep: true }
);

const related_nodes = ref([]);
const related_coef = ref([]);
const eventHandlers = {
  "node:pointerover": function ({ node }) {
    targetNodeId.value = node;
    tooltipOpacity.value = 1; // show

    const relatedNodes = [];
    const relatedCoef = [];

    const edges = ref(props.edges);

    // Loop through each edge object in edges.value
    for (const key in edges.value) {
      const edge = edges.value[key];
      if (edge.source === node) {
        relatedNodes.push(edge.target);
        relatedCoef.push(edge.width);
      } else if (edge.target === node) {
        relatedNodes.push(edge.source);
        relatedCoef.push(edge.width)
      }
    }

    related_nodes.value = relatedNodes;
    related_coef.value = relatedCoef;
  },
  "node:pointerout": function () {
    tooltipOpacity.value = 0; // hide
    related_nodes.value = [];
    related_coef.value = [];
  },
};

const zoomIn = () => {
  if (graph.value) {
    graph.value.zoomIn();
  }
};

const zoomOut = () => {
  if (graph.value) {
    graph.value.zoomOut();
  }
};

</script>

<style>
.control-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 12px;
  display: flex;
  gap: 10px;
}
.button {
  font-size: 12px;
  border: 1px solid rgba(134, 134, 246, 0.3);
  padding: 2px 2px;
}
.tooltip-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}
.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  width: 160px;
  height: 125px;
  display: grid;
  place-content: center;
  text-align: center;
  font-size: 12px;
  background-color: #fff0bd;
  border: 1px solid #ffb950;
  box-shadow: 2px 2px 2px #aaa;
  transition: opacity 0.2s linear;
  pointer-events: none;
}
</style>