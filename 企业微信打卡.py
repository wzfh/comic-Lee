import io
import os
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import uiautomator2 as u2
import time

from PIL import Image

# 发件人信息
sender_email = "1114377437@qq.com"
sender_password = "usnxlmvexcboiagh"

# 收件人信息
recipient_email = "1114377437@qq.com"

# 构造邮件对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = "企微打卡邮件"

# 添加正文
body = "早上企微打卡邮件。"
msg.attach(MIMEText(body, 'plain'))


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


from apscheduler.schedulers.blocking import BlockingScheduler

try:
    print("正在连接设备")
    device = os.popen("adb devices").readlines()
    device_id = device[1]
    print(device_id.split()[0])
except IndexError:
    print('重启手机')
    os.system('adb shell reboot')


def click_text(self, str, sq=0):  # 对于无法直接点击的控件写了个函数
    path = d(text=str)[sq]
    x, y = path.center()
    d.click(x, y)
    return str


class MY():
    def __init__(self):
        # self.file_path=r'C:\Users\rjcsyb2\Desktop\comic-Lee\region.png'
        self.file_path = r'C:\Users\rjcsyb2\Desktop\region.png'

    def 截图(self):
        import uiautomator2 as u2
        import time
        from PIL import Image
        device = os.popen("adb devices").readlines()
        device_id = device[1]
        d = u2.connect_usb(f'{device_id.split()[0]}')
        imge = d.screenshot(format='raw')
        # screen_size = d.window_size()
        # x1, y1, x2, y2 = 34, 431, 1039, 1854
        x1, y1, x2, y2 = 86, 646, 951, 1527
        io_image = io.BytesIO(imge)
        image = Image.open(io_image)
        region_image = image.crop((x1, y1, x2, y2))
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"\n文件 {self.file_path} 已被成功删除.")
        countdown(3)
        # imge.save('text.png')
        region_image.save(self.file_path)
        print('\n重新截取屏幕')

    def 识别图片(self):
        from PIL import Image
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rjcsyb2\Desktop\Tesseract-OCR\tesseract.exe'

        file_path = self.file_path
        img = Image.open(file_path)
        config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
        self.count1 = pytesseract.image_to_string(img, config=config)
        self.image_text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')
        # 打印结果
        print(self.image_text[:7])
        return self.image_text[:7]


def click(text1):
    # d.app_stop_all()
    d.app_stop("com.tencent.mm")
    print('关闭微信')
    d.app_stop("com.tencent.wework")
    print('关闭企业微信')
    countdown(5)
    d.app_start("com.tencent.wework")  # 启动应用
    print("\n企业微信应用启动成功")
    countdown(5)
    d(text="工作台").click()
    print('\n找到工作台')
    countdown(2)
    d.swipe(930, 1480, 980, 480)
    click_text(d, '打卡')
    print('\n找到打卡页面')
    countdown(80)
    if d(text="不在打卡范围内").exists(timeout=2):
        while True:
            d.press("back")
            print('\n返回')
            click_text(d, '打卡')
            print('点击打卡页面按钮')
            print('找到打卡页面')
            d(text=f"{text1}").exists(timeout=2)
            countdown(50)
            MY().截图()
            if MY().识别图片() != '不在打卡范围内':
                break
            continue
    if d(text="下班·正常").exists(timeout=2):
        print('\n下班·正常')
        MY().截图()
    if d(text="上班·正常").exists(timeout=2):
        print('\n上班·正常')
        MY().截图()
    if d(text="上班自动打卡·正常").exists(timeout=2):
        print('\n上班自动打卡·正常')
        MY().截图()
    if d(text="下班自动打卡·正常").exists(timeout=2):
        print('\n下班自动打卡·正常')
        MY().截图()
    if d(text="你已在打卡范围内").exists(timeout=2):
        print('\n你已在打卡范围内')
        countdown(10)
        d(text=f"{text1}").exists(timeout=2)
        if d(text='今日打卡已完成').exists(timeout=2):
            MY().截图()
            d.app_stop("com.tencent.mm")
            d.app_stop("com.tencent.wework")
            os.system('adb shell svc bluetooth disable')
            os.system('adb shell settings put secure location_mode 0')
            os.system('adb shell input keyevent 26')
            with open(f"{MY().file_path}", "rb") as attachment:
                part = MIMEApplication(attachment.read(), _subtype='png')
                part.add_header('Content-Disposition', 'attachment', filename=MY().file_path)
                msg.attach(part)
            # 发送邮件
            with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipient_email, msg.as_string())
            print('退出程序')
            os._exit(0)
    countdown(5)
    # 添加附件
    with open(f"{MY().file_path}", "rb") as attachment:
        part = MIMEApplication(attachment.read(), _subtype='png')
        part.add_header('Content-Disposition', 'attachment', filename=MY().file_path)
        msg.attach(part)
    # 发送邮件
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, msg.as_string())


# def send_info():  # 将打卡信息截图利用小号发送给自己大号
#     d.app_start("com.tencent.mm")  # 启动应用
#     print("\n微信应用启动成功")
#     countdown(4)
#     print(f'\n选择发送人:',end='')
#     click_text(d, "鱼溪")
#     countdown(3)
#     d.click(0.338, 0.953)
#     time.sleep(2)
#     d.click(0.289, 0.815)
#     time.sleep(1)
#     d.click(0.105, 0.817)
#     time.sleep(1)
#     d.click(0.787, 0.815)
#     time.sleep(1)
#     d.click(0.105, 0.684)
#     time.sleep(1)
#     d.click(0.927, 0.943)
#     print('\n已发送打卡短信')
#     time.sleep(1)
#     d.app_stop("com.tencent.mm")
#     print('关闭微信')


