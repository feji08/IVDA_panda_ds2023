<template>
  <div>
    <v-row align="center" justify="center" class="mt-0.5 mb-0">
      <h3> Company Size </h3>
      <h3> vs. Average Company Size in {{ selectedCompanyCategory }}</h3>
    </v-row>
    <div style="height: 90vh">
      <div id='myBarChart' style="height: inherit"></div>
    </div>
  </div>
</template>



<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "BarChart",
  props: ["selectedCompanyId","selectedCompanyName"],
  data: () => ({
    BarChartData: {x: [], y: []},
    selectedCompanyCategory: ''
  }),
  mounted() {
    this.fetchData()
  },
  watch: {
    selectedCompanyId() {
      this.BarChartData.x = [];
      this.BarChartData.y = [];

      this.fetchData();
    },
    selectedCategory() {
      this.BarChartData.x = [];
      this.BarChartData.y = [];

      this.fetchData();
    }
  },
  methods: {
    async fetchAllCompaniesInCategory(category) {
      // 发送请求以获取所在类别的所有公司
      const reqUrl = 'http://127.0.0.1:5000/companies?category=' + category;
      const response = await fetch(reqUrl);
      return response.json();
    },
    async fetchSelectedCompanyData(companyId) {
      // 发送请求以获取选定公司的数据
      const reqUrl = 'http://127.0.0.1:5000/companies/' + companyId + '?algorithm=None';
      const response = await fetch(reqUrl);
      return response.json();
    },
    async fetchData() {
      // req URL to retrieve single company from backend
      const selectedCompanyData = await this.fetchSelectedCompanyData(this.$props.selectedCompanyId);
      //const selectedCompanyData = await this.fetchSelectedCompanyData(1);
      this.selectedCompanyCategory = selectedCompanyData.category;

      // req URL to retrieve all companies from the category above
      const allCompaniesInCategory = await this.fetchAllCompaniesInCategory(this.selectedCompanyCategory);

      // Calculate the average number of employees in the same category of companies
      let totalEmployeesInCategory = 0;
      let totalCompaniesInCategory = 0;

      // Iterate through all companies in the same category and get average employees in category
      for (const company of allCompaniesInCategory) {
        totalEmployeesInCategory += company.employees;
        totalCompaniesInCategory++;
      }
      const averageEmployeesInCategory = totalEmployeesInCategory / totalCompaniesInCategory; // Calculate the average

      // transform data to usable by barchart
      this.BarChartData.x.push(selectedCompanyData.name);
      this.BarChartData.x.push(this.selectedCompanyCategory + ' company');
      this.BarChartData.y.push(selectedCompanyData.employees);
      this.BarChartData.y.push(averageEmployeesInCategory);

      // draw the bar chart after the data is processed
      this.drawBarChart();
    },
    drawBarChart() {
      var data = [
        {
          x: this.BarChartData.x,
          y: this.BarChartData.y,
          type: 'bar'
        }
      ];
      var layout = {
        xaxis: {
          title: 'Company'
        },
        yaxis: {
          title: 'Employees'
        }
      }
      var config = { responsive: true, displayModeBar: false }
      Plotly.newPlot('myBarChart', data, layout, config);
    }
  }
}
</script>


<style scoped>

</style>
