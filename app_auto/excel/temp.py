import re
import xlsxwriter
import os
import xlrd


def all_path(dirname):
    global file_name_list
    filter = [".txt"]  # 设置过滤后的文件类型 当然可以设置多个类型
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
            if ext in filter:
                result.append(apath)
    return file_name_list

# 一天的数据
class OneDayData:
    date = ''
    # 24h 上下架数量
    publish_24h = 0
    remove_24h = 0
    # A级客户总数与在线数
    A_customer = 0
    A_off_customer = 0
    # B级客户总数与在线数
    B_customer = 0
    B_off_customer = 0

    all_list = []
    all_ab_list = []
    offline_3_days_list = []
    pending_list = []
    off_24_list = []
    off_48_list = []
    pending_10_list = []
    up_24_list = []
    danger_list = []

start = 'GP在线情况'
end = '24小时内发布情况'
start2 = '24小时内下架'
end2 = '下架3天以上'
off_line = 'OffLine'
pending = 'Pending'
online = 'Online'

def build_data_from_txt(files):
    one_day_datas = []
    # 客户没有反馈 或者不要求上架的
    filter_list = [1073, 1153, 1053]
    for file_name in files:
        f = open(file_name, "r+")
        one_day_data = OneDayData()
        print(one_day_data)
        p = r"(\D*)(\d*)"
        one_day_data.date = re.match(p, file_name).group(2)
        # -1 初始化 0 开始读GP上架情况 1 开始读24小时内发布情况 2 开始读24小时内下架情况 3 读下架超过3天情况
        start_read = -1
        pattern = r"(\d{4,6})(___)([A-D])(___)(\w+)(___)([a-zA-Z0-9\.]*)(___)(\w*)(___)(\d*)(\s\w{5})(.*)"
        pattern_offline_3_days = r"(\d{4,6})(___)(\w+)(___)([A-D])(___)([a-zA-Z0-9\.]*)(____)(online\s)(\d*)(\s\w{5}\s)(___\soffline\s)(\d*)(.*)"
        pattern_24_off = r"(\d{4,6})(___)(\w+)(___)([A-D])(___)([a-zA-Z0-9\.]*)(____)(online\s)(\d*)(\s\w{5})(___)(\d*)(.*)"
        line = f.readline()
        while line:
            if start_read == 0:
                m = re.match(pattern, line)
                if m is not None:
                    one_day_data.all_list.append(build_bean(m))
                    if m.group(3) == "A" or m.group(3) == "B":
                        one_day_data.all_ab_list.append(build_bean(m))
            # 读取24小时发布情况
            elif start_read == 1:
                m = re.match(pattern, line)
                if m is not None:
                    one_day_data.up_24_list.append(build_bean(m))
            # 读取24小时内下架情况 记录下架的上架时长 分别存在24 和 48
            elif start_read == 2:
                m = re.match(pattern_24_off, line)
                if m is not None:
                    if (m.group(5) == "A" or m.group(5) == "B") and int(m.group(10)) < 49:
                        if int(m.group(10)) <= 24:
                            one_day_data.off_24_list.append(build_bean_24_off(m))
                        else:
                            one_day_data.off_48_list.append(build_bean_24_off(m))
            # 读取下架三天以上的数据 这里需要与第一个列表进行比对，剔除非A、B级用户
            elif start_read == 3:
                m = re.match(pattern_offline_3_days, line)
                if m is not None:
                    if m.group(5) == "A" or m.group(5) == "B":
                        one_day_data.offline_3_days_list.append(build_bean_3_days_offline(m))
                # 先过滤是否要剔除
                for no in filter_list:
                    for item in one_day_data.offline_3_days_list:
                        if no == int(item['no']):
                            one_day_data.offline_3_days_list.remove(item)
                            break
                # 遍历列表1进行比对
                for item in one_day_data.offline_3_days_list:
                    for item_all in one_day_data.all_list:
                        # 剔除online状态的 pending状态的不剔除 也要加到高危名单
                        if int(item["no"][0: 4]) == int(item_all['no'][0:4]) and (
                                (item_all['type'] is not "A" and item_all['type'] is not "B") or (
                        item_all['status'].__contains__(online))):
                            one_day_data.offline_3_days_list.remove(item)
                            break
                # 24、48小时内下架的不剔除 也是高危名单
                # for item_24 in off_24_list:
                #     for item in offline_3_days_list:
                #         if int(item["no"][0: 4]) == int(item_24['no'][0:4]):
                #             print(item['no'])
                #             offline_3_days_list.remove(item)
                #             break
                # for item_48 in off_48_list:
                #     for item in offline_3_days_list:
                #         if int(item["no"][0: 4]) == int(item_48['no'][0:4]):
                #             print(item['no'])
                #             offline_3_days_list.remove(item)
                #             break
            if line.__contains__(start):
                start_read = 0
                print('start')
            if line.__contains__(end):
                start_read = 1
            if line.__contains__(start2):
                start_read = 2
            if line.__contains__(end2):
                start_read = 3
            line = f.readline()
        f.close()
        for item in one_day_data.all_ab_list:
            if item['status'] == pending:
                one_day_data.pending_list.append(item)
                if int(item['online_hours']) > 9:
                    one_day_data.pending_10_list.append(item)
        print('===========  24h内上架  ===========')
        print(one_day_data.up_24_list)
        print('======== 下架三天以上 或 高危  ==============')
        print(one_day_data.offline_3_days_list)
        print('===========  上线不到24h   ===========')
        print(one_day_data.off_24_list)
        print('===========  上线不到48h ===========')
        print(one_day_data.off_48_list)
        print('===========  pending10h ===========')
        print(one_day_data.pending_10_list)
        one_day_datas.append(one_day_data)
    return one_day_datas

