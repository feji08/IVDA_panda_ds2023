<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Related view of attributes</h3>
    </v-row>
    <div class="network-graph-container">
      <NetWorkGraph ScaleRatio=1 />
      <div class="network-graph-small">
        <NetWorkGraphSmall/>
      </div>
    </div>
  </div>
</template>

<script>
import NetWorkGraph from './NetWorkGraph';
import NetWorkGraphSmall from "./NetWorkGraphSmall";

export default {
  components: {NetWorkGraph, NetWorkGraphSmall},
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
  width: 40%;
  border: 2px solid #adaaaa;
}
</style>