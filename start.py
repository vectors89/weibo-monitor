import os
import requests

print("===== 开始自我体检 =====")
print("1. 正在检查 Token 状态...")
token = os.environ.get('WXPUSHER_APP_TOKEN', '')
print("Token 是否获取成功:", "成功" if token else "失败 (为空)")

print("2. 正在检查 UID 状态...")
uid = os.environ.get('WXPUSHER_UID', '')
print("UID 是否获取成功:", "成功" if uid else "失败 (为空)")

print("3. 正在尝试发送 WxPusher...")
url = 'https://wxpusher.zjiecode.com/api/send/message'
datas = {
    "appToken": token,
    "content": "来自 GitHub Actions 的强制测试消息",
    "summary": "测试推送",
    "contentType": 1,
    "uids": [uid]
}
res = requests.post(url, json=datas).json()
print("WxPusher 返回结果:", res)
print("===== 体检结束 =====")
