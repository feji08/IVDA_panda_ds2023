<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="3" class="sideBar">
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Company Overview</div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="categories.values"
                  label="Select a category"
                  dense
                  v-model="categories.selectedValue"
                  @change="changeCategory"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Profit View of Company</div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="companies.names"
                  label="Select a company"
                  dense
                  v-model="companies.selectedValue"
                  item-text="names"
                  @change="changeCompany"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="algorithm.values"
                  label="Select an algorithm for prediction"
                  dense
                  v-model="algorithm.selectedValue"
                  @change="changeAlgorithm"
              ></v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="3">
          <ScatterPlot :key="scatterPlotId"
                       :selectedCategory="categories.selectedValue"
                       @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
          />
        </v-col>
        <v-col cols="12" md="3">
          <LinePlot :key="linePlotId"
                    :selectedCompanyId="companies.companyNameToId[companies.selectedValue]"
                    :selectedCompanyName="companies.selectedValue"
                    :selectedAlgorithm="algorithm.selectedValue"
          />
        </v-col>
        <v-col cols="12" md="3">
          <BarChart :key="BarChartId"
                    :selectedCompanyId="companies.companyNameToId[companies.selectedValue]"
                    :selectedCompanyName="companies.selectedValue"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ScatterPlot from './ScatterPlot';
import LinePlot from './LinePlot';
import BarChart from './BarChart.vue';
export default {
  components: {ScatterPlot, LinePlot, BarChart},
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    BarChartId: 0,
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      selectedValue: 'alphabet',
      names:[],
      companyNameToId: []
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    }
  }),
    mounted() {
      this.fetchData()
    },
  methods: {
     async fetchData() {
      // req URL to retrieve companies from backend
       var reqUrl = 'http://127.0.0.1:5000/companies?category=All'
        console.log('ReqURL ' + reqUrl)
        // await response and data
        const response = await fetch(reqUrl)
        const responseData = await response.json();
        const companyNameToId = {};

        // get company data
        responseData.forEach((company) => {
          this.companies.names.push(company.name)
          companyNameToId[company.name] = company.id
          this.companies.companyNameToId = companyNameToId
       })
     },
    getCompanyName(value) {
      return this.companies.companyIdToName[value];
    },
    changeCurrentlySelectedCompany(companyName) {
      this.companies.selectedValue = companyName
      this.changeCompany()
    },
    changeCategory() {
      this.scatterPlotId += 1
    },
    changeCompany() {
      this.linePlotId += 1
    },
    changeAlgorithm() {
      this.linePlotId += 1
    }
  }
  }
</script>

<style scoped>
.control-panel-font {
  font-family: "Open Sans", verdana, arial, sans-serif;
  align-items: center;
  font-size: 19px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  font-weight: 800;
  height: 40px;
}
.sideBar {
  border-right: 2px solid rgba(0, 0, 0, 0.1);
  background: #edeafc;
  padding-left: 17px;
  height: calc(100vh - 50px);
}
</style>

