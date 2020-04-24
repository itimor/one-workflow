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
        >
          {{ "搜索" }}
        </el-button>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >
          {{ "添加" }}
        </el-button>
        <el-button
          v-if="permissionList.del"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
        >
          {{ "删除" }}
        </el-button>
      </el-button-group>
    </div>

    <el-table :data="list" v-loading="listLoading" border style="width: 100%" highlight-current-row @sort-change="handleSortChange"
              @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column label="菜单名称" prop="name"></el-table-column>
      <el-table-column label="菜单代码" prop="code"></el-table-column>
      <el-table-column label="排序值" prop="sequence"></el-table-column>
      <el-table-column label="菜单类型" prop="type">
        <template slot-scope="scope">
          <span>{{ scope.row.type | menuTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作类型" prop="operate">
        <template slot-scope="scope">
          <span>{{ scope.row.operate | operateTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="菜单状态" prop="status">
        <template slot-scope="scope">
          <span>{{scope.row.status}}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group v-show="row.id !== 1">
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >
              {{ "编辑" }}
            </el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              {{ "删除" }}
            </el-button>
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
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="父级" prop="parent">
          <SelectTree
            v-model.number="temp.parent"
            type="number"
            :props="propsSelectTree"
            :options="optionDataSelectTree"
            :value="valueIdSelectTree2"
            :clearable="true"
            :accordion="true"
            @getValue="getSelectTreeValue($event, 2)"
          />
        </el-form-item>
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="temp.name"/>
        </el-form-item>
        <el-form-item label="菜单代码" prop="code">
          <el-input v-model="temp.code"/>
        </el-form-item>
        <el-form-item label="菜单URL" prop="curl">
          <el-input v-model="temp.curl"/>
        </el-form-item>
        <el-form-item label="菜单图标" prop="icon">
          <el-input v-model="temp.icon"/>
        </el-form-item>
        <el-form-item label="排序值" prop="sequence">
          <el-input v-model="temp.sequence"/>
        </el-form-item>
        <el-form-item label="菜单类型" prop="type">
          <el-select v-model.number="temp.type" placeholder="状态" style="width: 90px" @change="handleshowOpera">
            <el-option
              v-for="item in menuTypeOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item v-show="showOpera" label="操作类型" prop="operate">
          <el-select v-model="temp.operate" placeholder="状态" style="width: 90px" class="filter-item">
            <el-option
              v-for="item in operateTypeOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="菜单状态" prop="status">
          <el-switch
            v-model="temp.status"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>
        </el-form-item>
                <el-form-item label="隐藏菜单" prop="hidden">
          <el-switch
            v-model="temp.hidden"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>
        </el-form-item>
        <el-form-item label="备注" prop="memo">
          <el-input v-model="temp.memo"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
          {{ "确定" }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {menu, auth} from '@/api/all'
  import Pagination from '@/components/Pagination'
  import SelectTree from '@/components/TreeSelect'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'

  export default {
    name: 'ymenu',

    components: {Pagination, SelectTree},
    data() {
      return {
        valueIdSelectTree: 0,
        valueIdSelectTree2: 0,
        propsSelectTree: {
          value: 'id',
          label: 'name',
          children: 'children',
          placeholder: '父级'
        },
        propsSelectlist: [],
        propsSelectlist2: [
          {id: 0, parent: -1, name: '顶级'}
        ],
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
        temp: {},
        dialogFormVisible: false,
        dialogStatus: '',
        textMap: {
          update: '编辑',
          create: '添加',
        },
        rules: {
          name: [{required: true, message: '请输入名称', trigger: 'blur'}],
          sequence: [{ required: true, message: "请输入排序", trigger: "blur" }],
        },
        multipleSelection: [],
        treeProps: {
          children: 'children',
          label: 'name'
        },
        treeData: [],
        menuTypeOptions: [
          {key: 1, display_name: '模块'},
          {key: 2, display_name: '菜单'},
          {key: 3, display_name: '操作'}
        ],
        operateTypeOptions: [
          {key: 'none', display_name: '无'},
          {key: 'add', display_name: '新增'},
          {key: 'del', display_name: '删除'},
          {key: 'update', display_name: '编辑'},
          {key: 'view', display_name: '查看'},
        ],
        showOpera: false,
        allmean: [],
      }
    },
    computed: {
      optionDataSelectTree() {
        const cloneData = this.allmean
        return cloneData.filter(father => {
          const branchArr = cloneData.filter(child => father.id === child.parent)
          branchArr.length > 0 ? father.children = branchArr : ''
          return father.parent === this.allmean[0].parent
        })
      }
    },
    created() {
      this.getMenuButton()
      this.getList()
      this.getAllMean()
    },
    methods: {
      checkPermission() {
        this.permissionList.add = checkAuthAdd(this.operationList)
        this.permissionList.del = checkAuthDel(this.operationList)
        this.permissionList.view = checkAuthView(this.operationList)
        this.permissionList.update = checkAuthUpdate(this.operationList)
      },
      getMenuButton() {
        auth.requestMenuButton('menu').then(response => {
          this.operationList = response.results
        }).then(() => {
          this.checkPermission()
        })
      },
      getList() {
        this.listLoading = true
        menu.requestGet(this.listQuery).then(response => {
          this.list = response.results
          this.total = response.count
          this.listLoading = false
        })
      },
      getAllMean() {
        menu.requestGet().then(response => {
          this.allmean = response.results
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
      resetTemp() {
        this.temp = {
          name: '',
          code: '',
          curl: '',
          icon: 'list',
          sequence: '',
          type: 2,
          operate: 'none',
          status: true,
          hidden: false,
          memo: '',
          parent: 0
        }
      },
      handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogFormVisible = true
        this.loading = false
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      createData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            this.temp.parent = this.valueIdSelectTree2
            menu.requestPost(this.temp).then(response => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              this.getList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleUpdate(row) {
        this.temp = row
        this.dialogStatus = 'update'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.valueIdSelectTree2 = this.temp.parent
          this.$refs['dataForm'].clearValidate()
        })
      },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            this.temp.parent = this.valueIdSelectTree2
            menu.requestPut(this.temp.id, this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleDelete(row) {
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          menu.requestDelete(row.id).then(() => {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getList()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      },
      handleshowOpera(val) {
        if (val === 3) {
          this.showOpera = true
        } else {
          this.showOpera = false
          this.temp.operate = 'none'
        }
      },
      getSelectTreeValue(value, type) {
        if (type === 1) {
          this.valueIdSelectTree = value
          this.handleFilter()
        } else {
          this.valueIdSelectTree2 = value
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val
      },
      handleBatchDel() {
        if (this.multipleSelection.length === 0) {
          this.$message({
            message: '未选中任何行',
            type: 'warning',
            duration: 2000
          })
          return
        }
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const ids = this.multipleSelection.map(x => x.id)
          menu.requestBulkDelete(ids).then(response => {
            console.log(response.results)
            this.getList()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      }
    }
  }
</script>
