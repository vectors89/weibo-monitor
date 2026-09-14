import os
import requests
import wbmonitor

# 1. 先打印环境变量，看看有没有读取到
print("===== 环境检查 =====")
print("AppToken是否读取到:", "Yes" if os.environ.get('WXPUSHER_APP_TOKEN') else "No ❌")
print("UID是否读取到:", "Yes" if os.environ.get('WXPUSHER_UID') else "No ❌")
print("Cookie是否读取到:", "Yes" if os.environ.get('WEIBO_COOKIE') else "No ❌")

# 2. 只要前面的打印能出来，说明基本环境是好的
print("===== 开始测试推送 =====")
url = 'http://wxpusher.zjiecode.com/api/send/message'
datas = {
    "appToken": os.environ.get('WXPUSHER_APP_TOKEN', ''),
    "content": "来自 GitHub Actions 的强制测试消息",
    "summary": "测试推送",
    "contentType": 1,
    "uids": [os.environ.get('WXPUSHER_UID', '')]
}
res = requests.post(url, json=datas).json()
print("WxPusher返回结果:", res)
print("===== 测试结束 =====")
