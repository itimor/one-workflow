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
export const workflowtype = new Request('/workflow/workflowtype/')
export const workflow = new Request('/workflow/workflow/')
export const state = new Request('/workflow/state/')
export const transition = new Request('/workflow/transition/')
export const customfield = new Request('/workflow/customfield/')

// tickets
export const ticket = new Request('/ticket/ticket/')
export const ticketflowlog = new Request('/ticket/ticketflowlog/')
export const ticketcustomfield = new Request('/ticket/ticketcustomfield/')
export const ticketuser = new Request('/ticket/ticketuser/')