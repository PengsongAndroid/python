#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import string
import sys, os
import re
import shutil
import requests
import json

#  app端创建分支，生成logo，替换logo，替换图片资源，全局替换appname，生成签名，修改包名，根据gw修改properties相关字段，commitpush，修改完后直接生成apk进行测试。

#  包名的三段名称
pkg_name1, pkg_name2, pkg_name3, full_pkg_name = "", "", "", ""

#  资源文件路径
source_path = None
#  项目文件路径
project_path = None
#  appName
app_name = None
#  原始包名
old_pkg_name = None
# jks name
jks_name = None
# gw url
gw_url = None
# 产品id
product_id = None
# main color
main_color = None
# main text color
main_text_color = None

# 随机生成4~6位的字母 调用三个去拼一个包名
def radomStr():
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', random.randint(4, 6)))


# 三次调用随机方法 生成包名
def generatePkgName():
    global pkg_name1, pkg_name2, pkg_name3
    if pkg_name1 == "" and pkg_name2 == "":
        pkg_name1 = radomStr()
        pkg_name2 = radomStr()
        pkg_name3 = radomStr()
    return pkg_name1 + "." + pkg_name2 + "." + pkg_name3


#  读取本地配置文件
def init():
    print('init start')
    #  配置文件
    config_file = open("D:\config.txt", "r+")
    global source_path, project_path, app_name, old_pkg_name, jks_name, gw_url, product_id, full_pkg_name, main_color, main_text_color
    line = config_file.readline()
    while line:
        if project_path is None:
            project_path = common_match('project_path', line)
        if source_path is None:
            source_path = common_match('source_path', line)
        if app_name is None:
            app_name = common_match('app_name', line)
        if old_pkg_name is None:
            old_pkg_name = common_match('old_pkg_name', line)
        if jks_name is None:
            jks_name = common_match('jks', line)
        if gw_url is None:
            gw_url = common_match('gw_url', line)
        if product_id is None:
            product_id = common_match('product_id', line)
        if main_color is None:
            main_color = common_match('main_color', line)
        if main_text_color is None:
            main_text_color = common_match('main_text_color', line)
        line = config_file.readline()
    config_file.close()
    full_pkg_name = generatePkgName()
    print('init finished')

def common_match(name, data):
    pattern = r"({}:)(.*)".format(name)
    m = re.match(pattern, data)
    if m is not None:
        return m.group(2)
    return None

def common_match2(name, data):
    pattern = r"({}=)(.*)".format(name)
    m = re.match(pattern, data)
    if m is not None:
        return m.group(2)
    return None

#  修改图片资源
def modify_pic_source():
    print('modify_pic_source start')
    project_source_path =  project_path + '\\app\\src\\main\\res\\drawable-xxhdpi\\'
    #  对文件进行循环
    for f in os.listdir(source_path):
        # print(f)
        if f.endswith(".png"):
            if deleteNoUsed(f):
                continue
            #  数字或"_"开头 / 带有“-” 的文件重命名
            num_patterm = r"\d.*"
            num_m = re.match(num_patterm, f)
            if num_m is not None:
                file_name = modify_file_name(num_m.group())
            else:
                file_name = f
            print(file_name)
            file_name = file_name.replace("-", "_").replace(" ", "_").replace("*", "_").lower()
            file_name = autoName(file_name)
            print(file_name + "===" + f)
            # try:
            new_file_path = project_source_path + file_name
            # 如果文件存在 先删除
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            shutil.copy(source_path + "\\" + f, project_source_path + file_name)
            # except Exception as e:
            #     print("exception：" + file_name)
    print('modify_pic_source finished')


#  删除无用的图片文件
def deleteNoUsed(fileName):
    if "logo107_4.png,logo207_4.png,logo307_4.png,".__contains__(fileName):
        os.remove(source_path + '\\' + fileName)
        print("delete " + fileName)
        return bool(1)
    return bool(0)

