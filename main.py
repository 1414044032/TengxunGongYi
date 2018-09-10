# -*- coding: utf-8 -*-
import requests
import json
from openpyxl import Workbook
import urllib3
# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

wb = Workbook()
sheet = wb.active
sheet.title = "微信捐款"
sheet.append(['单号','时间','金额（不含配捐）','腾讯配捐','小红花配捐'])
header = {
'Host':'ssl.gongyi.qq.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Linux; Android 8.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044207 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x26070239) NetType/WIFI Language/zh_CN',
'Accept':'*/*',
'Referer':'https://ssl.gongyi.qq.com/user_center/donation.html',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
'Cookie':'cookie',
'Q-UA2':'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.7.2&TBSVC=43613&CO=BK&COVC=044207&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= FRD-AL10 &RL=1080*1792&OS=8.0.0&API=26',
'Q-GUID':'',
'Q-Auth':''
}
url = "抓包取到的https地址"
# session =requests.session()
# result = session.get(url, headers=header,verify=False)
all_result = []
for i in range(1,100):
    result = requests.get(url%str(i), headers=header, verify=False)
    x = str(result.text).find('(')
    # true data
    y = str(result.text)[x+1:-2]
    data = json.loads(y)
    all = data.get("info").get("data")
    i = 1
    if all:
        for one in all:
            print("当前第"+str(i)+"笔")
            i +=1
            oddnumber = one.get("transcode")
            url1 = "https://ssl.gongyi.qq.com/cgi-bin/gywcom_1899_thanks.fcgi?code=%s"%oddnumber
            result1 = requests.get(url1,headers=header, verify=False)
            print(result.text)
            data1 = json.loads(result1.text)
            tmm = data1.get("matching").get("tmm")/100
            rmm = data1.get("matching").get("rmm")/100
            createtime = one.get("dtime")
            money = one.get("money")/100
            line = [oddnumber,createtime,money,tmm,rmm]
            sheet.append(line)
            wb.save('weixin_donation.xlsx')
            all_result.append([oddnumber,createtime,money])
    else:
        break
print(all_result)