# def lya():
#     d.app_start("no.nordicsemi.android.mcp")  # 启动应用
#     print("应用启动成功")
#     # size = d.window_size()
#     # print(size)
#     # x1 = int(size[0] * 0.5)
#     # y1 = int(size[1] * 0.9)
#     # y2 = int(size[1] * 0.15)
#
#     while True:
#         # d.swipe(x1, y1, x1, y2)
#         # d(scrollable=True).scroll.toEnd()
#         d(scrollable=True).scroll.to(text='MJ01_BLE_1260')
#         # if d(text="MJ01_BLE_1260"):
#         time.sleep(2)
#         d(text="MJ01_BLE_1260").click()
#         time.sleep(7)
#         d(text="CLONE").click()
#         d(text="OK").click()
#         break
#     time.sleep(7)
#     click_text(d, "ADVERTISER")
#     time.sleep(1)
#     d.click(0.881, 0.211)
#     time.sleep(2)
#     d(text="OK").click()
#     time.sleep(2)
#     # d.app_stop("no.nordicsemi.android.mcp")
#     # d.app_clear("no.nordicsemi.android.mcp")


def job1():
    os.system('adb devices')
    time.sleep(2)
    os.system(r'adb push C:\Users\rjcsyb2\Desktop\atx-agent_0.10.0_linux_armv7/atx-agent /data/local/tmp')
    time.sleep(2)
    os.system('adb shell chmod 755 /data/local/tmp/atx-agent')
    time.sleep(2)
    os.system('adb shell /data/local/tmp/atx-agent server -d')
    time.sleep(2)
    os.system('adb shell /data/local/tmp/atx-agent server -d --stop')
    time.sleep(2)
    print('打开蓝牙')
    os.system('adb shell svc bluetooth enable')
    print('打开定位')
    os.system('adb shell settings put secure location_mode 1')
    time.sleep(2)
    for i in range(3):
        try:
            print('关闭usb选择')
            os.system('adb shell input tap 185 450')
            print(f'循环次数：{i + 1}')
            click("上班打卡")
            print('\n已打上班卡')
            countdown(5)
        except:
            continue
    d.app_stop("com.tencent.mm")
    print('\n关闭微信')
    d.app_stop("com.tencent.wework")
    print('关闭企业微信')
    print('关闭蓝牙')
    os.system('adb shell svc bluetooth disable')
    print('关闭定位')
    os.system('adb shell settings put secure location_mode 0')
    print('结束程序')
    os.system('adb shell input keyevent 26')


def job2():
    os.system('adb devices')
    time.sleep(2)
    os.system(r'adb push C:\Users\rjcsyb2\Desktop\atx-agent_0.10.0_linux_armv7/atx-agent /data/local/tmp')
    time.sleep(2)
    os.system('adb shell chmod 755 /data/local/tmp/atx-agent')
    time.sleep(2)
    os.system('adb shell /data/local/tmp/atx-agent server -d')
    time.sleep(2)
    os.system('adb shell /data/local/tmp/atx-agent server -d --stop')
    time.sleep(2)
    print('打开蓝牙')
    os.system('adb shell svc bluetooth enable')
    print('打开定位')
    os.system('adb shell settings put secure location_mode 1')
    time.sleep(2)
    for i in range(1):
        try:
            print('关闭usb选择')
            os.system('adb shell input tap 185 450')
            print(f'循环次数：{i + 1}')
            click("下班打卡")
            print('\n已打下班卡')
            countdown(5)
        except:
            continue
    d.app_stop("com.tencent.mm")
    print('\n关闭微信')
    d.app_stop("com.tencent.wework")
    print('关闭企业微信')
    print('关闭蓝牙')
    os.system('adb shell svc bluetooth disable')
    print('关闭定位')
    os.system('adb shell settings put secure location_mode 0')
    print('结束程序')
    os.system('adb shell input keyevent 26')


if __name__ == "__main__":
    d = u2.connect_usb(f'{device_id.split()[0]}')
    print(device_id.split())
    if device_id.split()[1] != 'device':
        print('设备连接失败')
        os.system('adb devices')
        time.sleep(2)
        os.system(r'adb push C:\Users\rjcsyb2\Desktop\atx-agent_0.10.0_linux_armv7/atx-agent /data/local/tmp')
        time.sleep(2)
        os.system('adb shell chmod 755 /data/local/tmp/atx-agent')
        time.sleep(2)
        os.system('adb shell /data/local/tmp/atx-agent server -d')
        time.sleep(2)
        os.system('adb shell /data/local/tmp/atx-agent server -d --stop')
        time.sleep(2)
        print('等待程序启动')
        sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡
        sched.add_job(job1, 'cron', day_of_week='mon-sat', hour='08', minute='00')
        sched.add_job(job1, 'cron', day_of_week='mon-sat', hour='09', minute='00')
        sched.add_job(job2, 'cron', day_of_week='sat', hour='12', minute='00')
        sched.add_job(job2, 'cron', day_of_week='mon-fri', hour='17', minute='30')
        sched.start()
    else:
        job2()
        # sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡
        # sched.add_job(job1, 'cron', day_of_week='mon-sat', hour='08', minute='00')
        # sched.add_job(job2, 'cron', day_of_week='sat', hour='12', minute='00')
        # sched.add_job(job2, 'cron', day_of_week='mon-fri', hour='17', minute='30')
        # sched.start()
