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
      <el-table-column label="名称" prop="field_name"></el-table-column>
      <el-table-column label="标识" prop="field_key"></el-table-column>
      <el-table-column label="类型" prop="field_type">
        <template slot-scope="{ row }">
          <span>{{row.field_type|FieldTypeFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="排序" prop="order_id"></el-table-column>
      <el-table-column label="默认值" prop="default_value"></el-table-column>
      <el-table-column label="标签" prop="label"></el-table-column>
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
        <el-form-item label="字段名称" prop="field_name">
          <el-input v-model="temp.field_name" />
        </el-form-item>
        <el-form-item label="字段标识" prop="field_key">
          <el-input v-model="temp.field_key" />
          <a class="tips">字段类型请尽量特殊，避免与系统中关键字冲突</a>
        </el-form-item>
        <el-form-item label="字段类型" prop="field_type">
          <el-select v-model="temp.field_type" clearable placeholder="请选择">
            <el-option
              v-for="(label, value) in field_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="order_id">
          <el-input v-model="temp.order_id" />
        </el-form-item>
        <el-form-item label="默认值" prop="default_value">
          <el-input v-model="temp.default_value" />
          <a class="tips">前端展示时，可以将此内容作为表单中的该字段的默认值</a>
        </el-form-item>
        <el-form-item label="文本域模板" prop="field_template">
          <el-input v-model="temp.field_template" />
          <a class="tips">文本域类型字段前端显示时可以将此内容作为字段的placeholder</a>
        </el-form-item>
        <el-form-item label="布尔类型显示名" prop="boolean_field_display">
          <el-input v-model="temp.boolean_field_display" />
          <a class="tips">当为布尔类型时候，可以支持自定义显示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意数字也需要引号</a>
        </el-form-item>
        <el-form-item label="多选值" prop="field_choice">
          <el-input v-model="temp.field_choice" />
          <a
            class="tips"
          >radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{"1":"中国", "2":"美国"},注意数字也需要引号</a>
        </el-form-item>
        <el-form-item label="标签" prop="label">
          <el-input v-model="temp.label" />
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
import { customfield, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "customfield",
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
      field_types: {
        10: "字符串",
        15: "整形",
        20: "浮点型",
        25: "布尔",
        30: "日期",
        35: "时间",
        40: "日期时间",
        45: "单选框",
        50: "多选框",
        55: "下拉列表",
        60: "多选下拉列表",
        65: "文本域",
        70: "用户名",
        75: "多选的用户名"
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
        .requestMenuButton("customfield")
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
        field_type: "10",
        field_key: "",
        field_name: "",
        order_id: 10,
        default_value: "",
        field_template: "",
        boolean_field_display: "",
        field_choice: "",
        label: "",
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
          customfield
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
          customfield
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
            .catch(() => {
              this.loading = false;
            });
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
          customfield.requestDelete(row.id).then(() => {
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
