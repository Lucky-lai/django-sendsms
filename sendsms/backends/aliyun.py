from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from sendsms.backends.base import BaseSmsBackend
from django.conf import settings

ACCESS_ID = getattr(settings, 'ALIYUN_ACCESS_ID')
ACCESS_SECRET = getattr(settings, 'ALIYUN_ACCESS_SECRET')
REGION = getattr(settings, 'ALIYUN_REGION')


class SmsBackend(BaseSmsBackend):

    def send_messages(self, messages):
        for message in messages:
            to = ','.join(message.to)
            template_id = message.body.get('template_id')
            datas = message.body.get('datas')
            sign_name = message.body.get('sign_name')
            return self.send_template_sms(to=to, datas=datas, template_id=template_id, sign_name=sign_name)

    def send_template_sms(self, to, template_id, datas, sign_name):
        client = AcsClient(ACCESS_ID, ACCESS_SECRET, REGION)

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', REGION)
        request.add_query_param('PhoneNumbers', to)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_id)
        request.add_query_param('TemplateParam', datas)

        response = client.do_action_with_exception(request)
        return response
