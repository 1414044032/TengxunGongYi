# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
import json
import time
import re

# 编写正则
regex_qrcode = "window\.QRLogin\.uuid.*?\"(.*?)\""
regex_status_code = "window.code=(\d).*"
regex_login = "window\.redirect_uri.*?\"(.*?)\""
get_qrcode_url = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_=1547629305614"
qrcode_path = "D:\\img2.jpg"
check_login_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r=-2134589005&_={2}"


class WX:
    def __init__(self):
        pass

    # 获取验证码标签
    def _get_qrcode(self):
        try:
            response = requests.get(get_qrcode_url)
            qr_login = re.findall(regex_qrcode, response.text)[0]
            return qr_login
        except Exception as e:
            print(e)
            return None

    # 保存验证码
    def _save_qrcode(self):
        qr_login =  self._get_qrcode()
        if qr_login:
            try:
                save_qrcode_url = urljoin("https://login.weixin.qq.com/qrcode/", qr_login)
                r = requests.get(save_qrcode_url, stream=True)
                # 保存登录验证码
                with open(qrcode_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 4):
                        if chunk:
                            f.write(chunk)
                print("二维码保存完成")
                return qr_login
            except Exception as e:
                print(e)
                return None

    def check_login(self):
        qr_login = self._save_qrcode()
        try:
            redirect_uri = None
            while redirect_uri is None:
                redirect_uri = self._send_request(qr_login)
            return redirect_uri
        except Exception as e:
            print(e)
            return None

    def _send_request(self, qr_login):
        try:
            check_login_url_true = check_login_url.format(qr_login, "0", str(int(time.time()) * 1000))
            # 三个状态 201 408 200
            response31 = requests.get(check_login_url_true)
            redirect_uri = re.findall(regex_login, response31.text, re.M)[0]
            cookie = response31.cookies.get_dict()
            print(cookie)
            return redirect_uri
        except Exception as e:
            return None

if __name__ =="__main__":
    print(WX().check_login())
