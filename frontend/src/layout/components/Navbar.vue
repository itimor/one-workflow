<template>
  <div class="navbar">
    <hamburger
      id="hamburger-container"
      :is-active="sidebar.opened"
      class="hamburger-container"
      @toggleClick="toggleSideBar"
    />

    <breadcrumb id="breadcrumb-container" class="breadcrumb-container"/>

    <div class="right-menu">
      <template v-if="device !== 'mobile'">
        <div class="right-menu-item">
          <a class="ip">{{ip}}</a>
          <a class="date">{{cur_date}}</a>
        </div>

        <search id="header-search" class="right-menu-item"/>

        <screenfull id="screenfull" class="right-menu-item hover-effect"/>

        <lang-select class="right-menu-item hover-effect"/>
      </template>

      <el-dropdown
        class="avatar-container right-menu-item hover-effect"
        trigger="click"
      >
        <div class="avatar-wrapper">
          <el-avatar :src="avatar"/>
        </div>
        <el-dropdown-menu slot="dropdown">
          <router-link to="/">
            <el-dropdown-item>
              {{ "首页" }}
            </el-dropdown-item>
          </router-link>
          <el-dropdown-item disabled>
            <span style="display:block;" @click="handleEditPwd">{{
              "个人中心"
            }}</span>
          </el-dropdown-item>
          <el-dropdown-item divided>
            <span style="display:block;" @click="logout">{{ "退出登录" }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
    <el-dialog title="修改密码" :visible.sync="dialogFormVisible" width="30%">
      <el-form
        ref="dataForm"
        v-loading="loading"
        element-loading-text="正在执行"
        element-loading-background="rgba(255,255,255,0.7)"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="120px"
        style="width: 400px; margin-left:50px;"
      >
        <!--<el-form-item label="原密码" prop="old_password">-->
        <!--<el-input-->
        <!--v-model="temp.old_password"-->
        <!--show-password-->
        <!--minlength="6"-->
        <!--maxlength="20"-->
        <!--/>-->
        <!--</el-form-item>-->
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="temp.new_password1"
            placeholder="6-20位"
            show-password
            minlength="6"
            maxlength="20"
          />
        </el-form-item>
        <el-form-item label="再次输入新密码" prop="new_password_again">
          <el-input
            v-model="temp.new_password2"
            placeholder="6-20位"
            show-password
            minlength="6"
            maxlength="20"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="editPwd()">
          {{ "确定" }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import Breadcrumb from '@/components/Breadcrumb'
  import Hamburger from '@/components/Hamburger'
  import Screenfull from '@/components/Screenfull'
  import LangSelect from '@/components/LangSelect'
  import Search from '@/components/HeaderSearch'
  import {auth} from '@/api/all'

  export default {
    components: {
      Breadcrumb,
      Hamburger,
      Screenfull,
      LangSelect,
      Search
    },
    data() {
      return {
        dialogVisible: false,
        dialogFormVisible: false,
        loading: true,
        cur_date: '',
        temp: {
          old_password: '',
          new_password1: '',
          new_password2: ''
        },
        rules: {
          old_password: [{required: true, message: '请输入旧密码', trigger: 'blur'}],
          new_password1: [{min: 6, max: 20, required: true, message: '长度在 8 到 20 个字符', trigger: 'blur'}],
          new_password2: [{min: 6, max: 20, required: true, message: '长度在 8 到 20 个字符', trigger: 'blur'}]
        }
      }
    },
    computed: {
      ...mapGetters([
        'sidebar',
        'name',
        'avatar',
        'ip',
        'device'
      ])
    },
    methods: {
      toggleSideBar() {
        this.$store.dispatch('app/toggleSideBar')
      },
      async logout() {
        await this.$store.dispatch('user/logout')
        this.$router.push(`/login?redirect=${this.$route.fullPath}`)
      },
      resetTemp() {
        this.temp = {
          old_password: '',
          new_password: '',
          new_password_again: ''
        }
      },
      handleEditPwd() {
        this.resetTemp()
        this.dialogFormVisible = true
        this.loading = false
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      editPwd() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            if (this.temp.new_password !== this.temp.new_password_again) {
              this.$message.error('两次输入的密码不一致')
              return
            }
            this.loading = true
            auth.changepwd(this.temp).then(response => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '修改成功',
                type: 'success',
                duration: 2000
              })
            }).catch(() => {
              this.loading = false
            })
          }
        })
      }
    },
    mounted() {
      var _this = this; //声明一个变量指向vue实例this,保证作用域一致
      this.timer = setInterval(function () {
        _this.cur_date = (new Date()).toLocaleString();//修改数据date
      }, 1000);
    }
  }
</script>

<style lang="scss" scoped>
  .navbar {
    height: 50px;
    overflow: hidden;
    position: relative;
    background: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

    .hamburger-container {
      line-height: 46px;
      height: 100%;
      float: left;
      cursor: pointer;
      transition: background 0.3s;
      -webkit-tap-highlight-color: transparent;

      &:hover {
        background: rgba(0, 0, 0, 0.025);
      }
    }

    .breadcrumb-container {
      float: left;
    }

    .errLog-container {
      display: inline-block;
      vertical-align: top;
    }

    .right-menu {
      float: right;
      height: 100%;
      line-height: 50px;

      &:focus {
        outline: none;
      }

      .right-menu-item {
        display: inline-block;
        padding: 0 8px;
        height: 100%;
        font-size: 18px;
        color: #5a5e66;
        vertical-align: text-bottom;

        .ip {
          color: #39b3d1;
        }

        .date {
          color: #d39011;
        }

        &.hover-effect {
          cursor: pointer;
          transition: background 0.3s;

          &:hover {
            background: rgba(0, 0, 0, 0.025);
          }
        }
      }

      .avatar-container {
        margin-right: 20px;

        .avatar-wrapper {
          margin-top: 5px;
          position: relative;

          .user-avatar {
            cursor: pointer;
            width: 40px;
            height: 40px;
            border-radius: 50%;
          }

          .el-icon-caret-bottom {
            cursor: pointer;
            position: absolute;
            right: -20px;
            top: 25px;
            font-size: 12px;
          }
        }
      }
    }
  }
</style>
