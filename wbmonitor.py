#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 微博
# Desc      : 微博主模块
# 添加新uid时，自行清空上一层里的微博id列表

import requests,json,sys

class WBMonitor():
    def __init__(self):
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cookie': 'XSRF-TOKEN=4564c6;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhhhBjMlgDHkZmpZ4QBjQzy5NHD95QNSKz71hM41KzRWs4Dqc_Ii--fi-2fi-i2i--fi-82i-2ci--NiK.XiKLsi--ci-z7i-zRi--Ri-isiKLhi--4iK.4i-8Wi--Xi-i2i-27i--fiKLhi-2Ri--Ri-zNi-8si--Xi-zRiKyW;MLOGIN=1;SUB=_2A25Hp_cbDeRhGeFL6VIZ9yfFyTSIHXVk3XbTrDV6PUJbktAbLWn4kW1NQkPtIFgE8EwWlpcFan4J6P4N4D_EudIq;ALF=1791693899;_T_WM=57525525339;M_WEIBOCN_PARAMS=uicode%3D20000174;SCF=Al_988sGYuw2b4CRhQHGKZXrEe99igeVFxITAV8Eso7mVXt-Fb7nNB7e370BAEUiMGIJ4V4noTy8BOV1EhM_u6A.;SSOLoginState=1789101899;WEIBOCN_FROM=1110006030'
        }
        # 这里添加关注人的uid
        self.uid = ['1002568141', '7996057394'] 
        self.dic = '/tmp/wbIds.txt'

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
                    continue # 跳过当前uid，继续下一个
                
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

    # 开始监控
    def startmonitor(self):
        returnDict = {}
        itemIds = []
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
                            self.echoMsg('Info', '发微博啦!!!')
                            self.echoMsg('Info', '目前有 %s 条微博' % (len(itemIds) + 1))
                            returnDict['id'] = j['mblog']['id']  # 新增：用于拼接原微博链接
                            returnDict['created_at'] = j['mblog']['created_at']
                            returnDict['text'] = j['mblog']['text']
                            returnDict['source'] = j['mblog']['source']
                            returnDict['nickName'] = j['mblog']['user']['screen_name']
                            
                            # 新增：提取图片链接
                                                      # 提取图片（增强兼容性）
                            returnDict['pics'] = []
                            if 'pics' in j['mblog']:
                                for pic in j['mblog']['pics']:
                                    # 优先取大图，没有大图就取原图
                                    img_url = pic.get('large', {}).get('url') or pic.get('url')
                                    if img_url:
                                        returnDict['pics'].append(img_url)
                                    
                            return returnDict
            except Exception as e:
                print(f"❌ 处理微博 {i} 时出错: {e}")

    # 格式化输出
    def echoMsg(self, level, msg):
        if level == 'Info':
            print('[Info] %s' % msg)
        elif level == 'Error':
            print('[Error] %s' % msg)
