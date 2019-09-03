# -*- coding: utf-8 -*-

try:
    from unittest import mock
except:
    import mock

try:
    from importlib import reload
except:
    pass

import unittest

from django.conf import settings
from django.test import SimpleTestCase

import sendsms

if not settings.configured:
    settings.configure(
        SENDSMS_BACKEND='sendsms.backends.locmem.SmsBackend',
        ESENDEX_USERNAME='niwibe',
        ESENDEX_PASSWORD='123123',
        ESENDEX_ACCOUNT='123123',
        ESENDEX_SANDBOX=True,
        RQ_QUEUES={
            'default': {
                'URL': 'redis://localhost',
                'DEFAULT_TIMEOUT': 500,
            }
        },
        RQ_SENDSMS_BACKEND='sendsms.backends.locmem.SmsBackend',
        CELERY_SENDSMS_BACKEND='sendsms.backends.locmem.SmsBackend',
    )


class TestApi(unittest.TestCase):
    def test_send_simple_sms(self):
        from sendsms.message import SmsMessage
        obj = SmsMessage(body="test", from_phone='111111111', to=['222222222'])
        obj.send()

        self.assertEqual(len(sendsms.outbox), 1)

    def test_send_esendex_sandbox(self):
        from sendsms.message import SmsMessage
        from sendsms.api import get_connection

        connection = get_connection('sendsms.backends.esendex.SmsBackend')
        obj = SmsMessage(body="test", from_phone='111111111', to=['222222222'],
                         connection=connection)
        res = obj.send()
        self.assertEqual(res, 1)


class RQBackendTest(SimpleTestCase):

    @mock.patch('sendsms.backends.rq.send_messages')
    def test_should_queue_sms(self, send_messages_mock):
        from sendsms.message import SmsMessage

        with self.settings(SENDSMS_BACKEND='sendsms.backends.rq.SmsBackend'):
            message = SmsMessage(
                body='Hello!',
                from_phone='29290',
                to=['+639123456789']
            )
            message.send()

        send_messages_mock.delay.assert_called_with([message])

    @mock.patch('sendsms.backends.twiliorest.SmsBackend')
    @mock.patch('sendsms.backends.locmem.SmsBackend')
    def test_send_message_should_use_configured_backend(self, LocmemBackend,
                                                        TwilioBackend):
        from sendsms.message import SmsMessage

        with self.settings(SENDSMS_BACKEND='sendsms.backends.rq.SmsBackend'):
            with self.settings(RQ_SENDSMS_BACKEND='sendsms.backends.twiliorest.SmsBackend'):  # noqa
                from sendsms.backends import rq

                backend = TwilioBackend()
                message = SmsMessage(
                    body='Hello!',
                    from_phone='29290',
                    to=['+639123456789']
                )
                rq.send_messages([message])
                backend.send_messages.assert_called_once_with([message])

            with self.settings(RQ_SENDSMS_BACKEND='sendsms.backends.locmem.SmsBackend'):  # noqa
                reload(rq)

                backend = LocmemBackend()
                message = SmsMessage(
                    body='Hello!',
                    from_phone='29290',
                    to=['+639123456789']
                )
                rq.send_messages([message])
                backend.send_messages.assert_called_once_with([message])


class CeleryBackendTest(SimpleTestCase):

    @mock.patch('sendsms.backends.celery.send_messages')
    def test_should_queue_sms(self, send_messages_mock):
        from sendsms.message import SmsMessage

        with self.settings(SENDSMS_BACKEND='sendsms.backends.celery.SmsBackend'):
            message = SmsMessage(
                body='Hello!',
                from_phone='29290',
                to=['+639123456789']
            )
            message.send()

        send_messages_mock.delay.assert_called_with([message])

    @mock.patch('sendsms.backends.twiliorest.SmsBackend')
    @mock.patch('sendsms.backends.locmem.SmsBackend')
    def test_send_message_should_use_configured_backend(self, LocmemBackend,
                                                        TwilioBackend):
        from sendsms.message import SmsMessage

        with self.settings(SENDSMS_BACKEND='sendsms.backends.celery.SmsBackend'):
            with self.settings(CELERY_SENDSMS_BACKEND='sendsms.backends.twiliorest.SmsBackend'):  # noqa
                from sendsms.backends import celery

                backend = TwilioBackend()
                message = SmsMessage(
                    body='Hello!',
                    from_phone='29290',
                    to=['+639123456789']
                )
                celery.send_messages([message])
                backend.send_messages.assert_called_once_with([message])

            with self.settings(CELERY_SENDSMS_BACKEND='sendsms.backends.locmem.SmsBackend'):  # noqa
                reload(celery)

                backend = LocmemBackend()
                message = SmsMessage(
                    body='Hello!',
                    from_phone='29290',
                    to=['+639123456789']
                )
                celery.send_messages([message])
                backend.send_messages.assert_called_once_with([message])


class YuntongxunBackendTest(SimpleTestCase):

    def test_send_message(self):
        from sendsms.message import SmsMessage
        with self.settings(SENDSMS_BACKEND='sendsms.backends.yuntongxun.SmsBackend'):
            body = {
                'template_id': '185733',
                'datas': ['潘运来', '20', '迪康基因']
            }
            obj = SmsMessage(body=body, from_phone='', to=['17798553635'])
            obj.send()


class AliyunBackendTest(SimpleTestCase):

    def test_send_message(self):
        from sendsms.message import SmsMessage
        import json
        with self.settings(SENDSMS_BACKEND='sendsms.backends.aliyun.SmsBackend',
                           ALIYUN_ACCESS_ID='LTAI4Fs5mnQwbw1seSDFFSTc',
                           ALIYUN_ACCESS_SECRET='0pSY02mWdcZqYZCuBHQQJy90AxEhFV',
                           ALIYUN_REGION=''):
            body = {
                'template_id': 'SMS_58960014',
                'datas': {"code": "1234", "product": "测试产品"},
                'sign_name': '身份验证a'
            }
            obj = SmsMessage(body=body, from_phone='', to=['17368588130'])
            res = obj.send()
            json_res = json.loads(res)
            print(json_res)
            self.assertEqual(json_res['Message'], 'OK')


if __name__ == '__main__':
    unittest.main(verbosity=2)
