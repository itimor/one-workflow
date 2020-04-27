import { isNumber } from 'util'

let Validators = {}

Validators.datetime = function (rule, value, callback) {
  let now = new Date()
  let expire = Date.parse(value)
  if (!value) {
    callback(new Error('不能为空，且时间必须为未来时间'))
  }
  if (now > expire) {
    callback(new Error('过期时间必须为未来时间'))
  } else {
    callback()
  }
}

Validators.string = function (rule, value, callback) {
  if (value !== '') {
    callback()
  } else {
    callback(new Error('不能为空'))
  }
}

Validators.number = function (rule, value, callback) {
  if (isNumber(value)) {
    callback()
  } else {
    callback(new Error('必须为数字'))
  }
}

export default Validators
