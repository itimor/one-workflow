<template>
  <div class="app-container">
    <div class="ticket">
      <el-card>
        <div slot="header" class="clearfix">
          <span class="ticket-title">流程</span>
        </div>
        <el-steps :active="temp.source_state" finish-status="success" process-status="finish">
          <el-step v-for="item in state_list" :ken="item.id" :title="item.name"></el-step>
        </el-steps>
      </el-card>
      <el-card>
        <div slot="header" class="clearfix">
          <span class="ticket-title">{{wfdata.name}}</span>
        </div>
        <div class="ticket-form" v-show="customfield_list.length>0">
          <el-form ref="dataForm" :rules="rules" :model="temp">
            <el-row :gutter="20">
              <el-col
                :md="{span: item.customfield.field_type === 65 ? 22 : 11}"
                v-for="item in customfield_list"
                :key="item.id"
              >
                <el-form-item :label="item.customfield.field_name">
                  <span>{{ item.field_value }}</span>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="处理意见" v-if="transition_list.length>1">
              <el-input
                type="textarea"
                :autosize="{ minRows: 5, maxRows: 8}"
                v-model="temp.suggestion"
              ></el-input>
            </el-form-item>

            <el-form-item style="text-align: center;" v-if="transition_list.length>1">
              <el-button
                v-for="item in transition_list"
                :key="item.id"
                :type="btn_types[item.attribute_type]"
                @click="handleButton(item)"
              >{{item.name}}</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card>
        <div slot="header" class="clearfix">
          <span class="ticket-title">操作日志</span>
        </div>
        <el-table :data="ticketlog_list" border style="width: 100%" highlight-current-row>
          <el-table-column label="节点" prop="state">
            <template slot-scope="{ row }">
              <span>{{row.state.name}}</span>
            </template>
          </el-table-column>
          <el-table-column label="参与者" prop="participant"></el-table-column>
          <el-table-column label="操作时间" prop="create_time"></el-table-column>
          <el-table-column label="处理意见" prop="suggestion"></el-table-column>
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
  auth
} from "@/api/all";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";
import { mapGetters } from "vuex";

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
      ticketlog_list: [],
      temp: {},
      rules: {},
      btn_types: {
        0: "primary",
        1: "primary",
        2: "danger",
        3: "danger",
        4: "warning",
        5: "warning"
      }
    };
  },
  computed: {
    ...mapGetters(["username"])
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.temp.ticket = id;
      const params = {
        id: id
      };
      ticket.requestGet(params).then(response => {
        this.wfdata = response.results[0];
        this.setTagsViewTitle();
        this.setPageTitle();

        this.temp.workflow = this.wfdata.workflow.id;
        this.temp.source_state = this.wfdata.state.id;
        this.getCustomfieldList();
        this.getStateList();
        this.getTicketlogList();
      });
    },
    getCustomfieldList() {
      ticketcustomfield.requestGet(this.temp).then(response => {
        this.customfield_list = response.results;
      });
    },
    getStateList() {
      state.requestGet(this.temp).then(response => {
        this.state_list = response.results;
        this.getTransitionList();
      });
    },
    getTransitionList() {
      transition.requestGet(this.temp).then(response => {
        this.transition_list = response.results;
      });
    },
    getTicketlogList() {
      ticketflowlog.requestGet(this.temp).then(response => {
        this.ticketlog_list = response.results;
      });
    },
    handleFilter() {
      this.fetchData();
    },
    setTagsViewTitle() {
      const title = this.wfdata.name;
      const route = Object.assign({}, this.tempRoute, {
        title: `${title} - 处理`
      });
      this.$store.dispatch("tagsView/updateVisitedView", route);
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 处理`;
    },
    handleButton(transition) {
      const data = Object.assign({}, this.wfdata, {
        transition: transition.id,
        state: transition.source_state.id,
        workflow: this.wfdata.workflow.id,
        create_user: this.username
      });
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          ticket
            .requestPut(data.id, data)
            .then(response => {
              this.temp = Object.assign(this.temp, {
                transition: transition.id,
                state: transition.source_state.id,
                participant: this.username
              });
              ticketflowlog.requestPost(this.temp).then(response => {
                this.$notify({
                  title: "成功",
                  message: "更新成功",
                  type: "success",
                  duration: 2000
                });
                this.$router.push({ path: "/todo_ticket" })
              });
            })
            .catch(() => {});
        }
      });
    }
  }
};
</script>