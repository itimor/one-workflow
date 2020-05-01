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
                <el-form-item v-show="!item.field_attribute" :label="item.field_name" :prop="item.field_key">
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
                      :key="index"
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
                      :key="index"
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
                      :key="index"
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
                      :key="index"
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
                    <el-option v-for="t in user_list" :key="t.id" :label="t.id">{{t.username}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 55"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.id">{{t.username}}</el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item >
              <span style="margin: 0 5px;" v-for="item in transition_list" :key="item.id">
                  <el-popover  v-if="item.name===1" placement="top" title="选择转交人" width="160" v-model="visible">
                    <el-select v-model="ticket.participant" placeholder="请选择">
                      <el-option
                        v-for="item in choice_user_list"
                        :key="item.username"
                        :label="item.username"
                        :value="item.username">
                      </el-option>
                    </el-select>
                    <div style="text-align: right; margin: 0">
                      <el-button size="mini" type="text" @click="visible = false">取消</el-button>
                      <el-button type="primary" size="mini" @click="handleButton('temp', item)">确定</el-button>
                    </div>
                  <el-button slot="reference" v-if="item.name===1" :type="btn_types[item.name]" @click="selectUser('temp', item)">{{item.name|TransitionNameFilter}}</el-button>
                </el-popover>
                <el-button v-if="item.name!==1" :type="btn_types[item.name]" @click="handleButton('temp', item)">{{item.name|TransitionNameFilter}}</el-button>
              </span>
              <!-- <span style="margin: 0 5px;" v-for="item in transition_list" :key="item.id">
                <el-button v-if="item.name===1" :type="btn_types[item.name]" @click="selectUser('temp', item)">{{item.name|TransitionNameFilter}}</el-button>
                <el-button v-else :type="btn_types[item.name]" @click="handleButton('temp', item)">{{item.name|TransitionNameFilter}}</el-button>
              </span> -->
              <el-button type="warning" @click="reset('temp')">重置</el-button>
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
      user_list: [],
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
      },
      choice_user_list: []
    };
  },
  computed: {
    ...mapGetters(["user_id"])
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
    selectUser(dataForm,row) {
      const state = row.dest_state
      this.choice_user_list = []
      if (state.participant_type ===1 || state.participant_type ===2) {
        const data = state.participant.split(',')
        for (var i in data) {
          this.choice_user_list.push({id: i, username:data[i]})
        }
      } else if  (state.participant_type ===2 ) {
        const params = {
          group: state.participant
        }
        user.requestGet(params).then(response => {
          this.choice_user_list = response.results;
        });
      } else if  (state.participant_type ===3 ) {
        const params = {
          roles: state.participant
        }
        user.requestGet(params).then(response => {
          this.choice_user_list = response.results;
        });
      } else {
        this.choice_user_list = []
      }
    },
    handleButton(dataForm, transition) {
      const customfield = [];
      for (var i of this.customfield_list) {
        if (this.temp[i.field_key]) {
          customfield.push({
            customfield: i.id,
            field_key: i.field_key,
            field_value: this.temp[i.field_key]
          });
        } else {
          customfield.push({
            customfield: i.id,
            field_key: i.field_key,
            field_value: ""
          });
        }
      }
      const data = Object.assign(
        {},
        {
          name: this.ticket.name,
          participant: this.ticket.participant,
          create_user: this.user_id,
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
