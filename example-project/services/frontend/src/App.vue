<template>
  <v-app>
    <v-app-bar app color="#081460" dark>
      <div class="header-container">
        <h2>Stock Exploring</h2>
      </div>
    </v-app-bar>
    <v-main>
      <ConfigurationPanel/>
    </v-main>
  </v-app>
</template>


<script>
import ConfigurationPanel from './components/ConfigurationPanel.vue'

export default {
  name: 'App',

  components: {
    ConfigurationPanel,
  },

  data: () => ({
    //
  }),
}
</script>


<style>
/* disable scrolling */
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}
html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
.header-container {
  display: flex;
  justify-content: flex-end;
  width: 200px;
}
</style>
