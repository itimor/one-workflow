<template>
  <div class="app-container">
    <div class="ticket">
      <div class="ticket-form" v-if="customfield_list.length>0">
        <el-form ref="temp" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工单标题">
                <el-input v-model="ticket.name" />
              </el-form-item>
            </div>
            <el-row :gutter="20">
              <el-col
                :md="{span: [7, 8, 9, 12].includes(item.field_type)? 22 : 11}"
                v-for="item in customfield_list"
                :key="item.id"
              >
                <el-form-item
                  v-show="!item.field_attribute"
                  :label="item.field_name"
                  :prop="item.field_key"
                  :rules="match_fields.includes(item.id)?
                  [{ required: true, message: '请输入' + item.field_name, trigger: 'blur' },]:[]"
                >
                  <el-input
                    v-if="item.field_type === 1"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  />

                  <el-input-number
                    v-if="item.field_type === 2"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-input-number>

                  <el-date-picker
                    type="date"
                    v-if="item.field_type === 5"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.field_type === 6"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 4, maxRows: 6}"
                    v-if="item.field_type === 8"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-input>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.field_type === 4"
                    v-model="temp[item.field_key]"
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  ></el-switch>

                  <el-radio-group
                    v-if="item.field_type === 9"
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
                    v-if="item.field_type === 12"
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
                    v-if="item.field_type === 10"
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
                    v-if="item.field_type === 13"
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

                  <el-date-picker
                    v-if="item.field_type === 7"
                    v-model="temp[item.field_key]"
                    format="yyyy 年 MM 月 dd 日"
                    value-format="yyyy-MM-dd"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                  ></el-date-picker>

                  <el-select
                    v-if="item.field_type === 11"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    :disabled="item.field_attribute ||! match_fields.includes(item.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.id">{{t.username}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 14"
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
            <el-form-item>
              <span style="margin: 0 5px;" v-for="item in transition_list" :key="item.id">
                <el-button
                  v-if="item.name===1"
                  :type="btn_types[item.name]"
                  @click="selectUser('temp', item)"
                >{{item.name|TransitionNameFilter}}</el-button>
                <el-button
                  v-else
                  :type="btn_types[item.name]"
                  @click="handleButton('temp', item)"
                >{{item.name|TransitionNameFilter}}</el-button>
              </span>
            </el-form-item>
          </el-card>
        </el-form>
      </div>
      <div v-else>
        <h1 style="text-align: center;">没有设置工作流字段</h1>
      </div>
    </div>

    <el-dialog :visible.sync="dialogVisible">
      <div slot="title">
        当前下一步处理对象是：
        <a style="color: red; font-width:700;">{{dialogTitle}}</a>
        请点击下方对应类，并选择转交用户
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-collapse v-model="activeName" accordion @change="selectType">
            <el-collapse-item title="用户" name="1"></el-collapse-item>
            <el-collapse-item title="部门" name="2">
              <div v-if="group_role_list.length>0">
                <li
                  v-for="item in group_role_list"
                  :key="item.id"
                  @click="checkGroupUser(item.id)"
                >{{item.name}}</li>
              </div>
              <div v-else>没有可选部门</div>
            </el-collapse-item>
            <el-collapse-item title="角色" name="3">
              <div v-if="group_role_list.length>0">
                <li
                  v-for="item in group_role_list"
                  :key="item.id"
                  @click="checkRoleUser(item.id)"
                >{{item.name}}</li>
              </div>
              <div v-else>没有可选角色</div>
            </el-collapse-item>
          </el-collapse>
        </el-col>
        <el-col :span="16">
          <el-table :data="choice_user_list" @row-click="checkTableUser" style="width: 100%">
            <el-table-column prop="username" label="用户" width="180"></el-table-column>
            <el-table-column prop="realname" label="姓名"></el-table-column>
          </el-table>
        </el-col>
      </el-row>

      <el-row>
        <el-input readonly v-model="ticket.participant">
          <template slot="prepend">选择用户</template>
        </el-input>
      </el-row>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button
          :disabled="ticket.participant?false:true"
          type="primary"
          @click="handleButton('temp', choice_transition)"
        >确 定</el-button>
      </span>
    </el-dialog>
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
import { GenDatetime } from "@/utils";

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
      ticket: {
        name: "",
        participant: ""
      },
      workflow_temp: {
        participant: this.username
      },
      choice_user_list: [],
      dialogTitle: "",
      dialogVisible: false,
      activeName: "1",
      participant_list: [],
      choice_transition: {},
      group_role_list: [],
      participant_type: {
        0: "无处理人",
        1: "个人",
        2: "部门",
        3: "角色"
      }
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
    selectUser(dataForm, row) {
      this.$refs[dataForm].validate(valid => {
        if (valid) {
          this.dialogVisible = true;
          this.choice_transition = row;
          this.dialogTitle = this.participant_type[
            row.dest_state.participant_type
          ];
        }
      });
    },
    selectType(val) {
      this.ticket.participant = "";
      this.choice_user_list = [];

      if (val === 1) {
        this.choice_user_list = this.choice_transition.dest_state.user_participant;
      } else if (val == 2) {
        this.group_role_list = this.choice_transition.dest_state.group_participant;
      } else if (val == 3) {
        this.group_role_list = this.choice_transition.dest_state.role_participant;
      } else {
        this.group_role_list = [];
      }
    },
    checkGroupUser(id) {
      const params = {
        group: id
      };
      user.requestGet(params).then(response => {
        this.choice_user_list = response.results;
      });
    },
    checkRoleUser(id) {
      const params = {
        roles: id
      };
      user.requestGet(params).then(response => {
        this.choice_user_list = response.results;
      });
    },
    checkTableUser(row) {
      this.ticket.participant = row.username;
    },
    handleButton(dataForm, transition) {
      this.dialogVisible = false;
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
