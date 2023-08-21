from flask import Flask, Response, request
from prometheus_client import generate_latest, Gauge, CollectorRegistry
from functools import wraps
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
all_flow = Gauge("all_flow", "x-ui总流量", registry=registry)
all_up_flow = Gauge("all_up_flow", "x-ui总上传流量", registry=registry)
all_down_flow = Gauge("all_down_flow", "x-ui总下载流量", registry=registry)
user_all_flow = Gauge("user_all_flow", "用户总流量", labelnames=['id', 'name', 'protocol'], registry=registry)
user_up_flow = Gauge("user_up_flow", "用户上传流量", labelnames=['id', 'name', 'protocol'], registry=registry)
user_down_flow = Gauge("user_down_flow", "用户下载流量", labelnames=['id', 'name', 'protocol'], registry=registry)


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
        user_up_flow.labels(id=user[0], name=user[5], protocol=user[10]).set(user[2])
        user_down_flow.labels(id=user[0], name=user[5], protocol=user[10]).set(user[3])
        user_all_flow.labels(id=user[0], name=user[5], protocol=user[10]).set(user[2] + user[3])
    all_flow.set(all_up + all_down)
    all_up_flow.set(all_up)
    all_down_flow.set(all_down)
    text = generate_latest(registry)
    return Response(text, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9600)
