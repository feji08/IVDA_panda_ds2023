<template>
  <v-col cols="12" sm="12">
    <v-row style="height: 15vh;">
      <v-col cols="12" sm="12" >
        <div >
          <div id='myCrossFilter1' style="height: 15px;"></div>
        </div>
      </v-col>
    </v-row>
    <v-row style="height: 15vh;">
      <v-col cols="12" sm="12">
        <div id='myCrossFilter2'></div>
      </v-col>
    </v-row>
    <v-row style="height: 15vh;">
      <v-col cols="12" sm="12">
        <div id='myCrossFilter3'></div>
      </v-col>
    </v-row>
    <v-row style="height: 25vh;">
      <v-col cols="12" sm="12">
        <div id='myBarChart' style="height: 100%; width: 100%;"></div>
      </v-col>
    </v-row>
  </v-col>
  <pre id="data">
Expt,Run,Speed
1,1,850
1,2,740
1,3,900
1,4,1070
1,5,930
1,6,850
1,7,950
1,8,980
1,9,980
1,10,880
1,11,1000
1,12,980
1,13,930
1,14,650
1,15,760
1,16,810
1,17,1000
1,18,1000
1,19,960
1,20,960
2,1,960
2,2,940
2,3,960
2,4,940
2,5,880
2,6,800
2,7,850
2,8,880
2,9,900
2,10,840
2,11,830
2,12,790
2,13,810
2,14,880
2,15,880
2,16,830
2,17,800
2,18,790
2,19,760
2,20,800
3,1,880
3,2,880
3,3,880
3,4,860
3,5,720
3,6,720
3,7,620
3,8,860
3,9,970
3,10,950
3,11,880
3,12,910
3,13,850
3,14,870
3,15,840
3,16,840
3,17,850
3,18,840
3,19,840
3,20,840
4,1,890
4,2,810
4,3,810
4,4,820
4,5,800
4,6,770
4,7,760
4,8,740
4,9,750
4,10,760
4,11,910
4,12,920
4,13,890
4,14,860
4,15,880
4,16,720
4,17,840
4,18,850
4,19,850
4,20,780
5,1,890
5,2,840
5,3,780
5,4,810
5,5,760
5,6,810
5,7,790
5,8,810
5,9,820
5,10,850
5,11,870
5,12,870
5,13,810
5,14,740
5,15,810
5,16,940
5,17,950
5,18,800
5,19,810
5,20,870
</pre>
</template>


<script>
import Plotly from 'plotly.js-dist/plotly';
import * as d3 from 'd3';
import crossfilter from 'crossfilter2';
import * as dc from 'dc';

export default {
  name: "RightBar",
  data: () => ({
    BarChartData: { x: [], y: [] },
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
        this.createCrossfilterInstance();
        this.plotBarChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    //TODO
    createCrossfilterInstance(){
      console.log('111:');
      var experiments = d3.csvParse(d3.select('pre#data').text());
      experiments.forEach(function(x) {
        x.Speed = +x.Speed;
      });
      // Create Crossfilter instance
      var cf = crossfilter(experiments);

      console.log('222:');
      // Create dimensions
      const attribute1Dim = cf.dimension(d => d.Expt);
      const attribute2Dim = cf.dimension(d => d.Run);
      const attribute3Dim = cf.dimension(d => d.Speed);

      // Create groups
      const attribute1Group = attribute1Dim.group();
      const attribute2Group = attribute2Dim.group();
      const attribute3Group = attribute3Dim.group();

      // Create  chart1
      //var chart1 = new dc.BarChart("#myCrossFilter1");
      // 获取最小和最大值，用于分组
      // const minDimension = selectDimension.bottom(1)[0][dimensionColumn];
      // const maxDimension = selectDimension.top(1)[0][dimensionColumn];

      // Adding a small epsilon value to ensure the upper bound is exclusive
      // const epsilon = 1e-10;
      // selectGroup = selectDimension.group(function(d) {
      //
      //   // 使用 bin 函数将数据分为 10 组
      //   return Math.floor((d - minDimension) / ((maxDimension - minDimension + epsilon) / 10)) * ((maxDimension - minDimension + epsilon) / 10);
      // });
      console.log('333:');
      var chart1 = new dc.BarChart("#myCrossFilter1");
      chart1
          .height(130)
          .x(d3.scaleLinear().domain([1, 5]))
          .brushOn(true)
          .yAxisLabel("Data number")
          .dimension(attribute1Dim)
          .group(attribute1Group)
          //.elasticX(true)
          .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
              console.log("click!", d);
            });
          });
      chart1.render();
      var chart2 = new dc.BarChart("#myCrossFilter2");
      chart2
          .height(130)
          .x(d3.scaleLinear().domain([1, 20]))
          .brushOn(true)
          .yAxisLabel("Data number")
          .dimension(attribute2Dim)
          .group(attribute2Group)
          //.elasticX(true)
          .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
              console.log("click!", d);
            });
          });
      chart2.render();
      var chart3 = new dc.BarChart("#myCrossFilter3");
      chart3
          .height(130)
          .x(d3.scaleLinear().domain([500, 1000]))
          .brushOn(true)
          .yAxisLabel("Data number")
          .dimension(attribute3Dim)
          .group(attribute3Group)
          //.elasticX(true)
          .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
              console.log("click!", d);
            });
          });
      chart3.render();

      // chart1.on('pretransition', function(chart) {
      //   let brushBegin = [], brushEnd = [];
      //   if(chart.filter()) {
      //     brushBegin = [chart.filter()[0]];
      //     brushEnd = [chart.filter()[1]];
      //   }
      //   let beginLabel = chart.select('g.brush')
      //       .selectAll('text.brush-begin')
      //       .data(brushBegin);
      //   beginLabel.exit().remove();
      //   beginLabel = beginLabel.enter()
      //       .append('text')
      //       .attr('class', 'brush-begin')
      //       .attr('text-anchor', 'end')
      //       .attr('dominant-baseline', 'text-top')
      //       .attr('fill', 'black')
      //       .attr('y', chart.margins().top)
      //       .attr('dy', 4)
      //       .merge(beginLabel);
      //   beginLabel
      //       .attr('x', d => chart.x()(d))
      //       .text(d => d.toFixed(2));
      //   let endLabel = chart.select('g.brush')
      //       .selectAll('text.brush-end')
      //       .data(brushEnd);
      //   endLabel.exit().remove();
      //   endLabel = endLabel.enter()
      //       .append('text')
      //       .attr('class', 'brush-end')
      //       .attr('text-anchor', 'begin')
      //       .attr('dominant-baseline', 'text-top')
      //       .attr('fill', 'black')
      //       .attr('y', chart.margins().top)
      //       .attr('dy', 4)
      //       .merge(endLabel);
      //   endLabel
      //       .attr('x', d => chart.x()(d))
      //       .text(d => d.toFixed(2));
      // })
      // chart1.render();
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
        font: { size: 10 },
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
/* Add any custom CSS styles here */
pre#data {
  display: none;
}
@import "../assets/dc.css";
</style>