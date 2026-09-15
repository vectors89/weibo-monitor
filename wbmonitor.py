#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Action    : 微博
# Desc      : 微博主模块

import requests
import json
import sys
import os

class WBMonitor():
    def __init__(self):
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cookie': os.environ.get('WEIBO_COOKIE', '')
        }
        # ========= 这里可以改你要监控的微博UID =========
        self.uid = ['1002568141', '7996057394'] 
        # =============================================
        self.dic = 'wbIds.txt'

    # 获取访问连接
    def getWBInfo(self):
        self.weiboInfo = []
        for i in self.uid:
            userInfo = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s' % (i)
            res = requests.get(userInfo, headers=self.reqHeaders)

            try:
                data = res.json()
                if 'data' not in data or 'tabsInfo' not in data['data']:
                    print("⚠️ 微博没有返回预期数据，实际返回内容如下：")
                    print(res.text)
                    continue
                
                for j in data['data']['tabsInfo']['tabs']:
                    if j['tab_type'] == 'weibo':
                        self.weiboInfo.append('https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s' % (i, j['containerid']))
            except Exception as e:
                print("❌ 解析出错:", e)
                print(res.text)

    # 收集已经发布动态的id
    def getWBQueue(self):
        self.itemIds = []
        for i in self.weiboInfo:
            res = requests.get(i, headers=self.reqHeaders)
            with open(self.dic, 'a') as f:
                for j in res.json()['data']['cards']:
                    if j['card_type'] == 9:
                        f.write(j['mblog']['id'] + '\n')
                        self.itemIds.append(j['mblog']['id'])
        self.echoMsg('Info', '微博数目获取成功')
        self.echoMsg('Info', '目前有 %s 条微博' % len(self.itemIds))

    # 开始监控（收集所有新微博，返回列表）
    def startmonitor(self):
        new_items = []  # 👈 改为收集列表
        itemIds = []
        if os.path.exists(self.dic):
            with open(self.dic, 'r') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    itemIds.append(line)
                
        for i in self.weiboInfo:
            try:
                res = requests.get(i, headers=self.reqHeaders)
                data = res.json()
                if 'data' not in data or 'cards' not in data['data']:
                    print(f"⚠️ 获取微博内容失败，UID: {i}")
                    continue
                
                for j in data['data']['cards']:
                    if j['card_type'] == 9:
                        if str(j['mblog']['id']) not in itemIds:
                            with open(self.dic, 'a') as f:
                                f.write(j['mblog']['id'] + '\n')
                            
                            returnDict = {}
                            returnDict['id'] = j['mblog']['id']
                            returnDict['text'] = j['mblog']['text']
                            returnDict['nickName'] = j['mblog']['user']['screen_name']
                            returnDict['pics'] = []
                            if 'pics' in j['mblog']:
                                for pic in j['mblog']['pics']:
                                    img_url = pic.get('large', {}).get('url') or pic.get('url')
                                    if img_url:
                                        returnDict['pics'].append(img_url)
                            
                            new_items.append(returnDict)  # 👈 收集而不是直接返回
            except Exception as e:
                print(f"❌ 处理微博 {i} 时出错: {e}")
                
        return new_items  # 👈 返回列表

    # 格式化输出
    def echoMsg(self, level, msg):
        if level == 'Info':
            print('[Info] %s' % msg)
        elif level == 'Error':
            print('[Error] %s' % msg)
