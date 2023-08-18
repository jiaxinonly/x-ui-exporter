from flask import Flask, Response, request
from prometheus_client import generate_latest, Gauge, CollectorRegistry
from functools import wraps
import sqlite3

# Create my app
app = Flask(__name__)
registry = CollectorRegistry()
x_ui_all_flow = Gauge("all_flow", "x-ui总流量", registry=registry)
x_ui_all_up_flow = Gauge("all_up_flow", "x-ui总上传流量", registry=registry)
x_ui_all_down_flow = Gauge("all_down_flow", "x-ui总下载流量", registry=registry)
user_all_flow = Gauge("user_flow", "用户总流量", registry=registry)
user_up_flow = Gauge("user_up", "用户上传流量", registry=registry)
user_down_flow = Gauge("user_down", "用户下载流量", registry=registry)


# 身份验证装饰器
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not (auth and auth.username == '' and auth.password == ''):
            return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


@app.route('/metrics')
# @requires_auth
def metrics():  # put application's code here
    connect = sqlite3.connect('x-ui.db')
    cursor = connect.cursor()
    cursor.execute("select * from inbounds")
    data = cursor.fetchall()
    all_up = 0
    all_down = 0
    for user in data:
        all_up += user[2]
        all_down += user[3]
    all = all_up + all_down
    x_ui_all_flow.set(all)
    x_ui_all_up_flow.set(all_up)
    x_ui_all_down_flow.set(all_down)

    text = generate_latest(registry)
    return Response(text, mimetype='text/plain')


if __name__ == '__main__':
    app.run()
