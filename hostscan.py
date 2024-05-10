# -*- coding: UTF-8 -*-

import requests
import re
requests.packages.urllib3.disable_warnings()
import concurrent.futures
import argparse
import json
import random

def hostscan(ip,hostfile):
    #用于存放有效结果
    lists=[]
    
    myuseragentlist = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
    ]

    http_s = ['http://','https://']
    for h in http_s :
        for hostlist in open(hostfile,'r'):
            host=hostlist.strip('\n')
            #print(host)
            #headers = {'Host':host,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            
            #随机选择一个User-Agent,防止被封
            headers = {'Host':host,'User-Agent':random.choice(myuseragentlist)}
            #print(headers)

            try:
                r = requests.session()
                #print(ip)
                rhost = r.get(h + ip,verify=False,headers=headers,timeout=5)
                rhost.encoding='utf-8'
                #title = re.search('<title>(.*)</title>', rhost.text).group(1) #获取标题
                #titles.append(title)
                #info = '{}{}  |  Host: {} | Size: {}  | status_code: {} | tittle: {}'.format(h, ip, host, len(rhost.text), rhost.status_code, title)
                if rhost.status_code!=404:
                    info = '{}{}  |  Host: {} | Size: {}  | status_code: {} '.format(h, ip, host, len(rhost.text), rhost.status_code)
                    lists.append(info)

            except Exception :
                error = h + ip + " --- " + host + " --- 访问失败！~"
                print(error)

            resultfile ='./result/{}.txt'.format(ip)
            with open(resultfile, 'w+') as f:
                for i in lists:
                    f.write(i + "\n")

#文件参数
#hostfile = './hosts.txt'
#ipfile = './ips.txt'

parser = argparse.ArgumentParser(description='host碰撞辅助测试脚本      作者Yan')
parser.add_argument('-I', '--ipfile', help='保存ip列表的文件')
parser.add_argument('-D', '--hostfile', help='保存host列表的文件')
args = parser.parse_args()

print("====================================开 始 匹 配====================================")
#读取IP地址
with open(args.ipfile, "r") as f:
    iplist = f.readlines()

#使用线程池并发扫描
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 使用列表推导式创建一个包含多个 Future 对象的列表,executor.submit(提交给线程池的函数，函数的参数1，函数的参数2……)
    futures = [executor.submit(hostscan, ip.strip(),args.hostfile) for ip in iplist]

print("结果已经写入 /result/ip.txt 中")