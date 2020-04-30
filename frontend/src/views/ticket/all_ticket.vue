<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
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
        >{{ "搜索" }}</el-button>
        <el-button
          v-if="permissionList.del & username === 'admin'"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
        >{{ "删除" }}</el-button>
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
      <el-table-column v-if="username === 'admin'" type="selection" width="55" />
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="工单流水号" prop="sn" width="260">
        <template slot-scope="{ row }">
          <router-link :to="'/s_ticket/' + row.id">
            <el-link type="success">{{row.sn}}</el-link>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="当前状态" prop="state">
        <template slot-scope="{ row }">
          <span>{{row.state.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="进行状态" prop="transition">
        <template slot-scope="{ row }">
          <span>{{row.transition.attribute_type|AttributeTypeFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建者" prop="create_user">
        <template slot-scope="{ row }">
          <span>{{row.create_user.username}}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time"></el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.del & username === 'admin'"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >{{ "删除" }}</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
import { ticket, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";
import { mapGetters } from "vuex";

export default {
  name: "all_ticket",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined
      },
      multipleSelection: []
    };
  },
  computed: {
    ...mapGetters(["username"])
  },
  created() {
    this.getMenuButton();
    this.getList();
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
        .requestMenuButton("all_ticket")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      ticket.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
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
    handleDelete(row) {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          ticket.requestDelete(row.id).then(() => {
            this.$message({
              message: "删除成功",
              type: "success"
            });
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      if (this.multipleSelection.length === 0) {
        this.$message({
          message: "未选中任何行",
          type: "warning",
          duration: 2000
        });
        return;
      }
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          const ids = this.multipleSelection.map(x => x.id);
          ticket.requestBulkDelete(ids).then(response => {
            console.log(response.results);
            this.getList();
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
