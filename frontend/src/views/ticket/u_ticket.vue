<template>
  <div class="app-container">
    <div class="ticket">
      <div class="ticket-form" v-if="customfield_list.length>0">
        <el-form ref="temp" :rules="rules" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工单标题">
                <el-input v-model="ticket.name" />
              </el-form-item>
            </div>
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
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  />

                  <el-input-number
                    v-if="item.field_type === 15"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-input-number>

                  <el-time-picker
                    v-if="item.field_type === 35"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-time-picker>

                  <el-date-picker
                    type="date"
                    v-if="item.field_type === 30"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.field_type === 40"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 4, maxRows: 6}"
                    v-if="item.field_type === 65"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-input>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.field_type === 25"
                    v-model="temp[item.field_key]"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-switch>

                  <el-radio-group
                    v-if="item.field_type === 45"
                    v-model="temp[item.field_key]"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-radio
                      v-for="(value, index) in JSON.parse(item.field_choice)"
                      :label="index"
                    >{{value}}</el-radio>
                  </el-radio-group>

                  <el-checkbox-group
                    v-if="item.field_type === 50"
                    v-model="temp[item.field_key]"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-checkbox
                      v-for="(value, index)  in JSON.parse(item.field_choice)"
                      :label="index"
                    >{{value}}</el-checkbox>
                  </el-checkbox-group>

                  <el-select
                    v-if="item.field_type === 55"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.field_choice)"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 60"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.field_choice)"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 70"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option v-for="t in user_list" :label="t.value">{{t.label}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 55"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option v-for="t in user_list" :label="t.value">{{t.label}}</el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item>
              <el-button
                v-for="item in transition_list"
                :key="item.id"
                :type="btn_types[item.name]"
                @click="handleButton('temp', item)"
              >{{item.name|TransitionNameFilter}}</el-button>

              <el-button type="warning" style="margin: 0 5px;" @click="reset('temp')">重置</el-button>
            </el-form-item>
          </el-card>
        </el-form>
      </div>
      <div v-else>
        <h1 style="text-align: center;">没有设置工作流字段</h1>
      </div>
    </div>
  </div>
</template>

<script>
import {
  workflow,
  customfield,
  state,
  transition,
  ticket,
  user,
  auth
} from "@/api/all";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";
import { mapGetters } from "vuex";
import Validators from "@/utils/validators";
import { GenDatetime, objectMerge } from "@/utils";

export default {
  name: "u_ticket",

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
      tempRoute: {},
      wfdata: {},
      customfield_list: [],
      state_list: [],
      transition_list: [],
      temp: {},
      rules: {},
      btn_types: {
        0: "primary",
        1: "success",
        2: "warning",
        3: "danger"
      },
      match_fields: [],
      ticket: {},
      workflow_temp: {
        participant: this.username
      }
    };
  },
  computed: {
    ...mapGetters(["username"])
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.getUserList();
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.workflow_temp.workflow = id;
      const params = {
        id: id
      };
      workflow.requestGet(params).then(response => {
        this.wfdata = response.results[0];
        this.setPageTitle();

        const d = new Date();
        this.ticket.name = this.wfdata.name + "-" + GenDatetime(d);
        this.getCustomfieldList();
        this.getStateList();
      });
    },
    getCustomfieldList() {
      customfield.requestGet(this.workflow_temp).then(response => {
        this.customfield_list = response.results;
      });
    },
    getStateList(id) {
      state.requestGet(this.workflow_temp).then(response => {
        this.state_list = response.results;
        this.match_fields = this.state_list[1].fields;
        this.getTransitionList(this.state_list[0].id);
      });
    },
    getTransitionList(source_state) {
      this.workflow_temp.source_state = source_state;
      transition.requestGet(this.workflow_temp).then(response => {
        this.transition_list = response.results;
      });
    },
    getUserList() {
      user.requestGet().then(response => {
        this.user_list = response.results;
      });
    },
    handleFilter() {
      this.fetchData();
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 创建`;
    },
    reset(formName) {
      this.$refs[formName].resetFields();
    },
    handleButton(dataForm, transition) {
      const customfield = [];
      for (var i of this.customfield_list) {
        if (this.temp[i.field_key]) {
          customfield.push({
            customfield: i.id,
            field_value: this.temp[i.field_key]
          });
        } else {
          customfield.push({
            customfield: i.id,
            field_value: ""
          });
        }
      }
      const data = Object.assign(
        {},
        {
          name: this.ticket.name,
          create_user: this.username,
          workflow: this.wfdata.id,
          state: transition.dest_state.id,
          transition: transition.id,
          customfield: JSON.stringify(customfield)
        }
      );

      this.$refs[dataForm].validate(valid => {
        if (valid) {
          ticket
            .requestPost(data)
            .then(res => {
              this.$notify({
                title: "成功",
                message: "创建成功",
                type: "success",
                duration: 2000
              });
              this.$router.push({ path: "/my_ticket" });
            })
            .catch(() => {});
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.card-solt {
  width: 450px;
}
</style>