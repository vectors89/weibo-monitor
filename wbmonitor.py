    def startmonitor(self):
        new_items = []  # 👈 改成列表，用来装多条微博
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
                print(f"处理微博 {i} 时出错: {e}")
                
        return new_items  # 👈 返回列表