def build_bean(m):
    item_dict = {}
    item_dict['no'] = m.group(1)
    item_dict['type'] = m.group(3)
    item_dict['author'] = m.group(5)
    item_dict['pkg'] = m.group(7)
    item_dict['online_hours'] = m.group(11)
    if m.group(13).__contains__(pending):
        item_dict['status'] = pending
    elif m.group(13).__contains__(off_line):
        item_dict['status'] = off_line
    else:
        item_dict['status'] = online
    return item_dict


def build_bean_3_days_offline(m):
    item_dict = {}
    item_dict['no'] = m.group(1)
    item_dict['type'] = m.group(5)
    item_dict['author'] = m.group(3)
    item_dict['pkg'] = m.group(7)
    item_dict['online_hours'] = m.group(10)
    item_dict['offline_hours'] = m.group(13)
    item_dict['status'] = off_line
    return item_dict

def build_bean_24_off(m):
    item_dict = {}
    item_dict['no'] = m.group(1)
    item_dict['type'] = m.group(5)
    item_dict['author'] = m.group(3)
    item_dict['pkg'] = m.group(7)
    item_dict['online_hours'] = m.group(10)
    item_dict['ago_hours'] = m.group(13)
    if m.group(14).__contains__(pending):
        item_dict['status'] = pending
    elif m.group(14).__contains__(off_line):
        item_dict['status'] = off_line
    else:
        item_dict['status'] = online
    return item_dict


# 生成excel
def create_excel(one_day_datas):
    # 创建一个excel
    workbook = xlsxwriter.Workbook("gp_data_test1.xlsx")
    for one_day_data in  one_day_datas:
        # 创建一个sheet
        print(one_day_data.date)
        worksheet = workbook.add_worksheet(one_day_data.date)
        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1})
        # --------1、准备数据并写入excel---------------
        # 写入表头
        headings = [one_day_data.date, '客户等级', '编号', '负责人', '包名', '在线时长/不在线时长', '备注', '下架原因', '是否更换域名', '是否更换描述', '人工/脚本']
        heads_format = workbook.add_format({
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            # 'fg_color': '#D7E4BC',  # 颜色填充
        })
        worksheet.write_row('A1', headings, heads_format)
        #  A1是日期+时间 A2~off_24_list size 合并单元格 是在线不满一天
        #  size + off 48 size 合并 在线不满两天
        #  size + pending size 合并 pending时长超过10h
        # size+高危名单size 合并 高危
        # 合并第0行的第0列到第3列。
        merge_format = workbook.add_format({
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            # 'fg_color': '#D7E4BC',  # 颜色填充
        })
        off_24_start_pos = 0
        off_24_end_pos = 0
        off_48_start_pos = 0
        off_48_end_pos = 0
        off_pending_start_pos = 0
        off_pending_end_pos = 0
        off_danger_start_pos = 0
        off_danger_end_pos = 0
        # first_row, first_col, last_row, last_col
        cursor = 1
        worksheet.merge_range(cursor, 0, len(one_day_data.off_24_list) + 2, 0, '在线时长不满一天', merge_format)
        off_24_start_pos = 1
        cursor = len(one_day_data.off_24_list) + 2
        worksheet.merge_range(cursor + 1, 0, cursor + 2 + len(one_day_data.off_48_list), 0, '在线时长不满两天', merge_format)
        off_48_start_pos = cursor + 1
        cursor = cursor + 2 + len(one_day_data.off_48_list)
        worksheet.merge_range(cursor + 1, 0, cursor + 2 + len(one_day_data.pending_10_list), 0, 'Pending时长超过10h', merge_format)
        off_pending_start_pos = cursor + 1
        cursor = cursor + 2 + len(one_day_data.pending_10_list)
        worksheet.merge_range(cursor + 1, 0, cursor + 2 + len(one_day_data.offline_3_days_list), 0, '高危', merge_format)
        off_danger_start_pos = cursor + 1
        cursor = cursor + 2 + len(one_day_data.pending_10_list)
        # 设置列的宽度
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(3, 3, 12)
        worksheet.set_column(4, 4, 20)
        # 开始写在线时长不满一天的
        cell_format = workbook.add_format({
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            # 'fg_color': '#D7E4BC',  # 颜色填充
        })
        write(worksheet, off_24_start_pos + 1, one_day_data.off_24_list, cell_format)
        write(worksheet, off_48_start_pos + 1, one_day_data.off_48_list, cell_format)
        write(worksheet, off_pending_start_pos + 1, one_day_data.pending_10_list, cell_format)
        write(worksheet, off_danger_start_pos + 1, one_day_data.offline_3_days_list, cell_format, True)
    workbook.close()

def write(worksheet, pos, data, format1, danger = False):
    # 生成数组
    for item in data:
        array_data = [item.get('type'), item.get('no'), item.get('author'), item.get('pkg')]
        if danger:
            array_data.append( '{}/{}'.format(item.get('online_hours'), item.get('offline_hours')))
        else:
            array_data.append(item.get('online_hours'))
        if item.get('memo') is not None:
            array_data.append(item.get('memo'))
        worksheet.write_row('B{}'.format(pos), array_data, format1)
        pos = pos + 1


# 先从最上面的列表 读取客户的等级 存储所有的A、B级用户
# 读取24小时内发布情况 暂不处理
# 读取24小时内下架情况 在线时长小于24或48的 单独存储
# 读取超过3天未上线的 存储之后 与第一个list比对，剔除非A、B级用户
# 高危名单定义 超过3天不在线，频繁下架 频繁下架的需要读历史数据 与今天的下架进行比对
if __name__ == '__main__':
    file_path = 'D:\\gp\\'
    files = []
    for file in all_path(file_path):
        files.append(file_path + file)
    create_excel(build_data_from_txt(files))