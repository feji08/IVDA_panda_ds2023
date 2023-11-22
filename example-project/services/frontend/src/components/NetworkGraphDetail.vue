<template>
  <div class="graph-container" ref="container">
    <NetWorkGraph :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                  :overview=false :scaleRatio=1
                  :viewBox="$props.detailViewBox" :indicator="$props.indicator"
                  :selectable="selectable"
                  @update-selection="handleUpdateSelection"/>
    <div class="buttons-container">
      <div class="instruction" v-show="showInstruction">"SHIFT" to select two nodes</div>
      <button class="grouping-button" @click="startSelection">SELECT</button>
      <button class="confirming-button" @click="groupNodes">GROUP</button>
    </div>
  </div>
</template>

<script>
import NetWorkGraph from "@/components/NetWorkGraph.vue";
export default {
  components: {NetWorkGraph},
  props: ["detailViewBox", "indicator", "nodes", "edges", "layouts"],
  data() {
    return {
      showInstruction: false,
      selectable: false,
      selectedNodes: {},
    };
  },
  methods: {
    startSelection() {
      this.showInstruction = true;
      this.selectable = true;
    },
    groupNodes() {
      this.showInstruction = false;
      this.selectable = false;
      if (this.selectedNodes.length === 2) {
        this.$emit('updateSelection', this.selectedNodes);
      }
    },
    handleUpdateSelection(newSelection) {
      this.selectedNodes = newSelection;
    }
  },
}
</script>

<style scoped>
.graph-container {
  position: relative;
}

.buttons-container {
  position: absolute;
  bottom: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
}

.instruction {
  font-size: 8px;
  color: #333; /* Set text color */
  position: absolute;
  bottom: 25px; /* Adjust the top position to create space above buttons */
  left: 0;
}

.grouping-button,
.confirming-button {
  font-size: 12px;
  border: 1px solid rgba(134, 134, 246, 0.3);
  padding: 2px 2px;
}

.grouping-button:hover,
.confirming-button:hover {
  background-color: rgba(134, 134, 246, 0.3);
}

</style>