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
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_hidden" type="success">是</el-tag>
          <el-tag v-else type="danger">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
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
        style="width: 400px; margin-left:50px;"
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
          <a class="tips">开启后允许工单创建人在此状态直接撤回工单到初始状态</a>
        </el-form-item>
        <el-form-item label="参与者类型" prop="participant_type">
          <el-select v-model="temp.participant_type" clearable placeholder="请选择">
            <el-option
              v-for="(label, value) in participant_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="参与者" prop="participant">
          <el-input v-model="temp.participant" />
          <a
            class="tips"
          >可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\部门id\角色id\变量(creator,creator_tl)\脚本记录的id等，包含子工作流的需要设置处理人为loonrobot</a>
        </el-form-item>
        <el-form-item label="表单字段" prop="state_field_str">
          <el-input v-model="temp.state_field_str" />
          <a
            class="tips"
          >json格式字典存储,包括读写属性1：只读，2：必填，3：可选. 示例：{"created_at":1,"title":2, "sn":1}, 内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称') # json格式存储,包括读写属性1：只读，2：必填，3：可选，4：不显示, 字典的字典</a>
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
import { state, auth } from "@/api/all";
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
        0: "无处理人",
        1: "个人",
        2: "多人",
        3: "部门",
        4: "角色"
      }
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
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
        order_id: 1,
        state_type: 1,
        enable_retreat: false,
        participant_type: 1,
        participant: "",
        state_field_str: '{"name":2,"start_time":2,"end_time":2}',
        workflow: this.wfdata.id
      };
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