# 资源文件替换为指定命名
def autoName(name):
    if name.__contains__("application") and name.__contains__("passed"):
        return "applicationpassed09_2.png"
    elif name.__contains__("work") and name.__contains__("card"):
        return "work_card.png"
    elif name.__contains__("frame") and name.__contains__("error"):
        return "frame_wrong.png"
    elif name.__contains__("frame") and name.__contains__("wrong"):
        return "frame_wrong.png"
    elif name.__contains__("frame") and name.__contains__("right"):
        return "frame_right.png"
    elif name.__contains__("front01"):
        return "id_right.png"
    elif name.__contains__("front02"):
        return "id_wrong_left.png"
    elif name.__contains__("front03"):
        return "id_wrong_middle.png"
    elif name.__contains__("front04"):
        return "id_wrong_right.png"
    elif name.__contains__("level") and name.__contains__("up"):
        return "levelup09_5.png"
    elif name.__contains__("logo") and name.__contains__("512"):
        return "logo.png"
    elif name.__contains__("icon") and name.__contains__("process"):
        return "dot14_1.png"
    elif name.__contains__("step01"):
        return "pic0104.png"
    elif name.__contains__("step02"):
        return "pic0204.png"
    elif name.__contains__("step03"):
        return "pic0304.png"
    elif name.__contains__("step04"):
        return "pic0404.png"
    elif ((name.__contains__('coin') or name.__contains__("money") or name.__contains__("amount")) and name.__contains__(
            "icon") and name.__contains__("08")):
        return "icon_amount08.png"
    elif name.__contains__("time") and name.__contains__("icon") and name.__contains__("08"):
        return "icon_time08.png"
    elif ((name.__contains__('coin') or name.__contains__("money") or name.__contains__("amount")) and name.__contains__(
            "icon") and name.__contains__("10")):
        return "icon_amount10_2.png"
    elif name.__contains__("time") and name.__contains__("icon") and name.__contains__("10"):
        return "icon_time10_2.png"
    elif name.__contains__("bannner") and name.__contains__("02"):
        return "banner02.png"
    elif name.__contains__("icon0202_2"):
        return "more02_2.png"
    elif name.__contains__("icon0202_2"):
        return "more02_2.png"
    return name

#  把字符串中的开头数字和下划线移动到末尾
def modify_file_name(fileName):
    fileName = str(fileName)
    patterm = r"([^a-zA-Z]*)([a-zA-Z_0-9]*)"
    m = re.match(patterm, fileName.split(".")[0])
    fileName = m.group(2) + m.group(1) + ".png"
    fileName = fileName.replace("_.", ".")
    return fileName

# 把修改好的文件资源 复制到对应目录
def movePicSource():
    # 删除原有的图片目录
    shutil.rmtree(project_path + "\\app\\src\\main\\res\\drawable-xxhdpi")
    # 复制修改好的资源文件到该路径
    shutil.copytree(source_path + "\\drawable-xxhdpi", project_path + "\\app\\src\\main\\res")
    return

#  全局修改app_name 修改包名 这个方法会遍历app目录下所有的java、xml文件 目前只有app目录下会有包名
def modify_pkg_name():
    print('modify_pkg_name start')
    # 只需要遍历 java目录还有layout xml 和 manifest.xml 由于目前代码中xml没有包名 这里就不遍历了
    fullPkgName = pkg_name1 + "." + pkg_name2 + "." + pkg_name3
    javaPath = project_path + "\\app\\src\\main\\java"
    replace_pkg_name(all_path(javaPath), fullPkgName)
    old_pkg = str(old_pkg_name).split('.')
    renameDir(javaPath + '\\{}'.format(old_pkg[0]), javaPath + '\\{}'.format(pkg_name1))
    renameDir(javaPath + '\\{}\\{}'.format(pkg_name1, old_pkg[1]), javaPath + '\\{}\\{}'.format(pkg_name1, pkg_name2))
    renameDir(javaPath + '\\{}\\{}\\{}'.format(pkg_name1, pkg_name2, old_pkg[2]), javaPath + '\\{}\\{}\\{}'.format(pkg_name1, pkg_name2, pkg_name3))
    print('modify_pkg_name finished')

# 修改文件夹的名称
def renameDir(old_path, new_path):
    os.rename(old_path, new_path)
    return


