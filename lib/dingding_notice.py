from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, date

token = ""
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
# 初始化机器人小丁
dingding = DingtalkChatbot(webhook)

today = "2023-09-14"


def send_dingding_msg(data):
    global today
    if today != date.today():
        if len(data['TrafficPackageSet']) == 0:
            text = "### 流量包通知\n没有流量包了老板[大哭]"
        elif data['AllRemainingAmount'] <= 10:
            text = f"### 流量包通知\n快没流量了，还剩{data['AllRemainingAmount']}GB[流泪]"
        else:
            text = "### 流量包通知\n#### 流量快过期了，赶紧用啊[怒吼]\n"
            for package in data['TrafficPackageSet']:
                deadline = datetime.strptime(package['Deadline'], '%Y-%m-%dT%H:%M:%SZ')
                if (deadline - datetime.today()).days < 15:
                    text += f"#### id:{package['TrafficPackageId']}\n #### name:{package['TrafficPackageName']}\n #### 总流量:{package['TotalAmount']}GB\n #### 剩余量:{package['RemainingAmount']}GB"

        dingding.send_markdown(title='流量包通知', text=text, is_at_all=False)
        today = date.today()
