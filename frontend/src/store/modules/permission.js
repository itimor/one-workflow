import { asyncRoutes, constantRoutes } from '@/router'
// import { getMenus } from '@/api/user'
/* Layout */
import Layout from '@/layout'
// import { getToken } from '@/utils/auth'
/**
 * 通过meta.role判断是否与当前用户权限匹配
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * 递归过滤异步路由表，返回符合用户角色权限的路由表
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

// 在这里定义state 状态管理
const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes2({ commit }, roles) {
    return new Promise(resolve => {
      let accessedRoutes
      if (roles.includes('admin')) {
        // 如果是管理员则加载所有路由
        accessedRoutes = asyncRoutes
      } else {
        // 如果不是总管理员则进行过滤
        // accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
        return
        /**
        // 从服务端请求菜单列表数据
        getMenus(state.username).then(response => {
          const { code, menus } = response // 这种形式可以直接接收 {code:2000,data:"ok"}
          console.log(code)
          console.log(menus)
          // const { roles, name, avatar, introduction } = data
          // 处理路由、菜单
          // const asyncRouterMap_copy = []
          // accessedRoutes = asyncRouterMap_copy
        }).catch(error => {
          console.log(error)
          return
        })
        **/
        // end
      }
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  },
  generateRoutes({ commit }, data) {
    return new Promise(resolve => {
      const accessedRouters = convertRouter(data)
      commit('SET_ROUTES', accessedRouters)
      resolve(accessedRouters)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

/**
 *将后台的路由表进行格式化
 * @param {*} asyncRouterMap
 */
function convertRouter(asyncRouterMap) {
  const accessedRouters = []
  if (asyncRouterMap) {
    asyncRouterMap.forEach(item => {
      var isParent = false
      if (item.children) {
        isParent = true
      }
      var parent = generateRouter(item, isParent)
      // console.log('003')
      // console.log(parent)
      var children = []
      if (item.children) {
        // console.log('004')
        item.children.forEach(child => {
          // 下一级
          var children2 = []
          if (child.children) {
            child.children.forEach(child2 => {
              children2.push(generateRouter(child2, false))
            })
          }
          var parent2 = generateRouter(child, false)
          parent2.children = children2
          children.push(parent2)
          // 下一级 end
          // children.push(generateRouter(child, false))
        })
      }
      parent.children = children
      accessedRouters.push(parent)
    })
  }
  accessedRouters.push({ path: '*', redirect: '/404', hidden: true })
  return accessedRouters
}

// 对component的处理
function generateRouter(item, isParent) {
  var component = Layout // 多层嵌套时只能有一个Layout
  if (isParent !== true) {
    component = componentsMap[item.component]
  }
  var router = {
    path: item.path,
    name: item.name,
    meta: item.meta,
    noCache: item.no_cache,
    activeMenu: item.active_menu,
    hidden: item.hidden,
    // component: isParent ? Layout : () => import(item.component) // 这个不可以
    // component: isParent ? Layout : componentsMap[item.component]
    component: component
  }
  if (isParent !== true) {
    // router.meta = item.meta
    // router.name = item.name
  }
  // router.meta.noCache = true
  return router
}

// componentsMap 需要在事先定义好
export const componentsMap = {
  // sys
  menu: () => import('@/views/sys/menu'), // 菜单
  user: () => import('@/views/sys/user'), // 用户
  group: () => import('@/views/sys/group'), // 用户组
  role: () => import('@/views/sys/role'), // 角色
  icon: () => import('@/views/icons/index'), // 图标管理

  // tool
  audit: () => import('@/views/tool/audit'), // 审计日志
  test: () => import('@/views/tool/test'), // test

  // workflow
  wfset: () => import('@/views/workflow/wfset'), // 工作流设计
  wfconf: () => import('@/views/workflow/wfconf'), // 工作流配置

  // tickets
  myticket: () => import('@/views/workflow/myticket'), // 我的工单
}
