<template>
  <div class="app-container">
    <div class="ticket">
      <el-card>
        <div slot="header" class="clearfix">
          <span class="card-title">流程</span>
        </div>
        <el-steps :active="stateActive" finish-status="success" process-status="finish">
          <el-step v-for="item in state_list" :key="item.id" :title="item.name"></el-step>
        </el-steps>
      </el-card>
      <div class="ticket-form" v-if="customfield_list.length>0">
        <el-form ref="temp" :rules="rules" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工单标题">
                <el-input disabled v-model="this.wfdata.name" />
              </el-form-item>
            </div>
            <el-row :gutter="20">
              <el-col
                :md="{span: item.customfield.field_type === 65 ? 22 : 11}"
                v-for="item in customfield_list"
                :key="item.id"
              >
                <el-form-item :label="item.customfield.field_name" :prop="item.field_key">
                  <el-input
                    v-if="item.customfield.field_type === 10"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  />

                  <el-input-number
                    v-if="item.customfield.field_type === 15"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-input-number>

                  <el-time-picker
                    v-if="item.customfield.field_type === 35"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-time-picker>

                  <el-date-picker
                    type="date"
                    v-if="item.customfield.field_type === 30"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.customfield.field_type === 40"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 4, maxRows: 6}"
                    v-if="item.customfield.field_type === 65"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-input>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.customfield.field_type === 25"
                    v-model="item.field_value"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-switch>

                  <el-radio-group
                    v-if="item.customfield.field_type === 45"
                    v-model="item.field_value"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-radio
                      v-for="(value, index) in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :label="index"
                    >{{value}}</el-radio>
                  </el-radio-group>

                  <el-checkbox-group
                    v-if="item.customfield.field_type === 50"
                    v-model="item.field_value"
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-checkbox
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :label="index"
                    >{{value}}</el-checkbox>
                  </el-checkbox-group>

                  <el-select
                    v-if="item.customfield.field_type === 55"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.customfield.field_type === 60"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    multiple
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.customfield.field_type === 70"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.id">{{t.username}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.customfield.field_type === 55"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    multiple
                    :disabled="item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.id">{{t.username}}</el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item>
              <span style="margin: 0 5px;" v-for="item in transition_list" :key="item.id">
                  <el-popover  v-if="item.name===1" placement="top" title="选择转交人" width="160" v-model="visible">
                    <el-select v-model="wfdata.participant" placeholder="请选择">
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
            </el-form-item>
          </el-card>
        </el-form>
      </div>

      <el-card>
        <div slot="header" class="clearfix">
          <span class="card-title">操作日志</span>
        </div>
        <el-table :data="ticketlog_list" border style="width: 100%" highlight-current-row>
          <el-table-column label="操作节点" prop="state">
            <template slot-scope="{ row }">
              <span>{{row.state.name}}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作类型" prop="transition">
            <template slot-scope="{ row }">
              <span>{{row.transition.attribute_type|AttributeTypeFilter}}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作者" prop="participant"></el-table-column>
          <el-table-column label="操作时间" prop="create_time"></el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import {
  ticketcustomfield,
  state,
  transition,
  ticket,
  ticketflowlog,
  user,
  auth
} from "@/api/all";
import { mapGetters } from "vuex";

export default {
  name: "s_ticket",

  components: {},
  data() {
    return {
      visible: false,
      tempRoute: {},
      wfdata: {},
      customfield_list: [],
      state_list: [],
      transition_list: [],
      ticketlog_list: [],
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
      workflow_temp: {
        participant: this.username,
        is_hidden: false
      },
      stateActive: 999,
      choice_user_list: [],
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
      this.workflow_temp.ticket = id;
      const params = {
        id: id
      };
      ticket.requestGet(params).then(response => {
        this.wfdata = response.results[0];
        this.setPageTitle();

        this.workflow_temp.workflow = this.wfdata.workflow.id;
        this.workflow_temp.source_state = this.wfdata.state.id;
        this.match_fields = this.wfdata.state.fields;

        this.getCustomfieldList();
        this.getStateList();
        this.getTicketlogList();
      });
    },
    getCustomfieldList() {
      ticketcustomfield.requestGet(this.workflow_temp).then(response => {
        this.customfield_list = response.results;
      });
    },
    getStateList() {
      state.requestGet(this.workflow_temp).then(response => {
        this.state_list = response.results
        for (var i in this.state_list) {
          if (this.state_list[i].id == this.wfdata.state.id && this.wfdata.state.state_type <2) {
            this.stateActive = parseInt(i);
            break
          }
        }
        this.getTransitionList();
      });
    },
    getTransitionList() {
      transition.requestGet(this.workflow_temp).then(response => {
        this.transition_list = response.results;
      });
    },
    getTicketlogList() {
      ticketflowlog.requestGet(this.workflow_temp).then(response => {
        this.ticketlog_list = response.results;
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
      document.title = `${title} - 处理`;
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
        customfield.push({
          id: i.id,
          ticket: i.ticket.id,
          customfield: i.customfield.id,
          field_value: i.field_value
        });
      }
      const data = Object.assign(
        {},this.wfdata,
        {
          create_user: this.wfdata.create_user.id,
          workflow: this.wfdata.workflow.id,
          state: transition.dest_state.id,
          transition: transition.id,
          customfield: JSON.stringify(customfield)
        }
      );
      this.$refs[dataForm].validate(valid => {
        if (valid) {
          ticket
            .requestPut(this.wfdata.id, data)
            .then(response => {
                this.$notify({
                  title: "成功",
                  message: "更新成功",
                  type: "success",
                  duration: 2000
                });
                this.$router.push({ path: "/todo_ticket" });
            })
            .catch(() => {});
        }
      });
    }
  }
};
</script>