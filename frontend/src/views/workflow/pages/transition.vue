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
      <el-table-column label="类型" prop="transition_type">
        <template slot-scope="{ row }">
          <span>{{row.transition_type|TransitionTypeFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="上一个节点" prop="source_state">
        <template slot-scope="{ row }">
          <span>{{row.source_state.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="下一个节点" prop="dest_state">
        <template slot-scope="{ row }">
          <span>{{row.source_state.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="属性类型" prop="attribute_type">
        <template slot-scope="{ row }">
          <span>{{row.attribute_type|AttributeTypeFilter}}</span>
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
        <el-form-item label="类型" prop="transition_type">
          <el-select v-model="temp.transition_type" clearable placeholder="请选择">
            <el-option
              v-for="(label, value) in transition_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="定时器" prop="timer">
          <el-input v-model="temp.timer" />‘
          <a class="tips">流转类型设置为定时器流转时生效,单位秒。处于源状态X秒后如果状态都没有过变化则自动流转到目标状态</a>
        </el-form-item>
        <el-form-item label="属性类型" prop="attribute_type">
          <el-select v-model="temp.attribute_type" clearable placeholder="请选择">
            <el-option
              v-for="(label, value) in attribute_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上一个节点" prop="source_state">
          <el-select v-model="temp.source_state" clearable placeholder="请选择">
            <el-option
              v-for="item in statedata"
              :key="item.id"
              :label="item.name"
              :value="parseInt(item.id)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下一个节点" prop="dest_state">
          <el-select v-model="temp.dest_state" clearable placeholder="请选择">
            <el-option
              v-for="item in statedata"
              :key="item.id"
              :label="item.name"
              :value="parseInt(item.id)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="条件表达式" prop="condition_expression">
          <el-input v-model="temp.condition_expression" />
        </el-form-item>
        <el-form-item label="点击弹窗提示" prop="alert_enable">
          <el-switch v-model="temp.alert_enable" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="弹窗内容" prop="alert_text">
          <el-input v-model="temp.alert_text" />
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
import { transition, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "transition",
  props: {
    wfdata: {
      type: Object,
      default: {}
    },
    statedata: {
      type: Array,
      default: []
    },
    list: {
      type: Array,
      default: []
    }
  },
  components: {},
  data() {
    return {
      aaa: this.statedata,
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
      transition_types: {
        0: "常规流转",
        1: "定时器流转"
      },
      attribute_types: {
        0: "同意",
        1: "拒绝",
        2: "其他"
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
        .requestMenuButton("transition")
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
        transition_type: 0,
        timer: 0,
        condition_expression: "[]",
        attribute_type: 0,
        alert_enable: false,
        alert_text: "",
        source_state: 1,
        dest_state: 2,
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
          transition
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
    handleUpdate(row) {
      this.temp = Object.assign({}, row, {
        source_state: row.source_state.id,
        dest_state: row.dest_state.id
      });
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          transition
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000
              });
            this.$emit('checkdata')
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
          transition.requestDelete(row.id).then(() => {
            this.$message({
              message: "删除成功",
              type: "success"
            });
            this.$emit('checkdata')
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
