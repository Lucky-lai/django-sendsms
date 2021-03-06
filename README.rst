==============
django-sendsms
==============

.. image:: https://coveralls.io/repos/github/stefanfoulis/django-sendsms/badge.svg?branch=master
    :target: https://coveralls.io/github/stefanfoulis/django-sendsms?branch=master

.. image:: https://travis-ci.org/stefanfoulis/django-sendsms.svg?branch=master
    :target: https://travis-ci.org/stefanfoulis/django-sendsms

.. image:: https://badge.fury.io/py/django-sendsms.svg
    :target: https://badge.fury.io/py/django-sendsms

A simple api to send SMS messages with django. The api is structured the same way as djangos own email api.

Installation
============

::

    pip install django-sendsms

Configure the ``SENDSMS_BACKEND`` (defaults to ``'sendsms.backends.console.SmsBackend'``)::

    SENDSMS_BACKEND = 'myapp.mysmsbackend.SmsBackend'


Basic usage
===========

Sending SMSs is like sending emails::

    from sendsms import api
    api.send_sms(body='I can haz txt', from_phone='+41791111111', to=['+41791234567'])

you can also make instances of ``SmsMessage``::

    from sendsms.message import SmsMessage
    message = SmsMessage(body='lolcats make me hungry', from_phone='+41791111111', to=['+41791234567'])
    message.send()


Custom backends
===============

Creating custom ``SmsBackend`` s::

    from sendsms.backends.base import BaseSmsBackend
    from some.sms.delivery.api

    class AwesomeSmsBackend(BaseSmsBackend):
        def send_messages(self, messages):
            for message in messages:
                for to in message.to:
                    try:
                        some.sms.delivery.api.send(
                            message=message.body,
                            from_phone=message.from_phone,
                            to_phone=to,
                            flashing=message.flash
                        )
                    except:
                        if not self.fail_silently:
                            raise

Then all you need to do is reference your backend in the ``SENDSMS_BACKEND`` setting.

云通信短信服务
===============

create yuntongxun config::

    SENDSMS_BACKEND = 'sendsms.backends.yuntongxun.SmsBackend'
    YUNTONGXUN_ACCOUNT_SID = ''
    YUNTONGXUN_ACCOUNT_TOKEN = ''
    YUNTONGXUN_APP_ID = ''


    from sendsms import api

    body = {
        'template_id': '<template id>',

        'datas': ['<data1>', '<data2>', '<data3>']
    }

    api.send_sms(body=body, from_phone='', to=['+860123456789'])

阿里云短信服务
===============
create aliyun config::

    SENDSMS_BACKEND = 'sendsms.backends.aliyun.SmsBackend'
    ALIYUN_ACCESS_ID = ''
    ALIYUN_ACCESS_SECRET = ''
    ALIYUN_REGION = ''


    from sendsms import api

    body = {
        'template_id': '<template id>',
        'datas': {"code":"123"}
        'sign_name':'<sign_name>'
    }

    api.send_sms(body=body, from_phone='', to=['+860123456789'])


Running tests
===============

python setup.py test
