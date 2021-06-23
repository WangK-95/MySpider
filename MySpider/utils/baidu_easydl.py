import requests
import json
import base64

from MySpider import settings


class BaiduEasyDL(object):
    def __init__(self, ak, sk):
        self.ak = ak
        self.sk = sk
        self.access_token = None

    def get_access_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(self.ak, self.sk)
        response = requests.get(host)
        if response.status_code == 200:
            res_json = response.json()
            if 'access_token' in res_json:
                self.access_token = res_json['access_token']

    def verification(self, image_file_path):
        """
        EasyDL 物体检测 调用模型公有云API Python3实现
        """

        if not self.access_token:
            print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
            return None

        # 目标图片的 本地文件路径，支持jpg/png/bmp格式
        # IMAGE_FILE_PATH = "【您的测试图片地址，例如：./example.jpg】"

        # 可选的请求参数
        # threshold: 默认值为建议阈值，请在 我的模型-模型效果-完整评估结果-详细评估 查看建议阈值
        PARAMS = {"threshold": 0.3}

        # 服务详情 中的 接口地址
        MODEL_API_URL = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/zhihu_captcha'

        # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
        # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
        # ACCESS_TOKEN = "【您的ACESS_TOKEN】"
        # API_KEY = "【您的API_KEY】"
        # SECRET_KEY = "【您的SECRET_KEY】"

        # print("1. 读取目标图片 '{}'".format(image_file_path))
        with open(image_file_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_str = base64_data.decode('UTF8')
        # print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
        PARAMS["image"] = base64_str

        # print("3. 向模型接口 'MODEL_API_URL' 发送请求")
        request_url = "{}?access_token={}".format(MODEL_API_URL, self.access_token)
        response = requests.post(url=request_url, json=PARAMS)
        response_json = response.json()
        # response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
        # print("结果:\n{}".format(response_str))
        if response_json and 'results' in response_json:
            if response_json['results'] and 'location' in response_json['results'][0]:
                return response_json['results'][0]['location']['left']
        return None

#
# if __name__ == '__main__':
#     easy_dl = BaiduEasyDL(settings.BAIDU_EASYDL_AK, settings.BAIDU_EASYDL_SK)
#     easy_dl.get_access_token()
#     image_path = '{0}{1}/{2}'.format(settings.STATIC_FILE, 'zhihu_captcha_test', '3848dde174ad4906bcca16167e686cf8.jpg')
#     left_num = easy_dl.verification(image_path)
#     print(left_num)
