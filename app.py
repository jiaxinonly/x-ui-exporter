from flask import Flask, Response, request
from prometheus_client import generate_latest, Gauge, CollectorRegistry
from functools import wraps
from lib.flow_packet import get_txy_share_flow_packet
import sqlite3

# 数据库地址
DB_PATH = "/etc/x-ui/x-ui.db"
# 是否要求鉴权
REQ_AUTH = False
# 如果需要鉴权，设置账号密码
username = ""
password = ""

# Flask app
app = Flask(__name__)

# 创建指标
registry = CollectorRegistry()
x_ui_all_flow_bytes = Gauge("x_ui_all_flow_bytes", "x-ui总流量", registry=registry)
x_ui_all_up_flow_bytes = Gauge("x_ui_all_up_flow_bytes", "x-ui总上传流量", registry=registry)
x_ui_all_down_flow_bytes = Gauge("x_ui_all_down_flow_bytes", "x-ui总下载流量", registry=registry)
x_ui_user_all_flow_bytes = Gauge("x_ui_user_all_flow_bytes", "x-ui用户总流量", labelnames=['id', 'name', 'protocol'],
                                 registry=registry)
x_ui_user_up_flow_bytes = Gauge("x_ui_user_up_flow_bytes", "x-ui用户上传流量", labelnames=['id', 'name', 'protocol'],
                                registry=registry)
x_ui_user_down_flow_bytes = Gauge("x_ui_user_down_flow_bytes", "x-ui用户下载流量",
                                  labelnames=['id', 'name', 'protocol'], registry=registry)
txy_all_flow_packet_total_amount_Gbytes = Gauge("txy_all_flow_packet_total_amount_Gbytes", "腾讯云所有共享流量包总量",
                                                registry=registry)
txy_all_flow_packet_remaining_amount_Gbytes = Gauge("txy_all_flow_packet_remaining_amount_Gbytes",
                                                    "腾讯云所有共享流量包剩余量",
                                                    registry=registry)
txy_all_flow_packet_used_amount_Gbytes = Gauge("txy_all_flow_packet_used_amount_Gbytes", "腾讯云所有共享流量包使用量",
                                               registry=registry)
txy_flow_packet_total_amount_Gbytes = Gauge("txy_flow_packet_total_amount_Gbytes", "腾讯云流量包总量",
                                            labelnames=['id', 'name', 'type'], registry=registry)
txy_flow_packet_remaining_amount_Gbytes = Gauge("txy_flow_packet_remaining_amount_Gbytes", "腾讯云流量包剩余量",
                                                labelnames=['id', 'name', 'type'], registry=registry)
txy_flow_packet_used_amount_Gbytes = Gauge("txy_flow_packet_used_amount_Gbytes", "腾讯云流量包使用量",
                                           labelnames=['id', 'name', 'type'], registry=registry)


# 身份验证装饰器
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if REQ_AUTH and (not auth or auth.username != username or auth.password != password):
            return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            return f(*args, **kwargs)

    return decorated


@app.route('/')
@requires_auth
def main():
    html = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>x-ui exporter</title>
</head>
<body>
    <h1>x-ui exporter</h1>
    <p><a href="./metrics">Metrics</a></p>
</body>
</html>"""
    return html


@app.route('/metrics')
@requires_auth
def metrics():  # put application's code here
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("select * from inbounds")
    data = cursor.fetchall()
    all_up = 0
    all_down = 0
    for user in data:
        # 统计总上传下载流量
        all_up += user[2]
        all_down += user[3]

        # 设置用户指标值
        x_ui_user_up_flow_bytes.labels(id=user[0], name=user[5], protocol=user[10]).set(user[2])
        x_ui_user_down_flow_bytes.labels(id=user[0], name=user[5], protocol=user[10]).set(user[3])
        x_ui_user_all_flow_bytes.labels(id=user[0], name=user[5], protocol=user[10]).set(user[2] + user[3])
    x_ui_all_flow_bytes.set(all_up + all_down)
    x_ui_all_up_flow_bytes.set(all_up)
    x_ui_all_down_flow_bytes.set(all_down)

    # 添加腾讯云共享流量包指标
    data = get_txy_share_flow_packet()
    txy_all_flow_packet_total_amount_Gbytes.set(data['AllTotalAmount'])
    txy_all_flow_packet_remaining_amount_Gbytes.set(data['AllRemainingAmount'])
    txy_all_flow_packet_used_amount_Gbytes.set(data['AllUsedAmount'])
    for package in data['TrafficPackageSet']:
        txy_flow_packet_total_amount_Gbytes.labels(id=package['TrafficPackageId'], name=package['TrafficPackageName'],
                                                   type=package['DeductType']).set(package['TotalAmount'])
        txy_flow_packet_remaining_amount_Gbytes.labels(id=package['TrafficPackageId'],
                                                       name=package['TrafficPackageName'],
                                                       type=package['DeductType']).set(package['RemainingAmount'])
        txy_flow_packet_used_amount_Gbytes.labels(id=package['TrafficPackageId'], name=package['TrafficPackageName'],
                                                  type=package['DeductType']).set(package['UsedAmount'])

    text = generate_latest(registry)
    return Response(text, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9600)
