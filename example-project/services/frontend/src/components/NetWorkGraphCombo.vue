<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div class="network-graph-container">
      <NetWorkGraph :overview=false :scaleRatio=1 :viewBox="detailViewBox"/>
      <div class="network-graph-small">
        <NetWorkGraphSmall @updateViewBox="handleUpdateViewBox"/>
      </div>
    </div>
  </div>
</template>

<script>
import NetWorkGraph from './NetWorkGraph';
import NetWorkGraphSmall from "./NetWorkGraphSmall";

export default {
  components: {NetWorkGraph, NetWorkGraphSmall},
  data() {
    return {
      detailViewBox: null,
    };
  },
  methods:{
    handleUpdateViewBox(newViewBox){
      console.log('NetWorkGraph received newViewBox: ', newViewBox);
      this.detailViewBox=newViewBox;
    }
  },
}
</script>

<style>
.network-graph-container {
  position: relative;
  height: 300px;
  border: 1px solid #adaaaa;
}

.network-graph-small {
  position: absolute;
  bottom: 0;
  right: 0;
  height: 30%;
  width: 30%;
  background: #fdfdfd;
  border: 2px solid #adaaaa;
}
</style>