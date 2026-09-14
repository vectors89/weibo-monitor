import os
import requests

# 这是一个极简的强制推送函数
def force_notify(token, uid, message):
    url = 'https://wxpusher.zjiecode.com/api/send/message'
    datas = {
        "appToken": token,
        "content": message,
        "summary": "GitHub Actions 体检报告",
        "contentType": 1,
        "uids": [uid]
    }
    try:
        res = requests.post(url, json=datas, timeout=10).json()
        print("发送请求返回:", res)
    except Exception as e:
        print("发送请求失败:", e)

# 开始体检
print("===== 开始体检 =====")

# 1. 读取 Secrets
token = os.environ.get('WXPUSHER_APP_TOKEN', '')
uid = os.environ.get('WXPUSHER_UID', '')
cookie = os.environ.get('WEIBO_COOKIE', '')

# 2. 检查是否有值
print("Token长度:", len(token))
print("UID长度:", len(uid))
print("Cookie长度:", len(cookie))

# 3. 强行给微信发一条通知，无论有没有错误
msg = f"体检结果:\nToken长度={len(token)}\nUID长度={len(uid)}\nCookie长度={len(cookie)}"
force_notify(token, uid, msg)

print("===== 体检结束 =====")
