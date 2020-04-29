# -*- coding: utf-8 -*-
# author: timor

from notices.serializers import *
from common.views import ModelViewSet, JsonResponse
from common import status
from collections import OrderedDict
from rest_framework.decorators import action


class NoticeViewSet(ModelViewSet):
    queryset = MailBot.objects.all()
    serializer_class = MailBotSerializer

    # send
    @action(methods=['post'], url_path='send', detail=False)
    def send(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        data = {'code': 20000, 'msg': 'null'}
        type = request.GET['type']
        if type == 'mail':
            import smtplib
            from email.mime.text import MIMEText

            bot_name = request.GET['bot_name']
            bot_obj = MailBot.objects.get(name=bot_name)
            mail_user = '{}@{}'.format(bot_obj.user, bot_obj.host)

            tos = bot_obj.to
            content = request.data.get('content', 'Hello Pornhub')
            message = MIMEText(content, 'plain', 'utf-8')
            message['Subject'] = "{}".format(request.form['subject'])
            message['From'] = mail_user
            message['To'] = tos[0:]

            try:
                smtpObj = smtplib.SMTP_SSL(bot_obj.host)
                smtpObj.login(mail_user, bot_obj.pasword)
                smtpObj.sendmail(mail_user, tos, message.as_string())
                smtpObj.quit()
            except smtplib.SMTPException as e:
                print(e)
                data['msg'] = 'error'
        elif type == 'telegram':
            import telegram
            bot_name = request.GET['bot_name']
            content = request.data.get('content', 'Hello Pornhub')
            bot_obj = TelegramBot.objects.get(name=bot_name)
            token = '{}:{}'.format(bot_obj.uid, bot_obj.token)
            bot = telegram.Bot(token=token)
            data['msg'] = bot.send_message(chat_id=bot_obj.chat_id, text=content)
        else:
            pass

        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))


class MailBotViewSet(ModelViewSet):
    queryset = MailBot.objects.all()
    serializer_class = MailBotSerializer
    search_fields = ['name']
    filter_fields = ['type', 'id', 'name']
    ordering_fields = ['name']


class TelegramBotViewSet(ModelViewSet):
    queryset = TelegramBot.objects.all()
    serializer_class = TelegramBotSerializer
    search_fields = ['name']
    filter_fields = ['type', 'id', 'name']
    ordering_fields = ['name']
