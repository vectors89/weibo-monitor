import os
import requests

print("===== 检查密码 =====")
token = os.environ.get('WXPUSHER_APP_TOKEN')
uid = os.environ.get('WXPUSHER_UID')

print("Token 长度:", len(token) if token else 0)
print("UID 长度:", len(uid) if uid else 0)

if not token or not uid:
    print("❌ 错误：密码没读取到，请检查 GitHub Secrets 名字是否完全一致！")
else:
    print("===== 尝试发送 =====")
    url = 'https://wxpusher.zjiecode.com/api/send/message'
    data = {
        "appToken": token,
        "content": "第一阶段测试成功！GitHub 已经能通过 WxPusher 发消息了！",
        "summary": "连通测试",
        "contentType": 1,
        "uids": [uid]
    }
    res = requests.post(url, json=data).json()
    print("WxPusher 返回结果:", res)
