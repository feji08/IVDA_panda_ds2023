<template>
  <div class="graph-container" ref="container">
    <NetWorkGraph :nodes="$props.nodes" :edges="$props.edges" :layouts="$props.layouts"
                  :overview=false :scaleRatio=1
                  :viewBox="$props.detailViewBox" :indicator="$props.indicator"
                  :selectable="selectable"
                  @update-selection="handleUpdateSelection"/>
    <div class="buttons-container">
      <div
          class="instruction"
          v-show="showSelectInstruction || showGroupInstruction"
      >
        <span v-if="showSelectInstruction">
          Select two nodes <br>to see how two attributes together influence indicator. <br>
          <br>
          Hint: use "SHIFT" to select two nodes
        </span>
        <span v-if="showGroupInstruction">
          Click here for confirmation.
        </span>
      </div>
      <button
          class="grouping-button"
          @click="startSelection"
          @mouseover="showSelectInstruction = true"
          @mouseleave="showSelectInstruction = false"
      >
        SELECT
      </button>
      <button
          class="confirming-button"
          @click="groupNodes"
          @mouseover="showGroupInstruction = true"
          @mouseleave="showGroupInstruction = false"
      >
        GROUP
      </button>
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
      showSelectInstruction: false,
      showGroupInstruction: false
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

.title-container {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
  border: 1px solid rgba(134, 134, 246, 0.3);
}

.buttons-container {
  position: absolute;
  bottom: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
}

.instruction {
  font-size: 11px;
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

/* hover to show test */
.grouping-button:hover + .instruction,
.confirming-button:hover + .instruction {
  display: block;
}

</style>