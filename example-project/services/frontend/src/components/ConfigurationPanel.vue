<template>
  <div>
    <v-container fluid="" class="main-container">
      <v-row>
        <v-col cols="16" md="4">
          <div class="left_panel">
            <v-row align="center" justify="center" class="mt-0.5 mb-0">
                <h3 class="control-panel-font">Swipe to Filter Stocks</h3>
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
            <!--          <v-row>-->
            <!--            <v-col cols="12" sm="12">-->
            <!--              <h3 class="control-panel-font">Swipe to cross filter data</h3>-->
            <!--            </v-col>-->
            <!--          </v-row>-->
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
          </div>
        </v-col>
        <v-col cols="20" md="8">
          <v-row>
            <v-col>
              <div class="selection-container">
                <v-select
                    :items="indicators.names"
                    label="Select an indicator"
                    dense
                    v-model="indicators.selectedValue"
                    item-text="names"
                    @change="changeIndicator"
                ></v-select>
                <v-select
                    :items="algorithms.names"
                    label="Select an algorithm"
                    dense
                    v-model="algorithms.selectedValue"
                    item-text="names"
                    @change="changeAlgorithms"
                ></v-select>
              </div>
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
      names: ['PCA', 'Factor Analysis'],
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
  background-color: #C0D6DF;
}

.main-container {
  background-color: #C0D6DF;
  display: flex;
  flex-wrap: wrap;
}

.left_panel {
  margin-top: 12px;
  min-height: 87vh;
  border-radius: 5px;
  background-color: #fdfdfd;
}

.control-panel-font {
  font-size: 14px;
  margin-top: 6px;
  max-height: 2px;
}

.v-range-slider .v-slider-thumb__label {
  min-width: 60px;
}

.v-range-slider .v-slider__container {
  width: 80%;
  margin-left: 10%;
}

.v-range-slider .v-slider-track__fill {
  height: 2px;
  background-color: #081460;
}

.v-range-slider .v-slider-thumb__surface {
  width: 6px;
  height: 20px;
  border-radius: 3px;
  margin-left: 6px;
}

.graph {
  border-radius: 5px;
  background-color: #fdfdfd;
}

.selection-container{
  border-radius: 5px;
  height:100%;
  max-height: 70px;
  background-color: #fdfdfd;
  display: flex;
}

.selection-container > * {
  margin: 15px;
}

.v-select .v-field.v-field--active.v-field--appended.v-field--center-affix.v-field--dirty.v-field--variant-filled.v-theme--light.v-locale--is-ltr{
  height:78%;
  padding-right: 0;
}

.v-select .v-field__overlay{
  height:75%;
  background: #ffffff;
  border-radius: 3px;
}

.v-select .v-field__loader,
.v-select .v-progress-linear{ /*lines under selection box */
  border: none;
}

.v-select .v-field__field, /* label and input container */
.v-select .v-field__append-inner{ /* right button container */
  height:75%;
  border: 0.5px solid #000000;
  background: #fdfdfd;
  border-radius: 3px;
  margin: 0;
  padding: 0;
}

.v-select .v-field-label{ /* select an algo container */
  height:50%;
  position: absolute;
  margin-top: -5px;
  margin-left: 10px;
}

.v-select .v-select__selection{ /* input container */
  height:75%;
  width: 200px;
  border-radius: 3px;
  margin-top: -4px;
}

.v-select .v-label,
.v-select .v-list .v-list-item__title,
.v-select .v-field-label,
.v-select .v-field .v-messages{
  font-size: 10px;
}

.v-select .v-select__selection-text{
  font-size: 14px;
}

</style>