# x-ui-exporter
> x-ui面板的promethues exporter，可以获取数据库中面板流量和用户流量，支持Basic Auth

## 使用说明
> 需要python3环境，默认监听9600端口
1. 安装依赖
   ```shell
   pip install -r requirements.txt
   ```
2. 根据需求修改app.py文件
   ```python
   # 数据库地址
   DB_PATH = "/etc/x-ui/x-ui.db"
   # 是否要求鉴权
   REQ_AUTH = False
   # 如果需要鉴权，设置账号密码
   username = ""
   password = ""
   ```
3. 启动x-ui-exporter
   ```shell
   python app.py 
   ```

## 效果
```text
# HELP all_flow x-ui总流量
# TYPE all_flow gauge
all_flow 3.62665272896e+011
# HELP all_up_flow x-ui总上传流量
# TYPE all_up_flow gauge
all_up_flow 7.715872942e+09
# HELP all_down_flow x-ui总下载流量
# TYPE all_down_flow gauge
all_down_flow 3.54949399954e+011
# HELP user_all_flow 用户总流量
# TYPE user_all_flow gauge
user_all_flow{id="1",name="test1",protocol="vmess"} 2.15725332162e+011
user_all_flow{id="2",name="test2",protocol="vless"} 8.0208273818e+010
user_all_flow{id="3",name="test3",protocol="trojan"} 5.7343541135e+010
# HELP user_up_flow 用户上传流量
# TYPE user_up_flow gauge
user_up_flow{id="1",name="test1",protocol="vmess"} 3.314052106e+09
user_up_flow{id="2",name="test2",protocol="vless"} 2.248560931e+09
user_up_flow{id="3",name="test3",protocol="trojan"} 2.025554928e+09
# HELP user_down_flow 用户下载流量
# TYPE user_down_flow gauge
user_down_flow{id="1",name="test1",protocol="vmess"} 2.12411280056e+011
user_down_flow{id="2",name="test2",protocol="vless"} 7.7959712887e+010
user_down_flow{id="3",name="test3",protocol="trojan"} 5.5317986207e+010
```