# -*- coding:utf-8 -*- 
__author__ = 'll'


from datetime import datetime
from base64 import b64encode, b64decode
from base64 import decodebytes, encodebytes
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import json


class AliPay(object):
    def __init__(self, appid, app_notify_url, app_private_key_path, apiplay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.apiplay_public_key_path = apiplay_public_key_path
        self.app_private_key = None
        self.return_url = return_url

        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        with open(self.apiplay_public_key_path) as fp:
            self.aliplay_public_key = RSA.import_key(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_play(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PLAY"
        }

        biz_content.update(**kwargs)
        data = self.build_body("aliplay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charest": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.00",
            "biz_content": biz_content
        }

        if return_url is not None:
            data['notify_url'] = self.app_notify_url
            data['return_url'] = self.return_url

        return data


    def sign_data(self, data):
        data.pop('sign', None)
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode('utf-8'))
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k ,v in unsigned_items)
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)


        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(key, value) for key, value in data.items()])

    def sign(self, unsigned_string):
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        sign = encodebytes(signature).decode('utf-8').replace("\n", "")

        return sign

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
            unsigned_itmes = self.ordered_data(data)
            message = "&".join(u"{}={}".format(k,v) for k, v in unsigned_itmes)
            return self._verify(message, signature)

    def _verify(self, raw_content, signature):
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf-8"))
        if signer.verify(digest, decodebytes(signature.encode("utf-8"))):
            return True
        return False



if __name__ == '__main__':
    return_url = 'http://47.92.87.172:8000/?total_amount=100.00&timestamp=2017-08-15+23%3A53%3A34&sign=e9E9UE0AxR84NK8TP1CicX6aZL8VQj68ylugWGHnM79zA7BKTIuxxkf%2FvhdDYz4XOLzNf9pTJxTDt8tTAAx%2FfUAJln4WAeZbacf1Gp4IzodcqU%2FsIc4z93xlfIZ7OLBoWW0kpKQ8AdOxrWBMXZck%2F1cffy4Ya2dWOYM6Pcdpd94CLNRPlH6kFsMCJCbhqvyJTflxdpVQ9kpH%2B%2Fhpqrqvm678vLwM%2B29LgqsLq0lojFWLe5ZGS1iFBdKiQI6wZiisBff%2BdAKT9Wcao3XeBUGigzUmVyEoVIcWJBH0Q8KTwz6IRC0S74FtfDWTafplUHlL%2Fnf6j%2FQd1y6Wcr2A5Kl6BQ%3D%3D&trade_no=2017081521001004340200204115&sign_type=RSA2&auth_app_id=2016080600180695&charset=utf-8&seller_id=2088102170208070&method=alipay.trade.page.pay.return&app_id=2016080600180695&out_trade_no=20170202185&version=1.0'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]

    alipay = Alipay(
        appid="2016080600180695",
        app_notify_url="http://47.92.87.172:8000/alipay/return/",
        app_private_key_path="../trade/keys/private_2048.txt",
        alipay_public_key_path="../trade/keys/alipay_key_2048.txt",
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        return_url="http://47.92.87.172:8000/alipay/return/"
    )

    for key, value in query_items():
        processed_query[key] = value[0]
    print (alipay.verify(processed_query, ali_sign))


    url = alipay.direct_play(
        subject="测试订单2",
        out_trade_no="20170202sss",
        total_amount=100,
        return_url="http://47.92.87.172:8000/alipay/return/",
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    print (re_url)














