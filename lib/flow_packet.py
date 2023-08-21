import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models

SecretId = ""
SecretKey = ""
Region = "ap-hongkong"


def get_txy_share_flow_packet():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "vpc.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = vpc_client.VpcClient(cred, Region, clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeTrafficPackagesRequest()
        params = {
            "Filters": [
                {
                    "Name": "status",
                    "Values": ["AVAILABLE"]
                }
            ]
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeTrafficPackagesResponse的实例，与请求对象对应
        resp = client.DescribeTrafficPackages(req)
        # 输出json格式的字符串回包
        resp = json.loads(resp.to_json_string())
        all_remaining_amount = 0
        all_used_amount = 0
        for package in resp['TrafficPackageSet']:
            all_remaining_amount += package['RemainingAmount']
            all_used_amount += package['UsedAmount']
        all_total_amount = all_remaining_amount + all_used_amount
        data = {"AllTotalAmount": all_total_amount, "AllRemainingAmount": all_remaining_amount,
                "AllUsedAmount": all_used_amount, 'TrafficPackageSet': resp['TrafficPackageSet']}
        return data


    except TencentCloudSDKException as err:
        print(err)


if __name__ == '__main__':
    data = get_txy_share_flow_packet()
    print(data)
