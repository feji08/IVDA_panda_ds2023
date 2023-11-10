<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div style="height: 90vh">
      <v-network-graph :nodes="nodes" :edges="edges" />
    </div>
  </div>
</template>

<script>
import { VNetworkGraph } from "v-network-graph"
import "v-network-graph/lib/style.css"

export default {
  components: {VNetworkGraph},
  data() {
    return {
      nodes: {},
      edges: {},
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // req URL to retrieve single company from backend
        var reqUrl = ""
        console.log("ReqURL " + reqUrl)
        // await response and data
        const response = await fetch(reqUrl)
        const responseData = await response.json();

        //parse nodes
        responseData.nodes.forEach((node) => {
          this.nodes[node.id] = { name: node.name };
        });
        //edges
        responseData.edges.forEach((edge) => {
          this.edges[edge.id] = { source: edge.source, target: edge.target };
        });
      } catch (error) {
        console.error('Error fetching data from the backend:', error);
      }
    },
  },
};
</script>

<style scoped>
</style>