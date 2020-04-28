<template>
  <div class="app-container">
    <div class="ticket">
      <div class="ticket-form" v-if="customfield_list.length>0">
        <el-form ref="dataForm" :rules="rules" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工单标题">
                <el-input v-model="temp.name" />
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
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                  />

                  <el-input-number
                    v-if="item.field_type === 15"
                    v-model="temp.field_value"
                    :placeholder="item.field_name"
                  ></el-input-number>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.field_type === 25"
                    v-model="temp.fields[item.field_key]"
                  ></el-switch>

                  <el-time-picker
                    v-if="item.field_type === 35"
                    v-model="temp.fields[item.field_key]"
                    :placeholder="item.field_name"
                  ></el-time-picker>

                  <el-date-picker
                    type="date"
                    v-if="item.field_type === 30"
                    v-model="temp.fields[item.field_key]"
                    :placeholder="item.field_name"
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.field_type === 40"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 5, maxRows: 8}"
                    v-if="item.field_type === 65"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                  ></el-input>

                  <el-radio-group
                    v-if="item.field_type === 45"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                  >
                    <el-radio
                      v-for="t in JSON.parse(item.field_choice)"
                      :label="t.value"
                    >{{t.label}}</el-radio>
                  </el-radio-group>

                  <el-checkbox-group
                    v-if="item.field_type === 50"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                  >
                    <el-checkbox
                      v-for="t in JSON.parse(item.field_choice)"
                      :label="t.value"
                    >{{t.label}}</el-checkbox>
                  </el-checkbox-group>

                  <el-select
                    v-if="item.field_type === 55"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                    clearable
                  >
                    <el-option
                      v-for="t in JSON.parse(item.field_choice)"
                      :value="t.value"
                    >{{t.label}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 60"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                  >
                    <el-option
                      v-for="t in JSON.parse(item.field_choice)"
                      :value="t.value"
                    >{{t.label}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 70"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                    clearable
                  >
                    <el-option v-for="t in user_list" :label="t.value">{{t.label}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 55"
                    v-model="item.field_value"
                    :placeholder="item.field_name"
                    clearable
                    multiple
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
                :type="btn_types[item.attribute_type]"
                @click="handleButton(item)"
              >{{item.name}}</el-button>
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
import { GenDatetime } from "@/utils"

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
      temp: {
        name: "",
        fields: []
      },
      rules: {},
      btn_types: {
        0: "primary",
        1: "danger",
        2: "warning"
      }
    };
  },
  computed: {
    ...mapGetters(["username"]),

    FormRules() {
      let validators = {};
      this.customfield_list.map(item => {
        if (item.field_attribute) {
          if ([10, 45, 55, 65, 70].includes(item.field_type)) {
            validators[item.field_key] = [
              { required: true, type: "string", trigger: "blur" }
            ];
          } else if ([30, 35, 40].includes(item.field_type)) {
            validators[item.field_key] = [
              {
                validator: Validators.datetime,
                type: "date",
                trigger: "change"
              }
            ];
          } else if ([50, 60, 75].includes(item.field_type)) {
            validators[item.field_key] = [
              { required: true, type: "array", trigger: "change" }
            ];
          } else if ([15, 20].includes(item.field_type)) {
            validators[item.field_key] = [
              { required: true, type: "number", trigger: "blur" }
            ];
          } else if (item.field_type === 25) {
            validators[item.field_type] = [
              { required: true, type: "boolean", trigger: "blur" }
            ];
          }
        }
      });
      return validators;
    },
    newForm() {
      let form = {};
      for (let i = 0; i < this.customfield_list.length; i++) {
        if ([50, 60, 70].includes(this.customfield_list[i].field_type)) {
          form[this.customfield_list[i].field_key] = [];
        } else if ([15, 20].includes(this.customfield_list[i].field_type_id)) {
          form[this.customfield_list[i].field_key] = 0;
        } else {
          form[this.customfield_list[i].field_key] = "";
        }
      }
      return form;
    }
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.getUserList();
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

        const d = new Date();
        this.temp.name = this.wfdata.name + '-' + GenDatetime(d);
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
    getUserList() {
      user.requestGet().then(response => {
        this.user_list = response.results;
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
    handleButton(transition) {
      for (var i of this.customfield_list) {
        this.temp.fields.push({ id: i.id, field_value: i.field_value });
      }
      this.temp = Object.assign(this.temp, {
        transition: transition.id,
        state: transition.dest_state.id,
        workflow: this.wfdata.id,
        name: this.wfdata.name,
        create_user: this.username,
        customfield: JSON.stringify(this.temp.fields)
      });
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          ticket
            .requestPost(this.temp)
            .then(response => {
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