import request from '@/utils/request'

export default class Request {
  constructor(apiurl) {
    this.apiurl = apiurl;
  }

  requestPost(data) {
    return request({
      url: this.apiurl,
      method: 'post',
      data
    })
  }

  requestDelete(id) {
    return request({
      url: this.apiurl + id + '/',
      method: 'delete'
    })
  }

  requestPut(id, data) {
    return request({
      url: this.apiurl + id + '/',
      method: 'put',
      data
    })
  }

  requestGet(query) {
    return request({
      url: this.apiurl,
      method: 'get',
      params: query
    })
  }

  requestBulkPost(data) {
    return request({
      url: this.apiurl + 'bulk_create/',
      method: 'post',
      data
    })
  }

  requestBulkPut(data) {
    return request({
      url: this.apiurl + 'bulk_update/',
      method: 'put',
      data
    })
  }

  requestBulkDelete(data) {
    return request({
      url: this.apiurl + 'bulk_delete/',
      method: 'delete',
      data
    })
  }
}