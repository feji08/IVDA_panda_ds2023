<template>
  <div style="height: 40vh;">
    <v-row>
      <v-col cols="12" sm="12">
        <div class="control-panel-font">Swipe to select time period</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="12">
        <v-range-slider
            v-model="selectedRange"
            min="2021"
            max="2023"
            thumb-label
        ></v-range-slider>
      </v-col>
    </v-row>
  </div>
  <div style="height: 43vh;">
    <div >
      <div id='myBarChart'></div>
    </div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly';
export default {
  name: "RightBar",
  data: () => ({
    BarChartData: { x: [], y: [] },
    //selectedCompanyCategory: '',
  }),
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // req URL to retrieve single company from backend
        var reqUrl = ''
        console.log("ReqURL " + reqUrl)
        // await response and data
        //const response = await fetch(reqUrl)
        // const responseData = await response.json();
        const responseData = {
          "x": ["D", "E", "D+E(selected data)", "D+E(all data)"],
          "y": [0.3, 0.2, 0.8, 0.6]
        }
        // 处理数据
        responseData.x.forEach((category) => {
          this.BarChartData.x.push(category);
        });
        responseData.y.forEach((value) => {
          this.BarChartData.y.push(value);
        });

        this.plotBarChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    plotBarChart() {
      const data = [{
        type: 'bar',
        x: this.BarChartData.x,
        y: this.BarChartData.y,
      }];

      const layout = {
        title: 'Coefficient with A',
        xaxis: { title: 'Categories' },
        yaxis: { title: 'Values' },
      };

      Plotly.newPlot('myBarChart', data, layout);
    },
  },
};
</script>
