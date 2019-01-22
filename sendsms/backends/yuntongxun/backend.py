from sendsms.backends.base import BaseSmsBackend
from .CCPRestSDK import REST

# 主帐号
ACCOUNT_SID = '8aaf0708559f32dd0155b3b6ce8a0bee'
# 主帐号Token
ACCOUNT_TOKEN = 'aceeb185e3894797ad55f6024f6c3992'
# 应用Id
APP_ID = '8aaf0708582eefe901584379904d0f18'
# 请求地址，格式如下，不需要写http://
SERVER_IP = 'app.cloopen.com'
# 请求端口
SERVER_PORT = '8883'
# REST版本号
SOFT_VERSION = '2013-12-26'


class SmsBackend(BaseSmsBackend):
    def __init__(self, fail_silently=False):
        super().__init__(fail_silently=fail_silently)
        self.rest = REST(ServerIP=SERVER_IP, ServerPort=SERVER_PORT, SoftVersion=SOFT_VERSION)
        self.rest.setAccount(AccountSid=ACCOUNT_SID, AccountToken=ACCOUNT_TOKEN)
        self.rest.setAppId(AppId=APP_ID)

    def send_messages(self, messages):
        for message in messages:
            to = ','.join(message.to)
            template_id = message.body.get('template_id')
            datas = message.body.get('datas')
            return self.send_template_sms(to=to, datas=datas, temp_id=template_id)

    def send_template_sms(self, to, datas, temp_id):
        try:
            # 调用云通讯的工具rest发送短信
            result = self.rest.sendTemplateSMS(to, datas, temp_id)  # 手机号码,内容数据,模板Id

        except Exception as error:
            raise error

        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送成功
            return True
        else:
            # 发送失败
            raise Exception(result)
