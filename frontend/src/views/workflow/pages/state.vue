<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button-group>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >{{ "添加" }}</el-button>
      </el-button-group>
    </div>

    <el-table :data="list" border style="width: 100%" highlight-current-row>
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="类型" prop="state_type">
        <template slot-scope="{ row }">
          <span>{{row.state_type|StateTypeFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="排序" prop="order_id"></el-table-column>
      <el-table-column label="是否隐藏" prop="is_hidden">
        <template slot-scope="{ row }">
          <el-tag v-if="row.is_hidden" type="success">是</el-tag>
          <el-tag v-else type="danger">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group v-if="!row.is_hidden">
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >{{ "编辑" }}</el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >{{ "删除" }}</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="100px"
        style="margin-left:50px;"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="隐藏" prop="is_hidden">
          <el-switch v-model="temp.is_hidden" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="类型" prop="state_type">
          <el-select v-model="temp.state_type" clearable placeholder="请选择">
            <el-option
              v-for="(label, value) in state_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="order_id">
          <el-input v-model="temp.order_id" />
        </el-form-item>
        <el-form-item label="允许撤回" prop="enable_retreat">
          <el-switch v-model="temp.enable_retreat" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
          <a class="tips">允许工单创建人在此状态直接撤回工单到初始状态</a>
        </el-form-item>
        <el-form-item label="参与者类型" prop="participant_type">
          <el-select v-model="temp.participant_type" placeholder="请选择">
            <el-option
              v-for="(label, value) in participant_types"
              :key="value"
              :label="label"
              :value="label"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="temp.participant_type == 'user'" label="参与用户" prop="participant">
          <el-select v-model="temp.user_participant" multiple filterable placeholder="请选择">
            <el-option
              v-for="item in choice_user_list"
              :key="item.id"
              :label="item.username"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="temp.participant_type == 'group'" label="参与部门" prop="participant">
          <el-select v-model="temp.group_participant" multiple filterable placeholder="请选择">
            <el-option
              v-for="item in choice_group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="temp.participant_type == 'role'" label="参与角色" prop="participant">
          <el-select v-model="temp.role_participant" multiple filterable placeholder="请选择">
            <el-option
              v-for="item in choice_role_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="可編輯字段" prop="fields">
          <el-transfer
            v-model="temp.fields"
            filterable
            :titles="['未选择', '已选择']"
            :data="customfield_list"
            :props="permprops"
          ></el-transfer>
        </el-form-item>
        <el-form-item label="备注" prop="memo">
          <el-input v-model="temp.memo" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >{{ "确定" }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { state, user, group, role, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "state",
  props: {
    wfdata: {
      type: Object,
      default: {}
    },
    list: {
      type: Array,
      default: []
    },
    customfield_list: {
      type: Array,
      default: []
    }
  },

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
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "添加"
      },
      rules: {
        name: [{ required: true, message: "请输入名称", trigger: "blur" }]
      },
      state_types: {
        0: "普通状态",
        1: "初始状态",
        2: "结束状态"
      },
      participant_types: {
        0: "none",
        1: "user",
        2: "group",
        3: "role"
      },
      permprops: {
        key: "id",
        label: "field_name",
        disabled: "field_attribute"
      },
      choice_user_list: [],
      choice_group_list: [],
      choice_role_list: []
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.selectParticipant();
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
        .requestMenuButton("state")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    handleFilter() {},
    resetTemp() {
      this.temp = {
        memo: "",
        name: "",
        is_hidden: false,
        order_id: undefined,
        state_type: 0,
        enable_retreat: false,
        participant_type: 0,
        user_participant: [],
        group_participant: [],
        role_participant: [],
        fields: [],
        workflow: this.wfdata.id
      };
    },
    selectParticipant() {
      user.requestGet().then(response => {
        this.choice_user_list = response.results;
      });
      group.requestGet().then(response => {
        this.choice_group_list = response.results;
      });
      role.requestGet().then(response => {
        this.choice_role_list = response.results;
      });
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          state
            .requestPost(this.temp)
            .then(response => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "创建成功",
                type: "success",
                duration: 2000
              });
              this.$emit("checkdata");
            })
            .catch(() => {});
        }
      });
    },
    handleUpdate(row) {
      this.temp = row;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          state
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000
              });
              this.$emit("checkdata");
            })
            .catch(() => {});
        }
      });
    },
    handleDelete(row) {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          state.requestDelete(row.id).then(() => {
            this.$message({
              message: "删除成功",
              type: "success"
            });
            this.$emit("checkdata");
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    }
  }
};
</script>
