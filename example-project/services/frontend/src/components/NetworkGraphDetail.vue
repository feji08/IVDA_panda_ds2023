<template>
  <div class="graph-container" ref="container">
    <NetWorkGraph :dataConfigs="$props.dataConfigs"
                  :overview=false :scaleRatio=1 :viewBox="$props.detailViewBox"/>
    <div class="buttons-container">
      <button class="grouping-button" @click="startSelection">Start Selection</button>
      <button class="confirming-button" @click="groupNodes">Group Nodes</button>
    </div>
  </div>
</template>

<script>
import NetWorkGraph from "@/components/NetWorkGraph.vue";
export default {
  components: {NetWorkGraph},
  props: ["dataConfigs","detailViewBox"],
  data() {
    return {
      selectedNodes: Array,
    };
  },
  methods: {
    startSelection() {
      this.selectedNodes = [];
      console.log("startSelection")
    },
    groupNodes() {
      //
      console.log("groupNodes")
      // console.log(this.$props.detailViewBox)
    },
  },
};
</script>

<style scoped>
.graph-container {
  position: relative;
}

.buttons-container {
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  gap: 10px;
}
</style>