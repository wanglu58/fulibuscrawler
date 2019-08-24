import time
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import sys
import socket
socket.setdefaulttimeout(30)
issue_start = input("请输入爬取哪一期开始(例:2019年第1期:输入2019001)\n")
while issue_start.isdigit() == False or issue_start=='':
    print('请好好输!\n')
    issue_start = input("请输入爬取哪一期开始(例:2019年第1期:输入2019001)\n")
issue_end = input("请输入爬取哪一期结束(例:2019年第96期:输入2019096)\n")
while issue_end.isdigit() == False or issue_end=='':
    print('请好好输!\n')
    issue_end = input("请输入爬取哪一期结束(例:2019年第96期:输入2019096)\n")
issue_start=int(issue_start)
issue_end = int(issue_end) + 1
for i in range(issue_start,issue_end):
    try:
        response = requests.get('https://fulibus.net/%d.html/%d'%(i,1))
    except requests.exceptions.ConnectionError:
        print('没有网络,退出!')
        sys.exit()
    path = os.path.abspath('.')
    lujing = path+'./%d/%d'%(i,1)
    try:
        os.makedirs(lujing)
    except FileExistsError as e:
        print(str(e)+'请删除该目录,再重新运行.')
        sys.exit()
    soup=BeautifulSoup(response.content,'lxml')
    data = soup.find_all('p')
    dnumber = 0
    inumber = 0
    print('网页'+str(i)+'开始下载第一页...')
    for d in data:
        dnumber += 1
        imgs=d.find_all('img')
        for img in imgs:
            tupian_url = img.get('src')
            print(tupian_url)
            list_data = tupian_url.split('.')
            houzhui = list_data[-1]
            inumber = inumber + 1
            count = str(i)+'-' +str(1)+'-'+ str(dnumber)+'-'+str(inumber)
            if houzhui == 'gif':
                downPath = lujing+'.\\%s.gif'%count
            if houzhui == 'jpg':
                downPath = lujing+'.\\%s.jpg' % count
            print('正在下载'+count+'的图片')
            try:
                urllib.request.urlretrieve(tupian_url, downPath)
            except urllib.request.URLError as err:
                print(err)
                print('网站图片无法加载,下载失败')
            except socket.timeout as e:
                print(e)
                print('网站图片无法加载,下载失败')            
    print('网页'+str(i)+'第一页图片已下载完成!\n')
    print('网页'+str(i)+'开始下载第二页...')
    try:
        response = requests.get('https://fulibus.net/%d.html/%d'%(i,2))
    except requests.exceptions.ConnectionError:
        print('没有网络,退出!')
        sys.exit()
    path = os.path.abspath('.')
    lujing = path+'./%d/%d'%(i,2)
    try:
        os.makedirs(lujing)
    except FileExistsError as e:
        print(str(e)+'请删除该目录,再重新运行.')
        sys.exit()
    soup=BeautifulSoup(response.content,'lxml')
    data = soup.find_all('p')
    dnumber = 0
    inumber = 0
    for d in data:
        dnumber += 1
        imgs=d.find_all('img')
        for img in imgs:
            tupian_url = img.get('src')
            print(tupian_url)
            list_data = tupian_url.split('.')
            houzhui = list_data[-1]
            inumber = inumber + 1
            count = str(i)+'-' +str(1)+'-'+ str(dnumber)+'-'+str(inumber)
            if houzhui == 'gif':
                downPath = lujing+'.\\%s.gif'%count
            if houzhui == 'jpg':
                downPath = lujing+'.\\%s.jpg' % count
            print('正在下载'+count+'的图片')
            try:
                urllib.request.urlretrieve(tupian_url, downPath)
            except urllib.request.URLError as err:
                print(err)
                print('网站图片无法加载,下载失败')
            except socket.timeout as e:
                print(e)
                print('网站图片无法加载,下载失败')
    print('网页'+str(i)+'第二页图片已下载完成!\n')
print('已全部下载完成!请在当前路径下查看\n')
key = input('按回车键退出\n')
while key!='':
    key = input('按回车键退出\n')
print('Enjoy it')
print('Powered by Wanglu')
time.sleep(3)