#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import re
import random
import time
import xlsxwriter

# 关键词 peminjaman ojk
keyword1 = 'peminjaman'
keyword4 = 'pinjaman'
keyword2 = 'Biaya penanganan'
keyword3 = 'OJK'
kw5 = 'RP'
kw6 = 'POJK'
# 访问每个gp 匹配关键词1 2  如果匹配则添加进列表 再匹配是否有3 如果有3则标记

def get_random_time():
    return random.uniform(5.00, 10.00)

def request_gp(url):
    print('start request')
    time.sleep(get_random_time())
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'cache-control':' max-age=0',
        "Connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded",
        "Cookie": "HSID=AFGc8HWqaU2lkStgJ; SSID=AO1NHWPiuu3Cw0LrL; APISID=iQlbrqJ7BhDzC1WZ/AjsMDHPr9cZrFvZOH; SAPISID=r0JQmzI-Ob1Dl77d/ACiZJ-5MYu6BX7NYr; CONSENT=YES+US.zh-CN+20161218-19-0; _ga=GA1.3.1006787421.1560418826; OTZ=4968580_24_24__24_; ANID=AHWqTUnTyhyGCYb0mGardaKqk1ChaFR5gOa_3zEd0sdMhkclLxOiNhOvu65-9yvT; _gid=GA1.3.1983113498.1562816412; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=pspensong@gmail.com; SID=mAcNrdT-n7bAkpxxppMCVRWy63EmbTnGNp3IQvGuqKDo7vDufLcXzVQgT8_5TcrZy1E4LQ.; 1P_JAR=2019-7-13-3; NID=187=QmZgBbfHvKcwKznocS5i2rLI2Kug-T5FyK6vpqNz79gPeTHRJ-V_06y6m9NKhUquvolOP-2sFHNupGW-qd1ZHiuckVRG7vH5WbjGET8HsBE6lY7UcM2BTBv5U-1B668OAuv2dXLoyetU_0qs5olIoLQxh5WZdF2lO5HamXGUINtIS8V0tAPIELMRkWzD_knfq26NM2WK37QjjtvhaTGndwWkrqhbVWAx_k7zYRE2ktBZ4XPsaDbiWUy8o6ydy4BHa2KVePGbutuU3XanqKMpl6o-YAiM9Oy5eAyUus0TIiEgp0lEtWmmb1dPR9yrkJ4WFt0mxH0DLcImnswR2O-wE4MOl-GChp5hPvTAH1h0; SIDCC=AN0-TYsnuIGFwq2U4goRAMXHNfHvS7txOzq1uAEriWlzvztv6DoRNrY5XAB7O72irGsCm_HkiQY",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "x-client-data": "CJS2yQEIpbbJAQjBtskBCNG3yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoBCIKrygE="
    }
    response = requests.get(url, headers)
    print('end request')
    content = response.text
    return match_content(content)


# 提取gp的描述内容 匹配是否存在ojk
def match_content(content):
    p = "(<div jsname=\"sngebd\">)(.*)(</div>)"
    g = re.search(p, content)
    print(g)
    if g is not None:
        des = g.group(2)
        if des.__contains__(keyword1) or des.__contains__(keyword2):
            if des.__contains__(keyword3):
                return 2
            else:
                return 1
        else:
            return 0


def write_file(data):
    print('start write_file')
    with open('result.txt', 'a') as f:  # 设置文件对象
        for str in data:
            f.writelines(str)  # 将字符串写入文件中
    f.close()
    print('end write_file')


def start():
    gp_list = []
    f = open("C:\\test.txt", "r+")
    json_str = json.loads(f.read())
    rows = json_str.get('table').get('rows')
    patter = r"(.*)(app/)(.*)(/)details/"
    count = 0
    for item in rows:
        if count > 5:
            break
        count = count + 1
        print(item)
        gp_item = []
        if item[1] is not None:
            gp_item.append(str(item[1][0].get('name')))
            # gp链接需要转一下 https://play.google.com/store/apps/details?id=id.saklff.yoyowallet.axcjgajs
            # /apps/google-play/app/com.cimbniaga.digipub/details/
            gp_item.append('https://play.google.com/store/apps/details?id=' + re.match(patter, str(item[1][0].get('url'))).group(3))
            result = request_gp(gp_item[1])
            if result is 0:
                continue
            elif result is 2:
                gp_item.append('true')
            else:
                gp_item.append('false')
        else:
            gp_item.append('')
        if len(item[6]) > 0:
            gp_item.append(str(item[6][0]))
        else:
            gp_item.append('')
        if item[8] is not None:
            gp_item.append(str(item[8][0]))
        else:
            gp_item.append('')
        if item[9] is not None:
            gp_item.append(str(item[9][0]))
        else:
            gp_item.append('')
        gp_item.append('Finance')
        gp_list.append(gp_item)
    print(gp_list)
    write_file(gp_list)


def start_local():
    f = open("data.txt", "r+")
    data = f.read()
    gp_list = json.loads(data).get('data')
    print(gp_list)
    count = 0
    for item in gp_list:
        if count > 5:
            break
        count = count + 1
        # 先转成大的list 然后判断item 如果不符合就remove
        print(item[1])
        # result = request_gp(item[1])
        result = 0
        if result == 0:
            gp_list.remove(item)
            continue
        elif result == 1:
            item[2] = 'False'
        elif result == 2:
            item[2] = 'True'
        write_file(str(item) + ',')
    f.close()
    print(gp_list)


def creat_excel():
    f = open("result1.txt", "r+")
    gp_list = json.loads(f.read()).get('data')
    # 创建一个excel
    workbook = xlsxwriter.Workbook("gp_rank_desc.xlsx")
    # 创建一个sheet
    worksheet = workbook.add_worksheet('7.11')
    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})
    # --------1、准备数据并写入excel---------------
    # 向excel中写入数据，建立图标时要用到
    headings = ['名称', 'GP链接', 'GP描述', '评分', '发布日期', '更新日期', '类别']
    # 写入表头
    worksheet.write_row('A1', headings, bold)
    for index in range(len(gp_list)):
        for item in gp_list[index]:
            # 写入数据
            print(item)
            worksheet.write_row('A' + str(index + 2), gp_list[index])
    workbook.close()


def creat_excel_arr():
    f = open("result2.txt", "r+")
    gp_list = f.read().split('#$&')
    print(gp_list[0])
    # 创建一个excel
    workbook = xlsxwriter.Workbook("gp_rank_desc.xlsx")
    # 创建一个sheet
    worksheet = workbook.add_worksheet('7.11')
    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})
    # --------1、准备数据并写入excel---------------
    # 向excel中写入数据，建立图标时要用到
    headings = ['名称', 'GP链接', 'GP描述', '评分', '发布日期', '更新日期', '类别']
    # 写入表头
    worksheet.write_row('A1', headings, bold)
    for index in range(len(gp_list)):
        items = gp_list[index].split('#$%')
        # 写入数据
        worksheet.write_row('A' + str(index + 2), items)
    workbook.close()

# 解析gp市场排行
if __name__ == '__main__':
    creat_excel_arr()
