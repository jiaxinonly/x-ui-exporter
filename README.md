# x-ui-exporter
> x-ui面板的prometheus exporter，可以获取数据库中面板流量和用户流量，支持Basic Auth  
> txy分支添加了腾讯云共享流量包数据和钉钉机器人通知
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
3. 修改lib.flow_packet下的腾讯云ak和区域
   ```python
   SecretId = "" # 腾讯云ak
   SecretKey = "" # 腾讯云ak
   Region = "ap-hongkong" # 区域参考腾讯云官方
   ```
4. 修改lib.dingding_notice下的钉钉机器人token
   ```python
   token = "" # 钉钉机器人token
   ```
3. 启动x-ui-exporter
   ```shell
   python app.py 
   ```

## 效果
```text
# HELP x_ui_all_flow_bytes x-ui总流量
# TYPE x_ui_all_flow_bytes gauge
x_ui_all_flow_bytes 3.62665272896e+011
# HELP x_ui_all_up_flow_bytes x-ui总上传流量
# TYPE x_ui_all_up_flow_bytes gauge
x_ui_all_up_flow_bytes 7.715872942e+09
# HELP x_ui_all_down_flow_bytes x-ui总下载流量
# TYPE x_ui_all_down_flow_bytes gauge
x_ui_all_down_flow_bytes 3.54949399954e+011
# HELP x_ui_user_all_flow_bytes 用户总流量
# TYPE x_ui_user_all_flow_bytes gauge
x_ui_user_all_flow_bytes{id="1",name="test1",protocol="vmess"} 2.15725332162e+011
x_ui_user_all_flow_bytes{id="2",name="test2",protocol="vless"} 8.0208273818e+010
x_ui_user_all_flow_bytes{id="3",name="test3",protocol="trojan"} 5.7343541135e+010
# HELP x_ui_user_up_flow_bytes 用户上传流量
# TYPE x_ui_user_up_flow_bytes gauge
x_ui_user_up_flow_bytes{id="1",name="test1",protocol="vmess"} 3.314052106e+09
x_ui_user_up_flow_bytes{id="2",name="test2",protocol="vless"} 2.248560931e+09
x_ui_user_up_flow_bytes{id="3",name="test3",protocol="trojan"} 2.025554928e+09
# HELP x_ui_user_down_flow_bytes 用户下载流量
# TYPE x_ui_user_down_flow_bytes gauge
x_ui_user_down_flow_bytes{id="1",name="test1",protocol="vmess"} 2.12411280056e+011
x_ui_user_down_flow_bytes{id="2",name="test2",protocol="vless"} 7.7959712887e+010
x_ui_user_down_flow_bytes{id="3",name="test3",protocol="trojan"} 5.5317986207e+010
# TYPE txy_all_flow_packet_total_amount_Gbytes gauge
txy_all_flow_packet_total_amount_Gbytes 300.0
# HELP txy_all_flow_packet_remaining_amount_Gbytes 腾讯云所有共享流量包剩余量
# TYPE txy_all_flow_packet_remaining_amount_Gbytes gauge
txy_all_flow_packet_remaining_amount_Gbytes 149.83
# HELP txy_all_flow_packet_used_amount_Gbytes 腾讯云所有共享流量包使用量
# TYPE txy_all_flow_packet_used_amount_Gbytes gauge
txy_all_flow_packet_used_amount_Gbytes 150.17
# HELP txy_flow_packet_total_amount_Gbytes 腾讯云流量包总量
# TYPE txy_flow_packet_total_amount_Gbytes gauge
txy_flow_packet_total_amount_Gbytes{id="tfp-LgzE6nmJ",name="未命名",type="FULL_TIME"} 300.0
# HELP txy_flow_packet_remaining_amount_Gbytes 腾讯云流量包剩余量
# TYPE txy_flow_packet_remaining_amount_Gbytes gauge
txy_flow_packet_remaining_amount_Gbytes{id="tfp-LgzE6nmJ",name="未命名",type="FULL_TIME"} 149.83
# HELP txy_flow_packet_used_amount_Gbytes 腾讯云流量包使用量
# TYPE txy_flow_packet_used_amount_Gbytes gauge
txy_flow_packet_used_amount_Gbytes{id="tfp-LgzE6nmJ",name="未命名",type="FULL_TIME"} 150.17
```