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
      <el-select class="filter-item" clearable v-model="listQuery.method" placeholder="请选择请求方式">
        <el-option
          v-for="item in ['GET', 'POST','PUT','DELETE']"
          :key="item.id"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
      <el-button
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
      >
        {{ "搜索" }}
      </el-button>
    </div>

    <el-table :data="list" v-loading="listLoading" border style="width: 100%" @sort-change="handleSortChange">
      <el-table-column label="请求方法" prop="method" width="100"></el-table-column>
      <el-table-column label="请求路径" prop="url"></el-table-column>
      <el-table-column label="请求参数" prop="query_string">
        <template slot-scope="{row}">
          <el-tag size="mini">query_params</el-tag>: {{JSON.parse(row.query_string).query_params}}
          <br/>
          <el-tag size="mini">json</el-tag>: {{JSON.parse(row.query_string).json}}
        </template>
      </el-table-column>
      <el-table-column label="请求用户" prop="user" width="100"></el-table-column>
      <el-table-column label="请求ip" prop="remote_ip" width="100"></el-table-column>
      <el-table-column label="请求时间" prop="create_time" width="200"></el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.offset"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
  import {auditlog} from '@/api/all'
  import Pagination from '@/components/Pagination'

  export default {
    name: 'cdn',

    components: {Pagination},
    data() {
      return {
        list: [],
        total: 0,
        listLoading: true,
        loading: true,
        listQuery: {
          offset: 1,
          limit: 20,
          search: undefined,
          ordering: undefined
        },
      }
    },
    computed: {},
    created() {
      this.getList()
    },
    methods: {
      getList() {
        this.listLoading = true
        auditlog.requestGet(this.listQuery).then(response => {
          this.list = response.results
          this.total = response.count
          this.listLoading = false
        })
      },
      handleFilter() {
        this.getList()
      },
      handleSortChange(val) {
        if (val.order === 'ascending') {
          this.listQuery.ordering = val.prop
        } else if (val.order === 'descending') {
          this.listQuery.ordering = '-' + val.prop
        } else {
          this.listQuery.ordering = ''
        }
        this.getList()
      },
    }
  }
</script>
