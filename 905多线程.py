import csv
import os
import random
import re
import threading
import time
from os import path
from socket import socket, AF_INET, SOCK_STREAM





def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)



def send_device_number(device_number):
    def get_xor(data):
        result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
        return result

    def get_bcc(inputStr: str) -> str:
        bcc = 0
        for i in inputStr.split(' '):
            bcc = bcc ^ int(i, 16)
        return f'{bcc:x}'
        # return f'{bcc}'

    path = os.path.dirname(__file__)
    # print(path)
    file_path = path + '/12.csv'
    fCase = open(file_path, 'r', encoding='gbk')
    datas = csv.reader(fCase)
    data1 = []
    o = 0
    for line in datas:
        data1.append(line)
    for nob1 in range(0, 864):
        t = data1[nob1]
        o += 1
        print('发送第%d条' % o)
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        # wd1 = get_latitude(base_lat=23.012173, radius=100000)
        # wd2 = float(wd1) * 60 / 0.0001
        wd2 = float(t[0]) * 60 / 0.0001
        wd3 = hex(int(wd2))
        # jd1 = get_longitude(base_log=114.348462, radius=100000)
        # jd2 = float(jd1) * 60 / 0.0001
        jd2 = float(t[1]) * 60 / 0.0001
        jd3 = hex(int(jd2))
        标识位 = '7E'
        消息ID = '0200'
        消息体属性 = '0023'
        # 设备号 = f'14569856655'
        # ISU标识 = '0{}'.format(设备号)  # 10位
        ISU标识 = f'0{device_number}'  # 10位
        流水号 = f'{1}'.zfill(4)
        正常 = '00000000'
        报警 = 正常
        状态 = '00000100'
        纬度 = wd3[2:].zfill(8).upper()
        经度 = jd3[2:].zfill(8).upper()
        速度 = '00E3'
        方向 = '01'
        时间 = now_time[2:]
        里程s = ['1A', '5E', '4F']
        附加里程 = f'0104000000{random.choice(里程s)}'
        油量 = ['5208', '044C', '04B0']
        附加油量 = f'0202{random.choice(油量)}'
        w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加里程 + 附加油量
        a = get_xor(w)
        b = get_bcc(a).zfill(2)
        E = w + b.upper()
        t = 标识位 + E.replace("7E", "00") + 标识位
        D = get_xor(E)
        data = '7E ' + D + ' 7E'
        if data[:2] != "7E":
            print(f"错误：{data}")
            print('\n' * 1)
            # print(t[80:])
            t = t[:81] + "00" + t[82:]
            # print("修改后t：{}".format(t))
            data = get_xor(t)
            print("修改后data：{}".format(data))
            print('\n' * 1)
        print(t)
        # print('\n' * 1)
        print(data)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('120.79.74.223', 17202))  # 测试
        # s.connect(('120.79.176.183', 17800))#压测
        # s.connect(('47.119.168.112', 17800))#生产
        s.send(bytes().fromhex(data))
        send = s.recv(1024).hex()
        print('服务器应答：' + send.upper())
        print('\n' * 1)
        countdown(10)
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