# 遍历指定目录 返回全路径名
def all_path(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)
    return result

# 替换指定文件中的包名
def replace_pkg_name(files, pkg_name):
    for file in files:
        modify_file_content(file, old_pkg_name, pkg_name)
    # 修改manifest
    modify_file_content(project_path + "\\app\\src\\main\\AndroidManifest.xml", old_pkg_name, pkg_name)
    return


def modify_file_content(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    f.close()
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
    f.close()

# 请求biz的请求头 请求前需要修改cookie 可能失效
headers = {
"accept": "application/json",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "keep-alive",
"content-type": "application/x-www-form-urlencoded",
"Cookie": "token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODYwMjcyMDA1NyIsImV4cCI6MTU2MjA1ODYxMX0.MG9vn-NEflpon3V29D2sxE0050pCda5jLN3pwjFFWSgc8Zu6JP3TXkkZRePKTmkxkWnH7fG8V2vx0gToOgbqJQ",
"Host": "biz.apollo.starblingbling.com",
"Referer": "https://biz.apollo.starblingbling.com/",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
"x-auth-token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODYwMjcyMDA1NyIsImV4cCI6MTU2MjA1ODYxMX0.MG9vn-NEflpon"
                "3V29D2sxE0050pCda5jLN3pwjFFWSgc8Zu6JP3TXkkZRePKTmkxkWnH7fG8V2vx0gToOgbqJQ"
}

#  获取gw配置 然后修改properties
def modify_gw_source():
    print('modify_gw_source start')
    # 请求gw地址
    response = requests.get(gw_url)
    json_str = json.loads(response.text)
    gateway_url = json_str.get("gateway")[0]
    gateway_ip = json_str.get("gateway")[1]
    harvester = str(json_str.get("harvester")[0]).split(":")
    harvester_ip = harvester[0] + ":" + harvester[1]
    harvester_port = harvester[2]
    repay_url = json_str.get("repay")[0]
    admin_host = json_str.get("admin")[0]
    agreement_url = json_str.get("privacy")[0]
    home = json_str.get("home")[0]
    print(harvester_ip + "==========" + harvester_port)
    # 请求biz 的对应产品页 获取第三方配置信息
    biz_url = 'https://biz.apollo.starblingbling.com/api/api/service-provider-info/' + product_id
    biz_response = requests.get(biz_url, headers = headers)
    print(biz_response)
    biz_datas = json.loads(biz_response.text).get('data')
    # 循环返回的数组 去获取需要修改的参数 目前来看需要修改的只有facebook和zendesk
    facebook_app_id, account_kit_client_token, zendesk_url, zendesk_app_id, zendesk_client_id = "","","","",""
    for data in biz_datas:
        # 如果是FACEBOOK或ZENDESK 则遍历bizItemEntityList
        service_name = data.get("serviceProviderName")
        entity_list = data.get('bizItemEntityList')
        if service_name == 'FACEBOOK':
            for entity in entity_list:
                print(entity)
                if entity.get('propKey') == 'accountkit_app_id':
                    facebook_app_id = entity.get('propVal')
                elif entity.get('propKey') == '客户端口令':
                    account_kit_client_token = entity.get('propVal')
        elif service_name == 'ZENDESK':
            zendesk_url = data.get('description')
            for entity in entity_list:
                if entity.get('propKey') == 'APP ID':
                    zendesk_app_id = entity.get('propVal')
                elif entity.get('propKey') == 'Client ID':
                    zendesk_client_id = entity.get('propVal')
    # 读取properties文件 修改对应内容
    properties_path = project_path + '\\gradle.properties'
    # 包名版本
    modify_propertiest(properties_path, 'app_id', full_pkg_name)
    modify_propertiest(properties_path, 'version_code', '100')
    modify_propertiest(properties_path, 'version_name', '1.0.0')
    modify_propertiest(properties_path, 'app_name', app_name)
    # 签名
    modify_propertiest(properties_path, 'signing_keyAlias', jks_name)
    modify_propertiest(properties_path, 'signing_certificate', '../jks/' + jks_name + '.keystore')
    modify_propertiest(properties_path, 'signging_certificatePassword', jks_name)
    modify_propertiest(properties_path, 'signging_certificatePassword', jks_name)
    # 主题色
    modify_propertiest(properties_path, 'main_color', main_color)
    modify_propertiest(properties_path, 'main_text_color', main_text_color)
    # zendesk
    modify_propertiest(properties_path, 'zendesk_url', '"' + zendesk_url + '"')
    modify_propertiest(properties_path, 'zendesk_app_id', '"' + zendesk_app_id + '"')
    modify_propertiest(properties_path, 'zendesk_client_id', '"' + zendesk_client_id + '"')
    # facebook
    modify_propertiest(properties_path, 'facebook_app_id', facebook_app_id)
    modify_propertiest(properties_path, 'account_kit_client_token', account_kit_client_token)
    # gw
    modify_propertiest(properties_path, 'gateway_url', '"' + gateway_url + '"')
    modify_propertiest(properties_path, 'gateway_ip', '"' + gateway_ip + '"')
    modify_propertiest(properties_path, 'base_url', '"' + home + '"')
    modify_propertiest(properties_path, 'harvest_ip', '"' + harvester_ip + '"')
    modify_propertiest(properties_path, 'harvest_port', harvester_port)
    modify_propertiest(properties_path, 'repayment_h5', '"' + repay_url + '"')
    modify_propertiest(properties_path, 'admin_host', '"' + admin_host + '"')
    modify_propertiest(properties_path, 'agreement_url', '"' + agreement_url + '"')
    print('modify_gw_source finished')


def modify_gw_source_simple():
    print('modify_gw_source start')
    # 读取properties文件 修改对应内容
    properties_path = project_path + '\\gradle.properties'
    # 包名版本
    modify_propertiest(properties_path, 'app_id', full_pkg_name)
    modify_propertiest(properties_path, 'version_code', '101')
    modify_propertiest(properties_path, 'version_name', '1.0.1')
    # 签名
    modify_propertiest(properties_path, 'signing_keyAlias', jks_name)
    modify_propertiest(properties_path, 'signing_certificate', '../jks/' + jks_name + '.keystore')
    modify_propertiest(properties_path, 'signging_certificatePassword', jks_name)
    modify_propertiest(properties_path, 'signging_certificatePassword', jks_name)
    print('modify_gw_source finished')

def modify_propertiest(path, key, new_value):
    with open(path, "r",  encoding="UTF-8") as f:
        for line in f:
            value = common_match2(key,line)
            if value is not None:
                modify_file_content(path, value, new_value)
    f.close()
#  新建分支
def creat_branch():
    return


#  提交代码
def commit_and_push():
    return


#  打tag
def creat_tag():
    return


#  生成签名文件
def create_jks():
    print('create jks start')
    command = 'keytool -genkey -alias {alias} -keypass {alias} -storepass {alias} -dname "CN=Unknown, OU=Unknown, O=Unknown, L=Unknown, ST=Unknown, C=Unknown" -keyalg RSA -validity 20000 -keystore {alias}.keystore'
    command = command.format(alias=jks_name)
    print(command)
    with os.popen(command, mode='r') as res:
        result = str(res.read())
        if result == "":
            file_path = os.getcwd() + "\\" + jks_name + ".keystore"
            print("build jks success " + file_path)
            # 把jks文件移动到app目录jks下
            jks_path = project_path + "\\jks"
            shutil.rmtree(jks_path)
            os.makedirs(jks_path)
            shutil.move(file_path, jks_path)
        else:
            print(result)
    print('create jks finished')


#  生成apk
def generate_apk():
    print('generate apk start')

    print('generate apk finished')


if __name__ == '__main__':
    # 创建分支
    # creat_branch()
    # 初始化配置
    init()
    # 修改图片资源 并替换掉项目中的目录
    # modify_pic_source()
    # 生成jks 并替换项目中的目录
    create_jks()
    # 全局修改包名
    modify_pkg_name()
    # 修改gw配置
    # modify_gw_source()
    modify_gw_source_simple()
    # 生成apk
    # generate_apk()
    # 提交代码
    # commit_and_push()
