import { request } from '@/api/service'

export const urlPrefix = '/api/system/system_config/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

export function saveContent (id, data) {
  return request({
    url: urlPrefix + 'save_content/',
    method: 'put',
    data: data
  })
}

export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

/*
获取所有的model及字段信息
 */
export function GetAssociationTable () {
  return request({
    url: urlPrefix + 'get_association_table/',
    method: 'get',
    params: { }
  })
}


export function GetDetailById (id) {
  return request({
    url: urlPrefix + 'get_detail_by_id/',
    method: 'get',
    params: {id}
  })
}

export function Test (data_path) {
  return request({
    url: urlPrefix + 'test/',
    method: 'get',
    params: {data_path}
  })
}


export function GetDataContent (data_path) {
  return request({
    url: urlPrefix + 'get_data_content/',
    method: 'get',
    params: {data_path}
  })
}


