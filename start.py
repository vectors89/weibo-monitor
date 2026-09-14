#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Action    : 监控
# Desc      : 启动模块（仅微博版）

import wbmonitor
import requests
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

headers = {
	'Connection': 'Keep-Alive',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Content-Type': 'application/json'
}

# 1. 调用的wxpusher平台
def notify_user(contents, summarys):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	datas = {
		"appToken": os.environ.get('WXPUSHER_APP_TOKEN', ''), # 👈 从环境变量读取
		"content": contents,
		"summary": summarys,
		"contentType": 3, 
		"topicIds": [],
		"uids": [
			os.environ.get('WXPUSHER_UID', '') # 👈 从环境变量读取
		],
		"url": ""
	}
	res = requests.post(url=url, headers=headers, json=datas).json()
	print("WxPusher返回结果:", res)

# 2. 微博格式化和调用推送
def wbweixin(dicts):
	flag = True
	try:
		nickname = dicts.get('nickName', '博主')
		text = dicts.get('text', '')
		pics = dicts.get('pics', [])
		weibo_id = dicts.get('id', '')

		summarys = f"{nickname}发布新微博！"
		contents = f"**【{nickname}】发布了新微博：**\n\n{text}\n\n"
		if pics:
			for img_url in pics:
				contents += f"![图片]({img_url})\n"
		if weibo_id:
			contents += f"\n[👉 点击查看原微博](https://m.weibo.cn/status/{weibo_id})"
			
		notify_user(contents, summarys)
	except Exception as e:
		print("推送出现异常:", e)
		flag = False
	return flag

# 3. 主逻辑
def main():
    # 心跳推送，证明自己活着
    notify_user("心跳测试", "云函数已被触发，正在检查微博...")

    try:
        w = wbmonitor.WBMonitor()
        w.getWBInfo()
        
        # 关键容错：如果历史文件不存在，先创建一个空的
        if not os.path.exists(w.dic):
            os.makedirs(os.path.dirname(w.dic), exist_ok=True)
            with open(w.dic, 'w') as f:
                f.write('')
            print("历史文件不存在，已自动创建")
        else:
            # 如果文件存在但是空的，就先把当前微博存进去，不推送
            with open(w.dic, 'r') as f:
                if f.read().strip() == '':
                    w.getWBQueue()
                    print("历史记录为空，已初始化当前微博")
                    
        # 开始正常监控
        newWB = w.startmonitor()
        if newWB is not None:
            print('抓到新微博，准备推送...')
            wbweixin(newWB)
            notify_user("监控成功", "发现新微博并已推送！")
        else:
            print('没有发现新微博')
            
    except Exception as e:
        notify_user("监控异常", f"执行出错：{str(e)}")

# 4. 阿里云函数入口
def handler(event, context):
    main()
    return "Success"
