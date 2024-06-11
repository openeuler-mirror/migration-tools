import Vue from 'vue'
import VueRouter from 'vue-router'


const originalPush = VueRouter.prototype.push
   VueRouter.prototype.push = function push(location) {
   return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path:"/home",
    component:()=>import("../views/home.vue"),
    name:"home",
    children:[
     
      
      {
        path:"/software",
        component:()=>import("../components/software/software.vue"),
        name:"software",
      },{
        path:"/hostment",
        component:()=>import("../components/hostment/hostment.vue"),
        name:"hostment"
      },
      {
        path:"/hostlist",
        component:()=>import("../components/hostlist/hostlist.vue"),
        name:"hostlist"
      },{
          path:"/migrationtips",
          component:()=>import("../components/Migrationtips/migrationtips.vue"),
          name:"migrationtips"
      },
       {
         path:"/inspect",
         component:()=>import("../components/inspect/inspect.vue"),
         name:"inspect"
       },
      {
        path:"/loadcenter",
        component:()=>import("../components/loadcenter/loadcenter.vue"),
        name:"loadcenter"
      },{
        path:"/softpath",
        component:()=>import("../components/softpath/softpath.vue"),
        name:"softpath"
      },
      {
        path:"/record",
        component:()=>import("../components/record/record.vue"),
        name:"record"
      },{
        path:"/coredata",
        component:()=>import("../components/coredata/coredata.vue"),
        name:"coredata"
      },{
          path:"/transferlist",
          component:()=>import("../components/transferlist/transferlist.vue"),
          name:"transferlist"
      },{
        path:"/transfer",
        component:()=>import("../components/transfer/transfer.vue"),
          name:"transfer"
      }
    ]
  },{
    path:"/",
    redirect:"/software"

  }
]

const router = new VueRouter({
  mode:"hash",
  routes
})

export default router
