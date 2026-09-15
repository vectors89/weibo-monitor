#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Action    : 监控
# Desc      : 启动模块（仅微博版）

import wbmonitor
import requests
import ssl
import os
import time  # 👈 必须加上这个，用于间隔推送

ssl._create_default_https_context = ssl._create_unverified_context

headers = {
	'Connection': 'Keep-Alive',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Content-Type': 'application/json'
}

# 调用的wxpusher平台
def notify_user(contents, summarys):
	url = 'https://wxpusher.zjiecode.com/api/send/message'
	datas = {
		"appToken": os.environ.get('WXPUSHER_APP_TOKEN', ''),
		"content": contents,
		"summary": summarys,
		"contentType": 3, 
		"topicIds": [],
		"uids": [os.environ.get('WXPUSHER_UID', '')],
		"url": ""
	}
	try:
		res = requests.post(url=url, headers=headers, json=datas).json()
		print("WxPusher返回结果:", res)
	except Exception as e:
		print("推送网络请求失败:", e)

def wbweixin(dicts):
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

def main():
    try:
        w = wbmonitor.WBMonitor()
        w.getWBInfo()
        
        if not os.path.exists(w.dic):
            w.getWBQueue()
        else:
            with open(w.dic, 'r') as f:
                if f.read().strip() == '':
                    w.getWBQueue()
                    
        newWBs = w.startmonitor()  # 👈 接收列表
        if newWBs:
            print(f'抓到 {len(newWBs)} 条新微博，准备推送...')
            for item in newWBs:  # 👈 遍历每一条微博
                wbweixin(item)
                time.sleep(2)  # 👈 关键：暂停2秒，防止WxPusher接口拦截
            print('推送完成')
        else:
            print('没有发现新微博')
    except Exception as e:
        print("执行出错:", e)

def handler(event, context):
    main()
    return "Success"

if __name__ == '__main__':
    main()
