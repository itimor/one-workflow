import Request from '@/api/common'

// auth
import * as auths from '@/api/auths'
export const auth = auths

// systems
export const user = new Request('/sys/user/')
export const group = new Request('/sys/group/')
export const role = new Request('/sys/role/')
export const menu = new Request('/sys/menu/')
export const perm = new Request('/sys/perm/')

// tools
export const audit = new Request('/tool/audit/')
export const simple = new Request('/tool/simple/')

// workflows
export const workflow = new Request('/workflow/workflow/')
export const state = new Request('/workflow/state/')
export const transition = new Request('/workflow/transition/')
export const customfield = new Request('/workflow/customfield/')

// tickets
export const tickiet = new Request('/tickiet/tickiet/')
export const ticketflowlog = new Request('/tickiet/ticketflowlog/')
export const ticketcustomfield = new Request('/tickiet/ticketcustomfield/')
export const ticketuser = new Request('/tickiet/ticketuser/')