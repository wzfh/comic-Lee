from PIL import Image
import pytesseract

from 早上企微打卡 import msg, sender_email, sender_password, recipient_email

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rjcsyb2\Desktop\Tesseract-OCR\tesseract.exe'


# file_path=r'C:\Users\rjcsyb2\Desktop\region.png'
# img = Image.open(file_path)
# config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
# print(pytesseract.image_to_string(img, config=config))
import io
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
class MY():
    def __init__(self):
        self.file_path=r'C:\Users\rjcsyb2\Desktop\region.png'

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
        x1, y1, x2, y2 = 86, 646, 950, 1527
        io_image = io.BytesIO(imge)
        image = Image.open(io_image)
        region_image = image.crop((x1, y1, x2, y2))
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"\n文件 {self.file_path} 已被成功删除.")
        # imge.save('text.png')
        region_image.save(self.file_path)
        print('重新截取屏幕')

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

    def 识别图片1(self):
        from PIL import Image
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rjcsyb2\Desktop\Tesseract-OCR\tesseract.exe'

        file_path = r'C:\Users\rjcsyb2\Desktop\region.png'
        img = Image.open(file_path)
        config = r'-c tessedit_char_whitelist=0123456789 --psm 10'
        # self.count1 = pytesseract.image_to_string(img, config=config)
        self.image_text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')
        # 打印结果
        print(self.image_text[15:19])
        return self.image_text[15:19]

import uiautomator2 as u2
print("正在连接设备")
device = os.popen("adb devices").readlines()
device_id = device[1]
d = u2.connect_usb(f'{device_id.split()[0]}')
if d(text="你已在打卡范围内").exists(timeout=2):
    print('\n你已在打卡范围内')
    if MY().识别图片1() == '下班打卡' or d(text="上班·正常").exists(timeout=2) or d(text="上班自动打卡·正常").exists(timeout=2):
        print('\n已上班打卡')
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
# MY().识别图片1()
# print('wwewewewe')
# import os
# import time
#
# # 发件人信息
# sender_email = "1114377437@qq.com"
# sender_password = "usnxlmvexcboiagh"
# #
# # # 收件人信息
# recipient_email = "1114377437@qq.com"
# #
# # 构造邮件对象
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = recipient_email
# msg['Subject'] = "这是一封测试邮件"
#
# # 添加正文
# body = "这是一封测试邮件，用Python发送。"
# msg.attach(MIMEText(body, 'plain'))
#
# # 添加附件
# with open("region.png", "rb") as attachment:
#     part = MIMEApplication(attachment.read(), _subtype='pdf')
#     part.add_header('Content-Disposition', 'attachment', filename="region.png")
#     msg.attach(part)
#
# # 发送邮件
# with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
#     smtp.login(sender_email, sender_password)
#     smtp.sendmail(sender_email, recipient_email, msg.as_string())
#
#
# # from apscheduler.schedulers.blocking import BlockingScheduler
# # import uiautomator2 as u2
# # from apscheduler.schedulers.blocking import BlockingScheduler
# #
# # print("正在连接设备")
# # device = os.popen("adb devices").readlines()
# # device_id = device[1]
# # print(device_id.split()[0])
# # d = u2.connect_usb(f'{device_id.split()[0]}')
# # print(device_id.split())
# #
# #
# # def click_text(self, str, sq=0):  # 对于无法直接点击的控件写了个函数
# #     path = d(text=str)[sq]
# #     x, y = path.center()
# #     d.click(x, y)
# #     print(str)
# #
# #
# # # os.system(r'adb push C:\Users\rjcsyb2\Desktop\atx-agent_0.10.0_linux_armv7/atx-agent  /data/local/tmp')
# # # time.sleep(2)
# # # os.system('adb shell chmod 755 /data/local/tmp/atx-agent')
# # # time.sleep(2)
# # # os.system('adb shell /data/local/tmp/atx-agent server -d')
# # # time.sleep(2)
# # # os.system('adb shell /data/local/tmp/atx-agent server -d --stop')
# # # time.sleep(2)
# # # print('等待程序启动')
# #
# # def job1():
# #     os.system('adb shell input tap 185 450')
# # sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡
# # sched.add_job(job1, 'cron', day_of_week='mon-sat', hour='08', minute='00')
# # sched.start()
#
#
