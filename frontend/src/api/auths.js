import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/sys/auth/jwt-token-auth/',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/sys/auth/getuserinfo/',
    method: 'get'
  })
}

export function requestMenuButton(menucode) {
  return request({
    url: '/sys/auth/getmenubutons/',
    method: 'get',
    params: {menucode}
  })
}

export function changepwd(data) {
  return request({
    url: '/sys/auth/changepwd/',
    method: 'post',
    data
  })
}
