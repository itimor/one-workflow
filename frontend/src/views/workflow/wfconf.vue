<template>
  <div class="app-container">
    <el-card>
      <el-steps>
        <el-step v-for="item in state_list" :keys="item.id" status="finish" :title="item.name"></el-step>
      </el-steps>
    </el-card>

    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane label="工作流字段" name="customfield">
        <keep-alive>
          <tab-customfield
            @checkdata="getCustomfieldList"
            :wfdata="wfdata"
            :list="customfield_list"
          ></tab-customfield>
        </keep-alive>
      </el-tab-pane>

      <el-tab-pane label="工作流节点" name="state">
        <keep-alive>
          <tab-state
            @checkdata="getStateList"
            :wfdata="wfdata"
            :list="state_list"
            :customfield_list="customfield_list"
          ></tab-state>
        </keep-alive>
      </el-tab-pane>

      <el-tab-pane label="工作流步骤" name="transition">
        <keep-alive>
          <tab-transition
            @checkdata="getTransitionList"
            :wfdata="wfdata"
            :statedata="state_list"
            :list="transition_list"
          ></tab-transition>
        </keep-alive>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { workflow, customfield, state, transition, auth } from "@/api/all";
import tabCustomfield from "./pages/customfield";
import tabState from "./pages/state";
import tabTransition from "./pages/transition";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "wfconf",

  components: { tabCustomfield, tabState, tabTransition },
  data() {
    return {
      activeName: "customfield",
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      tempRoute: {},
      wfdata: {},
      customfield_list: [],
      state_list: [],
      transition_list: [],
      temp: {
        workflow: undefined,
      },
    };
  },

  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.temp.workflow = id;
      const params = {
        id: id
      };
      workflow.requestGet(params).then(response => {
        this.wfdata = response.results[0];
        this.setPageTitle();
        this.getCustomfieldList();
        this.getStateList();
        this.getTransitionList();
      });
    },
    getCustomfieldList() {
      customfield.requestGet(this.temp).then(response => {
        this.customfield_list = response.results;
      });
    },
    getStateList() {
      state.requestGet(this.temp).then(response => {
        this.state_list = response.results;
      });
    },
    getTransitionList() {
      transition.requestGet(this.temp).then(response => {
        this.transition_list = response.results;
      });
    },
    handleFilter() {
      this.fetchData();
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 配置`;
    }
  }
};
</script>