import re
import urllib.request
import ssl
import requests

def match():
    f = open('html.txt', "r+")
    pattern = r"(?<=<div jsname=\"sngebd\">)(.*)(?=</div></span>)"
    data = f.read()
    print(re.search(pattern, data).group(0).replace('</div><div jsname="Igi1ac" style="display:none;">', '').replace('\\t', ''))
    f.close()

def request_gp():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'cache-control': ' max-age=0',
        "Connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded",
        "Cookie": "HSID=AFGc8HWqaU2lkStgJ; SSID=AO1NHWPiuu3Cw0LrL; APISID=iQlbrqJ7BhDzC1WZ/AjsMDHPr9cZrFvZOH; SAPISID=r0JQmzI-Ob1Dl77d/ACiZJ-5MYu6BX7NYr; CONSENT=YES+US.zh-CN+20161218-19-0; _ga=GA1.3.1006787421.1560418826; OTZ=4968580_24_24__24_; ANID=AHWqTUnTyhyGCYb0mGardaKqk1ChaFR5gOa_3zEd0sdMhkclLxOiNhOvu65-9yvT; _gid=GA1.3.1983113498.1562816412; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=pspensong@gmail.com; SID=mAcNrdT-n7bAkpxxppMCVRWy63EmbTnGNp3IQvGuqKDo7vDufLcXzVQgT8_5TcrZy1E4LQ.; 1P_JAR=2019-7-13-3; NID=187=QmZgBbfHvKcwKznocS5i2rLI2Kug-T5FyK6vpqNz79gPeTHRJ-V_06y6m9NKhUquvolOP-2sFHNupGW-qd1ZHiuckVRG7vH5WbjGET8HsBE6lY7UcM2BTBv5U-1B668OAuv2dXLoyetU_0qs5olIoLQxh5WZdF2lO5HamXGUINtIS8V0tAPIELMRkWzD_knfq26NM2WK37QjjtvhaTGndwWkrqhbVWAx_k7zYRE2ktBZ4XPsaDbiWUy8o6ydy4BHa2KVePGbutuU3XanqKMpl6o-YAiM9Oy5eAyUus0TIiEgp0lEtWmmb1dPR9yrkJ4WFt0mxH0DLcImnswR2O-wE4MOl-GChp5hPvTAH1h0; SIDCC=AN0-TYsnuIGFwq2U4goRAMXHNfHvS7txOzq1uAEriWlzvztv6DoRNrY5XAB7O72irGsCm_HkiQY",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "x-client-data": "CJS2yQEIpbbJAQjBtskBCNG3yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoBCIKrygE="
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    opener = urllib.request.build_opener()
    opener.addheaders = headers
    # response = opener.open('https://www.appannie.com/apps/google-play/app/ovo.id/details/')
    # response = urllib.request.urlopen('https://www.appannie.com/apps/google-play/app/ovo.id/details/', headers)
    response = requests.get('https://www.appannie.com/apps/google-play/app/ovo.id/details/', headers)
    print(response.text)

if __name__ == '__main__':
    match()
