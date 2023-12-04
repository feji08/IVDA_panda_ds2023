<template>
  <div>
    <v-container fluid="" class="main-container">
      <v-row>
        <v-col cols="16" md="4">
          <v-row>
            <v-col cols="12" sm="12">
              <h3 class="control-panel-font">Swipe to select time period</h3>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-range-slider
                  v-model="selectedTimeRange"
                  :min="new Date('2010-01').getTime()"
                  :max="new Date('2022-12').getTime()"
                  :step="30 * 24 * 60 * 60 * 1000"
                  thumb-label="always"
                  class="my-custom-thumb-label"
                  @mouseup="handleSliderChange"
              >
                <template v-slot:thumb-label="{ modelValue }">
                  {{ formatTimestamp(modelValue) }}
                </template>
              </v-range-slider>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <h3 class="control-panel-font">Swipe to cross filter data</h3>
            </v-col>
          </v-row>
          <v-row>
            <!--  传递的数据！！！ -->
            <RightBar class = "rightBar"
                      :key="RightBarId"
                      :selectedIndicator="indicators.selectedValue"
                      :selectedAlgorithm="algorithms.selectedValue"
                      :formattedTimeRange="formattedTimeRange"
                      :selectedNodes="selectedNodes"
                      @crossfilterDataChanged="handleCrossfilterDataChange"
            />
          </v-row>
        </v-col>
        <v-col cols="20" md="8">
          <v-row>
            <v-col cols="12" sm="6">
              <v-select
                  :items="indicators.names"
                  label="Select an indicator"
                  dense
                  v-model="indicators.selectedValue"
                  item-text="names"
                  @change="changeIndicator"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                  :items="algorithms.names"
                  label="Select an algorithm"
                  dense
                  v-model="algorithms.selectedValue"
                  item-text="names"
                  @change="changeAlgorithms"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <NetWorkGraphCombo
                  class = "graph"
                  :selectedIndicator="indicators.selectedValue"
                  :selectedAlgorithm="algorithms.selectedValue"
                  :formattedTimeRange="formattedTimeRange"
                  :SelectedCrossfilterDataRange="SelectedCrossfilterDataRange"
                  @updateSelection="handleUpdateSelection"/>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import NetWorkGraphCombo from './NetWorkGraphCombo.vue';
import RightBar from './RightBar';
export default {
  components: {NetWorkGraphCombo, RightBar},
  data: () => ({
    selectedTimeRange: [new Date('2010-01').getTime(), new Date('2022-12').getTime()],
    formattedTimeRange: ['2010-01','2022-12'],
    indicators: {
      names: ['revenue', 'netIncome', 'eps', 'grossProfit'],
      selectedValue: 'revenue',
    },
    algorithms: {
      names: ['PCA', 'K-Means'],
      selectedValue: 'PCA',
    },
    //这是传递的数据
    SelectedCrossfilterDataRange: [0, 1, 55279300, 45126800000, -1.2, 1.2],
    //这是传递的数据
    selectedNodes: ["",""],
  }),
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      return `${year}-${month}`;
    },
    handleSliderChange(){
      this.formattedTimeRange = this.selectedTimeRange.map(timestamp => this.formatTimestamp(timestamp));
      console.log('handleSliderChange:',this.formattedTimeRange)
    },
    handleCrossfilterDataChange(newData){
      this.SelectedCrossfilterDataRange = newData
      console.log('handleCrossfilterDataChange:',this.SelectedCrossfilterDataRange)
    },
    handleUpdateSelection(newVal){
      this.selectedNodes = newVal;
    }
  },
}
</script>


<style>
body {
  background-color: #a9c1d6;
}

.main-container {
  background-color: #a9c1d6;
}

.rightBar {
  border-radius: 5px;
  background-color: #fdfdfd;
}

.graph {
  border-radius: 5px;
  background-color: #fdfdfd;
}

.control-panel-font {
  font-size: 14px;
}

.v-range-slider .v-slider-thumb__label {
  min-width: 60px;
}

</style>