<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
          >{{ "搜索" }}</el-button
        >
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
          >{{ "添加" }}</el-button
        >
        <el-button
          v-if="permissionList.del"
          :disabled="multipleSelection.length < 1"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
          >{{ "删除" }}</el-button
        >
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="排序" prop="sequence"></el-table-column>
      <el-table-column label="备注" prop="memo"></el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="320"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="mini"
              type="primary"
              @click="handleUpdate('base', row)"
              >{{ "编辑" }}</el-button
            >
            <el-popconfirm title="你确定要删除吗" @confirm="handleDelete(row)">
              <el-button
                slot="reference"
                v-if="permissionList.del"
                size="mini"
                type="danger"
                >{{ "删除" }}</el-button
              >
            </el-popconfirm>
          </el-button-group>
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="mini"
              type="success"
              plain
              @click="handleUpdate('menu', row)"
              >{{ "菜单" }}</el-button
            >
            <el-button
              v-if="permissionList.update"
              size="mini"
              type="warning"
              plain
              @click="handleUpdate('perm', row)"
              >{{ "权限" }}</el-button
            >
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > listQuery.limit"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>

    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="BaseFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
      >
        <div v-show="form == 'base'">
          <el-form-item label="父级" prop="parent">
            <SelectTree
              v-model.number="temp.parent"
              type="number"
              :props="propsSelectTree"
              :options="optionDataSelectTree2"
              :value="valueIdSelectTree2"
              :clearable="true"
              :accordion="true"
              @getValue="getSelectTreeValue($event, 2)"
            />
          </el-form-item>
          <el-form-item label="名称" prop="name">
            <el-input v-model="temp.name" />
          </el-form-item>
          <el-form-item label="代码" prop="code">
            <el-input v-model="temp.code" />
          </el-form-item>
          <el-form-item label="排序值" prop="sequence">
            <el-input v-model="temp.sequence" />
          </el-form-item>
          <el-form-item label="备注" prop="memo">
            <el-input v-model="temp.memo" />
          </el-form-item>
        </div>
        <div v-show="form == 'menu'">
          <el-form-item label="菜单" prop="menus">
            <el-tree
              ref="tree"
              :check-strictly="false"
              :data="treeData"
              :props="treeProps"
              show-checkbox
              :default-expanded-keys="[1]"
              :accordion="true"
              node-key="id"
              class="permission-tree"
            />
          </el-form-item>
        </div>
        <div v-show="form == 'perm'">
          <el-form-item label="模块权限" prop="model_perms">
            <el-transfer
              v-model="temp.model_perms"
              filterable
              :titles="['未选择', '已选择']"
              :data="allperm"
              :props="permprops"
            ></el-transfer>
          </el-form-item>
        </div>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="BaseFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
          >{{ "确定" }}</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { role, menu, perm, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import SelectTree from "@/components/TreeSelect";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "role",
  components: { Pagination, SelectTree },
  data() {
    return {
      valueIdSelectTree: 0,
      valueIdSelectTree2: 0,
      propsSelectTree: {
        value: "id",
        label: "name",
        children: "children",
        placeholder: "父级",
      },
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
      },
      form: "base",
      temp: {},
      BaseFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "添加",
      },
      rules: {
        name: [{ required: true, message: "请输入名称", trigger: "blur" }],
        code: [{ required: true, message: "请输入代码", trigger: "blur" }],
        sequence: [{ required: true, message: "请输入排序", trigger: "blur" }],
      },
      multipleSelection: [],
      treeProps: {
        children: "children",
        label: "name",
      },
      treeData: [],
      allrole: [],
      allperm: [],
      permprops: {
        key: "id",
        label: "name",
      },
    };
  },
  computed: {
    optionDataSelectTree2() {
      const cloneData = this.allrole;
      const ha = cloneData.filter((father) => {
        const branchArr = cloneData.filter(
          (child) => father.id === child.parent
        );
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === this.allrole[0].parent;
      });
      return ha;
    },
  },
  created() {
    this.getMenuButton();
    this.getList();
    this.getTreeData();
    this.getAllRole();
    this.getAllPerm();
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
        .requestMenuButton("role")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      role.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    getAllRole() {
      role.requestGet().then((response) => {
        this.allrole = response.results;
      });
    },
    getAllPerm() {
      perm.requestGet().then((response) => {
        this.allperm = response.results;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    },
    resetTemp() {
      this.temp = {
        name: "",
        code: "",
        sequence: "",
        menus: [],
        model_perms: [],
        memo: "",
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.BaseFormVisible = true;
      this.loading = false;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.temp.parent = this.valueIdSelectTree2;
          this.temp.menus = this.$refs.tree.getCheckedKeys();
          role
            .requestPost(this.temp)
            .then((response) => {
              this.BaseFormVisible = false;
              this.$notify({
                title: "成功",
                message: "创建成功",
                type: "success",
                duration: 2000,
              });
              this.getList();
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleUpdate(val, row) {
      this.temp = row;
      this.dialogStatus = "update";
      this.form = val;
      this.BaseFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
        this.valueIdSelectTree2 = this.temp.parent;
        this.$refs.tree.setCheckedKeys(this.temp.menus);
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          if (this.form == "menu") {
            this.temp.parent = this.valueIdSelectTree2;
            this.temp.menus = this.$refs.tree.getCheckedKeys();
          }
          role
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.BaseFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000,
              });
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleDelete(row) {
      role.requestDelete(row.id).then(() => {
        this.$message({
          message: "删除成功",
          type: "success",
        });
        this.getList();
      });
    },
    getSelectTreeValue(value, type) {
      if (type === 1) {
        this.valueIdSelectTree = value;
        this.handleFilter();
      } else {
        this.valueIdSelectTree2 = value;
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          const ids = this.multipleSelection.map((x) => x.id);
          role.requestBulkDelete(ids).then((response) => {
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    getTreeData() {
      menu.requestGet().then((response) => {
        this.treeData = this.optionDataSelectTree(response.results);
      });
    },
    optionDataSelectTree(data) {
      const cloneData = data;
      return cloneData.filter((father) => {
        const branchArr = cloneData.filter(
          (child) => father.id === child.parent
        );
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === data[0].parent;
      });
    },
  },
};
</script>