<template>
  <div class="app-container">
    <el-card>
      <div slot="header" class="clearfix">
        <h2 style="text-align: center;">{{wfdata.name}}</h2>
      </div>
      <div class="form" v-show="customfield_list.length>0">
        <el-form ref="dataForm" :rules="rules" :model="temp">
          <el-row :gutter="20">
            <el-col
              :md="{span: item.field_type === 65 ? 22 : 11}"
              v-for="item in customfield_list"
              :key="item.id"
            >
              <el-form-item :label="item.field_name" :prop="item.field_key">
                <el-input
                  v-if="item.field_type === 10"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                />
                <el-input-number
                  v-if="item.field_type === 15"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                ></el-input-number>
                <el-switch
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  v-if="item.field_type === 25"
                  v-model="temp[item.field_key]"
                ></el-switch>
                <el-time-picker
                  v-if="item.field_type === 35"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                ></el-time-picker>
                <el-date-picker
                  type="date"
                  v-if="item.field_type === 30"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                ></el-date-picker>
                <el-date-picker
                  type="datetime"
                  v-if="item.field_type === 40"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                ></el-date-picker>
                <el-input
                  type="textarea"
                  :autosize="{ minRows: 5, maxRows: 8}"
                  v-if="item.field_type === 65"
                  v-model="temp[item.field_key]"
                  :placeholder="item.field_name"
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item style="text-align: center;">
            <el-button
              v-for="item in transition_list"
              :key="item.id"
              :type="btn_types[item.attribute_type]"
            >{{item.name}}</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { workflow, customfield, state, transition, ticket, auth } from "@/api/all";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "u_ticket",

  components: {},
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
        workflow: undefined
      },
      rules: {},
      btn_types: {
        0: "primary",
        1: "danger",
        2: "warning"
      }
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
        this.setTagsViewTitle();
        this.setPageTitle();
        this.getCustomfieldList();
        this.getStateList();
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
        this.temp.source_state = this.state_list[0].id;
        this.getTransitionList();
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
    setTagsViewTitle() {
      const title = this.wfdata.name;
      const route = Object.assign({}, this.tempRoute, {
        title: `${title} - 创建`
      });
      this.$store.dispatch("tagsView/updateVisitedView", route);
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 创建`;
    },
    handleButton() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          this.temp.workflow = this.wfdata.id
          ticket
            .requestPost(this.temp)
            .then(response => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "创建成功",
                type: "success",
                duration: 2000
              });
            this.$emit('checkdata')
            })
            .catch(() => {});
        }
      });
    },
  }
};
</script>