import requests
from django.conf import settings

class WeChatPushService:
    def __init__(self):
        self.appid = settings.WECHAT_MINI_APP['APPID']
        self.secret = settings.WECHAT_MINI_APP['SECRET']
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}'
        response = requests.get(url)
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        raise Exception(f'获取access_token失败: {data}')
    
    def send_message(self, openid, template_id, data):
        url = f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={self.access_token}'
        payload = {
            'touser': openid,
            'template_id': template_id,
            'data': data
        }
        response = requests.post(url, json=payload)
        return response.json()
