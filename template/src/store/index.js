import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tableData:[],
    softpathData:[],
    xin2Data:[],
    tranferdata:[]
  },
  mutations: {
    getData(state,tableData){
      state.tableData=tableData
    },
    softData(state,softpathData){
      state.softpathData=softpathData
    },
    coreData(state,xin2Data){
      state.xin2Data=xin2Data
    },
    gotransfer(state,tranferdata){
      state.tranferdata=tranferdata
    }

    },
  plugins:[createPersistedState(
    {
      storage: window.sessionStorage,
      reducer(data){
        return{
          tableData : data.tableData,
          softpathData:data.softpathData,
          xin2Data:data.xin2Data,
          tranferdata:data.tranferdata
        }
      }
    }
  )],
  actions: {
  },
  modules: {
  }
})
