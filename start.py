import os
import requests

print("===== 开始体检 =====")
token = os.environ.get('WXPUSHER_APP_TOKEN', '')
uid = os.environ.get('WXPUSHER_UID', '')
cookie = os.environ.get('WEIBO_COOKIE', '')

print(f"Token长度: {len(token)}")
print(f"UID长度: {len(uid)}")
print(f"Cookie长度: {len(cookie)}")

if not token or not uid:
    print("❌ 致命错误：Token 或 UID 为空！请检查 GitHub Secrets 配置。")
else:
    print("尝试发送测试消息...")
    url = 'https://wxpusher.zjiecode.com/api/send/message'
    datas = {
        "appToken": token,
        "content": "GitHub Actions 体检测试",
        "summary": "体检报告",
        "contentType": 1,
        "uids": [uid]
    }
    try:
        res = requests.post(url, json=datas, timeout=10).json()
        print("WxPusher 返回结果:", res)
    except Exception as e:
        print("发送请求失败，错误信息:", e)

print("===== 体检结束 =====")
