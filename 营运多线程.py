import csv
import os
import random
import re
import threading
import time
from os import path
from socket import socket, AF_INET, SOCK_STREAM
紧急报警 = '00000001'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
正常 = '00000000'

未卫星定位 = '00000001'
南纬 = '00000002'
西经 = '00000004'
停运状态 = '00000008'
预约任务车 = '00000010'
空转重 = '00000020'
重转空 = '00000040'
ACC开 = '00000100'
重车 = '00000200'
车辆油路断开 = '00000400'
车辆电路断开 = '00000800'
车门加锁 = '00001000'
车辆锁定 = '00002000'
已达到限制营运次数时间 = '00004000'
ACC开和载客 = '00000300'




def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)
def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result

def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)
    return f'{bcc:x}'


def send_device_number(device_number):
    path = os.path.dirname(__file__)
    file_path = path + '/12.csv'
    fCase = open(file_path, 'r', encoding='gbk')
    datas = csv.reader(fCase)
    data1 = []
    o = 0
    for line in datas:
        data1.append(line)
    for nob1 in range(0, 1):
        t = data1[nob1]
        o += 1
        print('发送第%d条' % o)
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        标识位 = '7E'
        消息ID = '0B05'
        消息体属性 = '0073'
        ISU标识 = f'0{device_number}'
        流水号 = f'0001'
        报警 = 正常
        状态 = 空转重
        wd2 = float(t[0]) * 1000000
        print(wd2)
        wd3 = hex(int(wd2))
        纬度 = wd3[2:].zfill(8).upper()
        jd2 = float(t[1]) * 1000000
        print(jd2)
        jd3 = hex(int(jd2))
        经度 = jd3[2:].zfill(8).upper()
        速度 = '0013'
        方向 = '01'
        时间 = now_time[2:]

        报警1 = 正常
        状态1 = 重转空
        wd2 = float(t[0]) * 1000000
        print(wd2)
        wd3 = hex(int(wd2))
        纬度1 = wd3[2:].zfill(8).upper()
        jd2 = float(t[1]) * 1000000
        print(jd2)
        jd3 = hex(int(jd2))
        经度1 = jd3[2:].zfill(8).upper()
        速度1 = '0031'
        方向1 = '04'
        时间1 = now_time[2:]

        营运ID = '3590AA28'  # 001101  0110  01000  01010 101000 101000
        评价ID = '3590AA28'
        评价选项 = '01'
        评价选项扩展 = '0000'
        电召订单ID = '1'.zfill(8)
        车牌号 = '534E31323535'  # SN1255
        企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
        驾驶员从业资格证号 = '534E3132333435363738393132333435363737'  # SN12345678912345679
        上车时间 = 时间[:10]
        上车时间1 = 时间[:10].replace(f'{上车时间}', f'{int(上车时间) - 1}')
        下车时间 = 上车时间[6:]
        计程公里数 = '000920'
        空驶里程 = '0091'
        fjf=['100','230','340','235']
        附加费 = f'000{random.choice(fjf)}'
        等待计时时间 = '0220'
        # print(等待计时时间)
        je=['3300','2500','4210','5200']
        交易金额 = f'00{random.choice(je)}'
        当前车次 = f'{0}'.zfill(8)
        交易类型 = '00'  # 0x00:现金交易：0x01:M1卡交易：0x03：CPU卡交易：0x09:其他
        附加 = '01040000008E0202044C250400000000300103'

        w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 报警1 + 状态1 + 纬度1 + 经度1 + 速度1 + 方向1 + 时间1 + 营运ID + 评价ID + 评价选项 + 评价选项扩展 + 电召订单ID + 车牌号 + 企业经营许可证号 + 驾驶员从业资格证号 + 上车时间1 + 下车时间 + 计程公里数 + 空驶里程 + 附加费 + 等待计时时间 + 交易金额 + 当前车次 + 交易类型 + 附加
        # w='0B0500830135268588550033000000080000000100D2B02C0416D0F6000000231205141112000000080000020100D2B02C0416D0F6000000231205141600370AE280000000000000000000000041303030303036313233203435363700000000000000BDADCBD5B0A2B2A8C2DE00000000000000000023120514101416000000000000000000050000860000001B00'
        a = get_xor(w)
        b = get_bcc(a)
        t = 标识位 + w + b.upper() + 标识位
        data = get_xor(t)
        print(t)
        print(data)

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('120.79.74.223', 17202))
        s.send(bytes().fromhex(t))
        send = s.recv(1024).hex()
        print(send.upper())
        print('\n' * 1)
        time.sleep(1)

    time.sleep(10)
    print(f"Sending device number: {device_number}")
    print(f"Device number {device_number} sent successfully!")


def read_and_send_device_numbers(filename):
    with open(filename, 'r', encoding='gbk') as file:
        device_numbers = file.readlines()

    threads = []
    for device_number in device_numbers:
        device_number = device_number.strip()  # 移除行尾的换行符
        thread = threading.Thread(target=send_device_number, args=(device_number,))
        thread.start()
        threads.append(thread)

        # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("All device numbers have been sent.")


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    file_path = path + '/13.csv'
    read_and_send_device_numbers(file_path)
