<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div>
      <v-network-graph class="graph-container"
                       v-model:selected-nodes="selectedNodes"
                       :nodes="nodes" :edges="edges"
                       :configs="configs" />
    </div>
  </div>
</template>

<script setup>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import * as vNG from "v-network-graph"
import { onMounted, ref, reactive } from "vue";

const selectedNodes = ref([]);
const configs = reactive(vNG.getFullConfigs())
configs.node.selectable = 2
configs.edge.normal.width = (edge) => edge.width;
configs.edge.normal.color = (edge) => edge.color;
configs.edge.normal.dashed = (edge) => edge.dashed; // currently not working

// fake data
const nodes = {
  node1: { name: "Node 1" },
  node2: { name: "Node 2" },
  node3: { name: "Node 3" },
  node4: { name: "Node 4" },
};
const edges = {
  edge1: { source: "node1", target: "node2", width: 1, color: "orange", dashed: true  },
  edge2: { source: "node2", target: "node3", width: 5, color: "gray", dashed: true },
  edge3: { source: "node3", target: "node4", width: 1, color: "black", dashed: false },
};
const fetchData = async () => {
  try {
    // // req URL to retrieve single company from backend
    // var reqUrl = ""
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
onMounted(fetchData);
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 500px;
  border: 1px solid #adaaaa;
}
</style>