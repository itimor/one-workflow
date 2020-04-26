<template>
  <div class="ticket-container">
    <el-row :gutter="20" style="margin-top:50px;">
      <el-col :span="6" v-for="item in list" :key="item.id">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>{{item.ticket_sn_prefix}}</span>
          </div>
          <div style="height:100px;">
            <router-link class="pan-btn light-blue-btn" :to="'/u_ticket/' + item.id">{{item.name}}</router-link>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { workflow, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "c_ticket",
  components: {},
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      list: []
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("wfset")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      workflow.requestGet().then(response => {
        this.list = response.results;
      });
    },
  }
};
</script>

<style scoped>
.ticket-container {
  background-color: #f0f2f5;
  padding: 30px;
  min-height: calc(100vh - 84px);
}
</style>
