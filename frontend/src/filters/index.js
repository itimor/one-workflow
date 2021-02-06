// set function parseTime,formatTime to filter
export { parseTime, formatTime } from '@/utils'

function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/* 数字 格式化*/
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

// 格式化时间
export function parseDate(datestr) {
  if (datestr !== undefined) {
    const date = datestr.slice(0, 10)
    const time = datestr.slice(11, 19)
    return date + ' ' + time
  }
}

export function diffDate(date) {
  const d1 = new Date()
  const d2 = new Date(date)
  return Math.round(parseInt(d2 - d1) / 1000 / 60 / 60 / 24)
}

// 菜单
export function menuTypeFilter(val) {
  const Map = {
    1: '模块',
    2: '菜单',
    3: '操作'
  }
  return Map[val]
}

// 按钮
export function operateTypeFilter(val) {
  const Map = {
    'none': '无',
    'add': '新增',
    'del': '删除',
    'update': '编辑',
    'view': '查看',
  }
  return Map[val]
}

// 字段类型
export function FieldTypeFilter(val) {
  const Map = {
    1: '字符串',
    2: '整型',
    3: '浮点型',
    4: '布尔',
    5: '日期',
    6: '日期时间',
    7: '范围日期',
    8: '文本域',
    9: '单选框',
    10: '下拉列表',
    11: '用户名',
    12: '多选框',
    13: '多选下拉',
    14: '多选用户名',
  }
  return Map[val]
}

// 状态类型
export function StateTypeFilter(val) {
  const Map = {
    0: '普通状态',
    1: '初始状态',
    2: '结束状态',
  }
  return Map[val]
}

// 流转类型
export function TransitionTypeFilter(val) {
  const Map = {
    0: '常规流转',
    1: '定时器流转',
  }
  return Map[val]
}

// 属性类型
export function AttributeTypeFilter(val) {
  const Map = {
    0: '草稿',
    1: '待审',
    2: '驳回',
    3: '撤销',
    4: '结束',
    5: '已关闭',
  }
  return Map[val]
}


// 流转名称
export function TransitionNameFilter(val) {
  const Map = {
    0: '保存',
    1: '转交下一步',
    2: '驳回',
    3: '撤销',
    4: '关闭',
  }
  return Map[val]
}

// 取第一个字母并大写
export function AvatarFilter(val) {
  return val.substr(0, 1).toUpperCase()
}
