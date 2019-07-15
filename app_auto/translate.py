import requests

#  有道翻译的api是免费的 其他的调用比较麻烦
if __name__ == '__main__':
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "Cookie": "CONSENT=YES+RU.en-GB+201906; _ga=GA1.3.1486001104.1562655532; APISID=qKLMzNH2E8oXv6UG/A1fXPs-bfOJICitbx; HSID=AtpCcJY4Ll9GOiv1u; SAPISID=odPLRFtrB9jk-sRJ/AG8kjuDI1rHnPaETa; SSID=AAVTTe7LYAPTPPE0z; SID=lwfOz_qa6q54ux3MtRYwCZI8Smn-UPhM0PzIDlnj-VHb6-zYk9GgXQ00WclID20UG3W_Ag.; SEARCH_SAMESITE=CgQIqI0B; ANID=AHWqTUlRQonBsPQ19GwhOj8vvQgQs73hnWw3QTeIlINGViGQKKErf8mzEHlDVGE9; NID=187=BUShnjvQ3wLFzwtF290q0eaV-6Ey1JwNlYITu9o9gdW9pGAO6Pi0vidZL9Ws6aAzEqTsT8W73hpc7AU7jOX3t8s4Aa52lRWFh43-6o3PYVMvWSzpMxocg5MuqBXz7FDQQiF4riL2fqoPBcuDww6J8QIjb5PgE7qpSI6fYL1k1JW53VWm-jEXD2cfGsQVTDNO1_1pPAfmDPgf45FZiW--TRWYHDnDh-82tcY47HKKTBcl; _gid=GA1.3.17312853.1563177185; 1P_JAR=2019-7-15-7; SIDCC=AN0-TYvupXFkk48V-7yAouD860n9y3Q96enVS62cwGLmt2R9VfW2NM_zKlzSMk4cFnIsAVG2EAQ",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "referer": "https://translate.google.com/?rlz=1C1CHWA_en__855__855&um=1&ie=UTF-8&hl=en&client=tw-ob",
        "x-client-data": "JO2yQEIpbbJAQjEtskBCNG3yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoBCJetygEIzK3KAQi/r8oB"
    }
    # response = requests.get('')
    print('Aplikasi keuangan mikro dikeluarkan oleh Shenzhen Investment Point Internet Financial Services Limited di bawah Undang-undang Otoritas Jasa Keuangan.'.encode())