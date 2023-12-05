<template>
  <v-col class= "barChart-container" cols="12" sm="12">
    <v-row class= "crossfilter-item-container" style="height: 15vh;">
      <v-col cols="12" sm="12">
        <div id='myCrossFilter1' style="height: 15px;"></div>
      </v-col>
    </v-row>
    <v-row class= "crossfilter-item-container" style="height: 15vh;">
      <v-col cols="12" sm="12">
        <div id='myCrossFilter2'></div>
      </v-col>
    </v-row>
    <v-row class= "crossfilter-item-container" style="height: 15vh;">
      <v-col cols="12" sm="12">
        <div id='myCrossFilter3'></div>
      </v-col>
    </v-row>
    <v-row class= "barChart-item-container" style="height: 25vh;">
      <v-col cols="12" sm="12">
        <div id='myBarChart' style="height: 100%; width: 100%;"></div>
      </v-col>
    </v-row>
  </v-col>
</template>


<script>
import Plotly from 'plotly.js-dist/plotly';
import * as d3 from 'd3';
import crossfilter from 'crossfilter2';
import * as dc from 'dc';

export default {
  name: "RightBar",
  props: ["selectedIndicator", "selectedAlgorithm", "formattedTimeRange", "selectedNodes"],
  data: () => ({
    BarChartData: { x: [], y: [] },
    SelectedCrossfilterDataRange: [0, 1, 55279300, 45126800000, -1.2, 1.2],
    CrossFilterData: [],
  }),
  watch: {
    selectedIndicator: "fetchDataBarChart",
    selectedAlgorithm: "fetchDataBarChart",
    formattedTimeRange: "fetchDataBarChart",
    SelectedCrossfilterDataRange: "fetchDataBarChart",
    selectedNodes: "fetchDataBarChart",
  },
  mounted() {
    this.fetchDataHistogram();
    this.fetchDataBarChart();
  },
  methods: {
    requestForCrossfilter() {
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "assetTurnover",
            "range": [0, 1]
          },
          "attribute2": {
            "name": "revenue",
            "range": [55279300, 45126800000]
          },
          "attribute3": {
            "name": "roe",
            "range": [-1.2, 1.2]
          }
        }
      };
    },
    requestForBarChart() {
      return {
        "time": this.$props.formattedTimeRange,
        "attributes": {
          "attribute1": {
            "name": "assetTurnover",
            "range": [this.SelectedCrossfilterDataRange[0], this.SelectedCrossfilterDataRange[1]]
          },
          "attribute2": {
            "name": "revenue",
            "range": [this.SelectedCrossfilterDataRange[2], this.SelectedCrossfilterDataRange[3]]
          },
          "attribute3": {
            "name": "roe",
            "range": [this.SelectedCrossfilterDataRange[4], this.SelectedCrossfilterDataRange[5]]
          }
        },
        "nodes": [this.$props.selectedNodes[0], this.$props.selectedNodes[1]],
        "indicator": this.$props.selectedIndicator,
        "algorithm": this.$props.selectedAlgorithm,
      };
    },
    async fetchDataHistogram() {
      try {
        console.log("fetchDataHistogram start:")
        // req URL to retrieve initial cross filter data from backend
        var reqUrl = "http://127.0.0.1:5000/histogram"
        console.log("ReqURL " + reqUrl)
        const postData = this.requestForCrossfilter();
        const requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json', // Specify the content type as JSON
          },
          body: JSON.stringify(postData), // Convert the postData object to a JSON string
        };
        // Make the POST request and wait for the response
        const response = await fetch(reqUrl, requestOptions);

        const responseData = await response.json();

        for (var i = 0; i < responseData.assetTurnover.length; i++) {
          // 构建新的对象并添加到 experiments 数组中
          this.CrossFilterData.push({
            "assetTurnover": responseData.assetTurnover[i],
            "revenue": responseData.revenue[i],
            "roe": responseData.roe[i]
          });

        }
        console.log("CrossFilterData ", this.CrossFilterData.slice(0, 10))
        this.createCrossfilterInstance();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async fetchDataBarChart() {
      try {
        console.log("fetchDataBarChart start:")


        // const responseData1 = {
        //   "x": ["D", "E", "D+E(selected data)", "D+E(all data)"],
        //   "y": [0.3, 0.2, 0.8, 0.6]
        // }
        // 处理数据
        // responseData1.x.forEach((category) => {
        //
        //   this.BarChartData.x.push(category);
        // });

        if (this.$props.selectedNodes[0].trim() === "" || this.$props.selectedNodes[0].trim() === "") {
          this.BarChartData = { x: ["null", "null", "null", "null"], y: [] }
        }
        else {
          // req URL to retrieve initial cross filter data from backend
          var reqUrl = "http://127.0.0.1:5000/barchart"
          console.log("ReqURL " + reqUrl)
          const postData = this.requestForBarChart();
          const requestOptions = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json', // Specify the content type as JSON
            },
            body: JSON.stringify(postData), // Convert the postData object to a JSON string
          };
          console.log("fetchDataBarChart start:1")
          // Make the POST request and wait for the response
          const response = await fetch(reqUrl, requestOptions);
          console.log("fetchDataBarChart start:2")
          const responseData = await response.json();
          console.log("fetchDataBarChart start:3")
          console.log("responseData ", responseData)
          // for (var i = 0; i < responseData1.y.length; i++) {
          //   this.BarChartData.x[i] = responseData1.x[i];
          // }
          this.BarChartData.x[0] = this.$props.selectedNodes[0];
          this.BarChartData.x[1] = this.$props.selectedNodes[1];
          this.BarChartData.x[2] = this.$props.selectedNodes[0] + "+" + this.$props.selectedNodes[1] + "(selected data)";
          this.BarChartData.x[3] = this.$props.selectedNodes[0] + "+" + this.$props.selectedNodes[1] + "(all data)";
          console.log("9 ")
          // responseData1.y.forEach((value) => {
          //   this.BarChartData.y.push(value);
          // });

          for (var j = 0; j < responseData.coefficients.values.length; j++) {
            this.BarChartData.y[j] = responseData.coefficients.values[j];
          }
          console.log("BarChartData ", this.BarChartData)
        }
        this.plotBarChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    createCrossfilterInstance() {
      console.log('111:');
      // var experiments = d3.csvParse(d3.select('pre#data').text());
      // experiments.forEach(function(x) {
      //   x.Speed = +x.Speed;
      // });
      //Create Crossfilter instance
      // console.log("experiments", ...experiments);
      var cf = crossfilter(this.CrossFilterData);
      console.log('CrossFilterData:', this.CrossFilterData.slice(0, 10));
      // 获取 Crossfilter 中的所有数据点
      var allData = cf.all();

      // 输出前几个数据点
      console.log('First 3 data points:', allData.slice(0, 3));

      console.log('222:');
      // Create dimensions
      const attribute1Dim = cf.dimension(d => d.assetTurnover);
      const attribute2Dim = cf.dimension(d => d.revenue);
      const attribute3Dim = cf.dimension(d => d.roe);
      console.log('attribute1Dim.top(3):', attribute1Dim.top(3));

      var scale = 1000000000; //billion
      var step = 5*scale;
      // Create groups
      const attribute1Group = attribute1Dim.group(function (d) { return Math.floor(d / 0.02) * 0.02; });
      const attribute2Group = attribute2Dim.group(function (d) { return Math.floor(d / step) * step; });
      console.log('333:');
      console.log(attribute2Group)
      const attribute3Group = attribute3Dim.group(function (d) { return Math.floor(d / 0.02) * 0.02; });


      var chart1 = new dc.BarChart("#myCrossFilter1");
      chart1
          .height(100)
          .x(d3.scaleLinear().domain([0, 1]))
          .brushOn(true)
          .xAxisLabel("Asset Turnover")
          .yAxisLabel("Number of Stocks")
          .dimension(attribute1Dim)
          .group(attribute1Group)
          .margins({ top: 10, right: 20, bottom: 50, left: 40 })  // 设置边距
          //.elasticX(true)
          .on('renderlet', function (chart) {
            chart.selectAll('rect').on("click", function (d) {
              console.log("click!", d);
            })
          })
          .on('renderlet', (chart) => {
            let brushBegin = '', brushEnd = '';
            if (chart.filter()) {
              brushBegin = chart.filter()[0];
              brushEnd = chart.filter()[1];
              console.log("SelectedCrossfilterDataRange", this.SelectedCrossfilterDataRange)
              this.SelectedCrossfilterDataRange[0] = brushBegin;
              this.SelectedCrossfilterDataRange[1] = brushEnd;
              // 触发自定义事件
              this.$emit('crossfilterDataChanged', this.SelectedCrossfilterDataRange);
            }
          })
          .yAxis().ticks(5);  // 设置y轴刻度数量;
      chart1.render();
      var chart2 = new dc.BarChart("#myCrossFilter2");
      chart2
          .height(100)
          .x(d3.scaleLinear().domain([0.05*scale, 50*scale]).rangeRound([0, 0.5*scale * 10]))
          .brushOn(true)
          .xAxisLabel("Revenue (USD in Billion)")
          .yAxisLabel("Number of Stocks")
          .dimension(attribute2Dim)
          .group(attribute2Group)
          .margins({ top: 10, right: 20, bottom: 50, left: 40 })  // 设置边距
          //.elasticX(true)
          .on('renderlet', function (chart) {
            chart.selectAll('rect').on("click", function (d) {
              console.log("click!", d);
            });
          })
          .on('renderlet', (chart) => {
            let brushBegin = '', brushEnd = '';
            if (chart.filter()) {
              brushBegin = chart.filter()[0];
              brushEnd = chart.filter()[1];
              console.log("SelectedCrossfilterDataRange", this.SelectedCrossfilterDataRange)
              this.SelectedCrossfilterDataRange[2] = brushBegin;
              this.SelectedCrossfilterDataRange[3] = brushEnd;
              // 触发自定义事件
              this.$emit('crossfilterDataChanged', this.SelectedCrossfilterDataRange);
            }
          })
          .yAxis().ticks(5);  // 设置y轴刻度数量;
      // 在图表渲染后执行的自定义操作
      chart2.on('renderlet', function (chart) {
        // 选择x轴上的刻度标签
        chart
            .selectAll('g.x text')
            .text(function(d) {
              return d3.format(".1f")(d/scale);
            })
            .attr('transform', 'rotate(0)') // 旋转刻度标签，这里是逆时针旋转10度
            .style('text-anchor', 'end'); // 设置旋转后的文本锚点位置，可以根据需要调整
      });
      chart2.render();
      var chart3 = new dc.BarChart("#myCrossFilter3");
      chart3
          .height(100)
          .x(d3.scaleLinear().domain([-0.4, 0.4]).rangeRound([0, 0.2 * 8]))
          .brushOn(true)
          .xAxisLabel("Roe")
          .yAxisLabel("Number of Stocks")
          .dimension(attribute3Dim)
          .group(attribute3Group)
          .margins({ top: 10, right: 20, bottom: 50, left: 40 })  // 设置边距
          //.elasticX(true)
          .on('renderlet', function (chart) {
            chart.selectAll('rect').on("click", function (d) {
              console.log("click!", d);
            });

          })
          .on('renderlet', (chart) => {
            let brushBegin = '', brushEnd = '';
            if (chart.filter()) {
              brushBegin = chart.filter()[0];
              brushEnd = chart.filter()[1];
              console.log("SelectedCrossfilterDataRange", this.SelectedCrossfilterDataRange)
              this.SelectedCrossfilterDataRange[4] = brushBegin;
              this.SelectedCrossfilterDataRange[5] = brushEnd;
              // 触发自定义事件
              this.$emit('crossfilterDataChanged', this.SelectedCrossfilterDataRange);
            }
          })
          .yAxis().ticks(5);  // 设置y轴刻度数量;
      chart3.render();
    },

    plotBarChart() {
      const data = [{
        type: 'bar',
        x: this.BarChartData.x,
        y: this.BarChartData.y,
        marker: {
          color: '#081460', // Set the color of the bars
        },
      }];

      const layout = {
        title: 'Coefficient with ' + this.$props.selectedIndicator,
        xaxis: { title: 'Categories' },
        yaxis: { title: 'Values' },
        font: { size: 8 },
        margin: {
          t: 30, // 设置上边距
          b: 40, // 设置下边距
          l: 30, // 设置左边距
          r: 30,  // 设置右边距
        },
      };

      Plotly.newPlot('myBarChart', data, layout);
    },
  },
};
</script>
<style>
#myCrossFilter1 g.axis text,
#myCrossFilter2 g.axis text,
#myCrossFilter3 g.axis text {
  font-size: 8px;
}

#myCrossFilter1 text.x-axis-label,
#myCrossFilter2 text.x-axis-label,
#myCrossFilter3 text.x-axis-label{
  font-size: 10px;
  /*position: absolute;
  margin-top:-10px;*/
}

#myCrossFilter1 text.y-axis-label,
#myCrossFilter2 text.y-axis-label,
#myCrossFilter3 text.y-axis-label{
  font-size: 9px;
  position: absolute;
  margin-left:-10px;
}



.barChart-container{
  margin-top:-10%;
}
.crossfilter-item-container,
.barChart-item-container{
  width: 90%;
  height: 80%;
  margin-left:5%;
  margin-bottom:2%;
}

#myCrossFilter1 .chart-body .bar,
#myCrossFilter2 .chart-body .bar,
#myCrossFilter3 .chart-body .bar{
  fill: #081460;
  stroke: #ffffff;
}

#myCrossFilter1 rect.bar {
  width: 1.5%; /* 根据需要调整宽度 */
}
#myCrossFilter2 rect.bar {
  width: 7.5%; /* 根据需要调整宽度 */
}
#myCrossFilter3 rect.bar {
  width: 2%; /* 根据需要调整宽度 */
}

</style>