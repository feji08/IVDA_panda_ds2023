<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
    </v-row>
    <div style="height: 90vh">
      <div id='myScatterPlot' style="height: inherit"></div>
    </div>
  </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "ScatterPlot",
  props: [
    "selectedCategory"
  ],
  data: () => ({
    ScatterPlotData: {x: [], y: [], name: [], color: []},
  }),
  mounted() {
    this.fetchData()
  },
  watch: {
      selectedCategory: function () {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];

      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      console.log('ReqURL ' + reqUrl)
      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      const colorForCategory = {
        bank: 'yellow',
        tech: 'green',
        health: 'red',
      }
      const colorData = []

      // transform data to usable by scatterplot
      responseData.forEach((company) => {
        this.ScatterPlotData.name.push(company.name)
        this.ScatterPlotData.x.push(company.founding_year)
        this.ScatterPlotData.y.push(company.employees)
        this.ScatterPlotData.color.push(colorForCategory[company.category]);
        colorData.push(colorForCategory[company.category])
      })
      // after the data is loaded, draw the plot
      this.drawScatterPlot(colorData)
    },
    drawScatterPlot(colorData) {
      var trace1 = {
        x: this.ScatterPlotData.x,
        y: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        text: this.ScatterPlotData.name,
        marker: {
          color: colorData,
          size: 12
        }
      };
      var data = [trace1];
      var layout = {
        xaxis: {
          title: 'Founding_year'
        },
        yaxis: {
          title: 'Employees'
        }
      }
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myScatterPlot', data, layout, config);

      this.clickScatterPlot(colorData)
    },
    clickScatterPlot(colorData) {
      var pn = 0
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      var colors = colorData;
      var companyNames = this.ScatterPlotData.name;
      myPlot.on('plotly_click', function (data) {
        for (var i = 0; i < data.points.length; i++) {
          colors = colorData.slice();
          // get the index of point
          pn = data.points[i].pointNumber;

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', companyNames[pn])

          // and change currently selected color to blue
          colors[pn] = '#3777ee';

          // update the marker and plot
          var update = {'marker': {color: colors, size: 12}};
          Plotly.restyle('myScatterPlot', update);
        }
      });
    }
  }
}
</script>



<style scoped>

</style>