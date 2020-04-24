# -*- coding: utf-8 -*-
# author: itimor

# 登录skype
from skpy import Skype

# skype账号
SK_ACOUNT = {
    'sk_user': 'itimor@126.com',
    'sk_pass': 'xxx'
}
SK = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])


def skype_bot(user, content):
    chat = SK.chats[user]
    chat.sendMsg(content)


if __name__ == '__main__':
    skypeid = 'live:dafaricky123'
    user = '8:' + skypeid  # skypeid 前面需要加 8
    skype_bot(user, "hello,gay,你个逗比，不加好友，发你妹的消息啊")
