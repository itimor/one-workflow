import { auth } from '@/api/all'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const state = {
  token: getToken(),
  username: '',
  user_id: '',
  avatar: '',
  roles: [],
  ip: ''
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USER_ID: (state, user_id) => {
    state.user_id = user_id
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_IP: (state, ip) => {
    state.ip = ip
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      auth.login({ username: username.trim(), password: password }).then(response => {
        const data = response.results
        commit('SET_TOKEN', data.token)
        setToken(data.token)
        resolve()
      }).catch(error => {
        console.log(error)
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      auth.getInfo(state.token).then(response => {
        const data = response.results
        if (!data) {
          reject('Verification failed, please Login again.')
        }
        const { username, avatar, user_id, ip } = data

        // roles must be a non-empty array
        // if (!roles || roles.length <= 0) {
        // reject('getInfo: roles must be a non-null array!')
        // }
        const roles = ['admin']
        commit('SET_ROLES', roles)
        commit('SET_USERNAME', username)
        commit('SET_AVATAR', avatar)
        commit('SET_USER_ID', user_id)
        commit('SET_IP', ip)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        removeToken()
        resetRouter()
        resolve()
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}