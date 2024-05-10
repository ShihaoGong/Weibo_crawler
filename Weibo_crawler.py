# _*_coding:utf-8_*_
# created by Echo_ooo on 2023/08/15 16:17

import queue
import calendar
import csv
import threading
import uuid
import requests
from urllib.parse import quote
from time import sleep
from lxml import etree

class searsh(object):
    ip_queue = queue.Queue() #放ip的队列
    word_queue = queue.Queue() #放关键词的队列
    num=0
    url_list = None
    sock = False
    cookie_flag = 1
    cookies = {
        # "cookie": "SINAGLOBAL=2300498818566.5474.1682585376310; SSOLoginState=1682585750; _s_tentry=weibo.com; Apache=4834696778293.832.1682585758658; ULV=1682585758686:2:2:2:4834696778293.832.1682585758658:1682585376312; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWX9hkHHJjwTQnNii.6AuFB5JpX5KMhUgL.FoMcSK.pe0M4Shq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSo-4eKeN1KBc; ALF=1686147909; SCF=At2pQCbKtJGiA7Z4_8RSVcizDvPWp0aKc4OsubYLZRrmLl3BTHB8d1CLsHIGTuv4hPLyDKessewE-QnoqCfoNro.; SUB=_2A25JXXYWDeRhGeFI7lsQ8ynFzzqIHXVqK-DerDV8PUNbmtANLWr5kW9NfRSEnUG3mOIhq4SN6GLLfK-cmfmSmtnN"
        'cookie':'SINAGLOBAL=2300498818566.5474.1682585376310; UOR=,,login.sina.com.cn; SSOLoginState=1692144893; _s_tentry=weibo.com; Apache=7939235856126.117.1692144901104; ULV=1692144901105:4:2:2:7939235856126.117.1692144901104:1692087425857; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5kxD83jeDLrh6zIfU-k7nW5JpX5KMhUgL.FoM0eh-XS0-Xehq2dJLoI0YLxKnL1heLB.BLxKqL1KqL1hMLxKnL1heLB.BLxKqLB-BLBKqLxKML1-2L1hBLxK-LB-BL1KBLxK-LB-BL1K5t; ALF=1694823311; SCF=At2pQCbKtJGiA7Z4_8RSVcizDvPWp0aKc4OsubYLZRrm8Kzq0FLM2jFxLoVHl8PbXWLXqnV6-eFgJdxGd4_yD0o.; SUB=_2A25J2RbCDeRhGeFN61cV9yvIyzqIHXVqrw8KrDV8PUNbmtANLRDykW9NQJf32CrAe9G0pw5CiOos1VU7rz3Qpnui'}
    aip_list='http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=c9c9d7990de3835a360d8ede9726a685&orderNo=GL20230815162945fsP0pRyJ&count=100&isTxt=1&proxyType=1'
    word_list = ['地铁']
    num_list=queue.Queue()
    lock = threading.Lock()
    def __init__(self):
        pass

    # 用于判断某个月中有多少天
    def month_days_mum(self,year, month):
        return calendar.monthrange(year, month)[1]

    def get_uuid(self):
        s_uuid = str(uuid.uuid4())
        l_uuid = s_uuid.split('-')
        s_uuid = ''.join(l_uuid)
        return s_uuid

    #获取到ip的函数
    def getIp_list(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        url = self.aip_list
        while True:
            try:
                response = requests.get(url=url, headers=headers, timeout=10).text
                break
            except:
                sleep(1)
                continue
        res = response.split('\r\n')

        print(res)
        for i in res:
            self.ip_queue.put({"https":i})
        print('当前ip',self.ip_queue.qsize())


    #拿到单个ip
    def getIp(self):
        print(self.ip_queue.qsize())
        if self.ip_queue.qsize()<5:
                self.getIp_list()
        return self.ip_queue.get()


    #进行数据请求的函数
    def request_url(self,url, ip):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        n = 0
        w = 0
        while True:
            try:
                # print('当前url',url)
                while True:
                  if self.cookie_flag == 1:
                    res = requests.get(url=url, headers=headers, timeout=10, proxies=ip, cookies=self.cookies)
                    res.encoding = 'utf-8'
                    # if len(res.text)<100:
                    #     ip = self.getIp()
                    #     continue
                    if self.cookie_flag ==0:
                        continue
                    # if '转发微博' in res.text:
                    #     with open('12.html', 'a', encoding='utf-8') as f:
                    #         f.write(url+'\n')
                    #         f.write(res.text+ '\n')

                    # if '高级' in res.text:
                    #     self.cookie_flag = 0
                    #     c = input('请换cookie')
                    #     self.cookies = {
                    #         "cookie": c
                    #     }
                    #     self.cookie_flag = 1
                    #     continue

                    break
                  else:
                    sleep(3)
                    continue
                if self.cookie_flag == 1:
                    break
            except:
                if w < 3:
                    w = w + 1
                    continue
                ip = self.getIp()
                n = n + 1
                continue
        return {'res': res, 'ip': ip}

    # 用于判断某个月中有多少天
    def month_days_mum(self,year, month):
        return calendar.monthrange(year, month)[1]
    # 输出 按小时的list
    def time_list(self,min, max):
        all_list = []
        min = min.split('-')
        max = max.split('-')
        min_year = int(min[0])
        min_mounth = int(min[1])
        min_day = int(min[2])

        while True:
            min_time = 0
            if min_year * 360 + min_mounth * 30 + min_day <= int(max[0]) * 360 + int(max[1]) * 30 + int(max[2]):
                while min_time <= 24:
                    if min_mounth < 10:
                        mouth = '0' + str(min_mounth)
                    else:
                        mouth = str(min_mounth)
                    if min_day < 10:

                        all_list.append(
                            str(min_year) + '-' + mouth + '-' + '0' + str(min_day) + '-' + str(min_time))
                    else:
                        all_list.append(
                            str(min_year) + '-' + mouth + '-' + str(min_day) + '-' + str(min_time))
                    min_time = min_time + 1
                if min_day == self.month_days_mum(min_year, min_mounth):
                    min_mounth = min_mounth + 1
                    if min_mounth == 13:
                        min_mounth = 1
                        min_year = min_year + 1
                    min_day = 1
                else:
                    min_day = min_day + 1
            else:
                break
        return all_list

    #文件读取关键词
    def read_text(self):
        with open('关键词.txt','r',encoding='utf-8') as f:
             a=f.read()
             for i in a.split('\n'):
                 self.word_queue.put(i)
    #解析文本
    def jx_text(self,tree,ip):
        global writer
        for li in tree.xpath('//div[@action-type="feed_list_item"]'):
            try:
                id = self.get_uuid()  # 随机id
                ID = li.xpath('./@mid')[0]+'\t' # 文章id
                user_id = li.xpath('.//div[@class="info"]/div[2]/a/@href')[0].split('?')[0].split('/')[3]  # 用户id
                bid = li.xpath('.//div[@class="from"]/a/@href')[0].split('?')[0].split('/')[4]  # 文章mid

                pos = li.xpath('.//div[@class="tag_title_2uq1r tag_cut_17TDH"]/text()')
                if not pos:
                    pos.append('')  # 定位

                name = li.xpath('.//a[@class="name"]/text()')[0]  # 用户名
                date = li.xpath('.//div[@class="from"]/a/text()')[0].strip()  # 时间
                if '年' not in date:
                    date = '2023年'+date

                cbox = li.xpath('.//p[@node-type="feed_list_content_full"]')  # 内容
                cbox = li.xpath('.//p[@node-type="feed_list_content"]')[0] if not cbox else cbox[0]
                cont = ' '.join(cbox.xpath('.//text()')).strip()

                cont=cont.replace('收起 d','')
                tran = li.xpath('.//div[@class="card-act"]/ul/li[1]/a//text()')[1].strip()  # 转发
                try:
                    tran = eval(tran)
                except:
                    tran = 0
                comm = li.xpath('.//div[@class="card-act"]/ul/li[2]/a//text()')[0].strip()  # 评论
                try:
                    comm = eval(comm)
                except:
                    comm = 0
                like = li.xpath('.//span[@class="woo-like-count"]//text()')[0].strip()  # 点赞
                try:
                    like = eval(like)
                except:
                    like = 0
                fa = 0
                user_url = f'https://weibo.com/u/{user_id}'

                url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
                res0 = self.request_url(url, ip)
                res1 = res0['res'].json()
                ip = res0['ip']
                # print(res1)
                followers_count = res1['data']['user']['followers_count'] #粉丝数
                d = res1['data']['user']['location']
                url = f'https://weibo.com/ajax/profile/detail?uid={user_id}'
                res2 = self.request_url(url, ip)
                res2 = res2['res'].json()
                ip = res0['ip']
                if 'ip_location' in res2['data']:
                    d = res2['data']['ip_location'].replace('IP属地：','')
                    if d == '':
                         d = res2['data']['location']
                gender = res1['data']['user']['gender']
                self.lock.acquire()
                writer.writerow([ID,user_id+'\t',d,name,gender,date,like,comm,tran,cont])
                # print([user_id,d,name,followers_count,gender,date,like,comm,tran,cont])
                self.lock.release()

                self.num+=1
            # print('1111')
                print('当前采集',self.num)
                if self.ip_queue.qsize()<5:
                    self.getIp_list()

            except:
                ip = self.getIp()
                continue

        return ip

    def main(self,name):
            # for name in self.word_list:
                # name = self.word_list[0]
                ip = self.getIp()
                while self.num_list.qsize()>0:
                            print('当前采集数为',self.num)
                            print('当前队列剩余元素为：', self.ip_queue.qsize())
                            flag = self.num_list.get()
                            page = 1
                            while page<=50:
                                url = 'https://s.weibo.com/weibo?q=' + quote(name) + '&typeall=1&suball=1&timescope=custom%3A' + \
                                      self.url_list[
                                          flag] + '%3A' + self.url_list[flag + 1] + '&Refer=g&page='+str(page)
                                print(url)
                                res0 = self.request_url(url, ip)
                                res = res0['res']
                                ip = res0['ip']
                                # print(res.text)
                                if '抱歉，未找到' in res.text:
                                    # flag = flag+1
                                    # print(self.url_list[flag])
                                    # continue
                                    break
                                tree = etree.HTML(res.text)
                                ip=self.jx_text(tree,ip)
                                page = page+1
                            # page_liat = tree.xpath('//ul[@class="s-scroll"]/li/a/@href')
                            # for page in page_liat:
                            #     res = self.request_url('https://s.weibo.com' + page,ip)
                            #     ip = res['ip']
                            #     if '抱歉，未找到' in res['res'].text:
                            #         flag = flag + 1
                            #         print(self.url_list[flag])
                            #         continue
                            #     tree = etree.HTML(res['res'].text)
                            #     ip=self.jx_text(tree,ip)
                            flag = flag + 1
                            print('当前：',name, self.url_list[flag])

    #开启线程
    def start(self,name):
        flag = 50
        threads = []
        for i in range(flag):
            t = threading.Thread(target=self.main, args=(name,))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

    #开启线程
    def start_p(self):
        global writer
        for name in self.word_list:
            with open(name + '.csv', 'w', encoding='utf-8', newline="") as f:
            # with open('共享汽车.csv', 'w', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                process_list = []
                self.getIp_list()
                self.url_list = self.time_list('2023-4-30', '2023-8-1')
                for a in range(len(self.url_list)):
                    self.num_list.put(a)
                print(self.num_list.qsize())
                self.start(name)

if __name__=='__main__':
    # 若乱码：用记事本打开-另存为，编码选带有BOM的UTF-8
    # 文档可以实时查看，看数据是否正确
    searsh().start_p()



