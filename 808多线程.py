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
        消息ID = '0200'
        消息体属性 = '002F'
        设备号 = f'0{device_number}'
        print(f'设备号:{设备号}')
        流水号 = f'{0}'.zfill(4)

        报警 = f'00000001'
        状态 = '00000003'
        wd2 = float(t[0]) * 1000000
        print(wd2)
        wd3 = hex(int(wd2))
        纬度 = wd3[2:].zfill(8).upper()
        jd2 = float(t[1]) * 1000000
        print(jd2)
        jd3 = hex(int(jd2))
        经度 = jd3[2:].zfill(8).upper()
        高程 = '0000'
        sdu = ['2A', '0A', '5C', '3D']
        速度 = f'00{random.choice(sdu)}'
        fx = ['1C', '2A', '0A', '5C', '3D']
        方向 = f'00{random.choice(fx)}'
        时间 = now_time[2:]
        里程s = ['1A', '5E', '4F']
        里程 = random.choice(里程s)
        附加里程 = f'0104000000{里程}'
        附加信息ID = '0202044C250400000000300103'
        w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加里程 + 附加信息ID
        a = get_xor(w)
        b = get_bcc(a)
        if b.upper() == "7E":
            a.replace("00", "01")
            b = get_bcc(a)
        E = w + b.upper().zfill(2)
        t = '7E' + E.replace("7E", "01") + '7E'
        D = get_xor(E)
        data = '7E ' + D + ' 7E'
        if data[:2] != "7E":
            print(f"错误：{data}")
            t = t[:81] + "00" + t[82:]
            data = get_xor(t)
            print("修改后data：{}".format(data))
            print('\n' * 1)

        print(data)

        s = socket(AF_INET, SOCK_STREAM)

        # s.connect(('120.79.74.223', 17201))  # 测试
        s.connect(('120.79.192.231', 7788))  # 测试
        s.send(bytes().fromhex(data))
        send = s.recv(1024).hex()
        print('服务器应答：' + send.upper())
        print('\n' * 1)
        countdown(1)
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
