import time
import requests
from bs4 import BeautifulSoup
import os
import sys
import threading

# 定义爬取福利吧的任务
def scrawler(issue_start,issue_end,page):
    for i in range(issue_start, issue_end):
        try:
            response = requests.get('https://fulibus.net/%s.html/%s' % (str(i), page), timeout=(30, 30))
            path = os.path.abspath('.')
            lujing = path + './%s/%s' % (str(i), page)
            try:
                os.makedirs(lujing)
            except FileExistsError as e:
                print(str(e) + '请删除该目录,再重新运行.')
                sys.exit()
            soup = BeautifulSoup(response.content, 'lxml')
            data = soup.find_all('p')
            dnumber = 0
            inumber = 0
            print('网页' + str(i) + '开始下载第%s页...'%page)
            for d in data:
                dnumber += 1
                imgs = d.find_all('img')
                for img in imgs:
                    inumber += 1
                    tupian_url = img.get('src')
                    print(tupian_url)
                    count = str(i) + '-' + page + '-' + str(dnumber) + '-' + str(inumber)
                    print('正在下载' + count + '的图片')
                    try:
                        img_file = requests.get(tupian_url, timeout=(30, 30))
                        if img_file.status_code == 200:
                            img_type = img_file.headers.get('content-type')
                            if img_type.split('/')[-1] == 'jpeg':
                                downPath = lujing + '.\\%s.jpg' % count
                            else:
                                downPath = lujing + '.\\%s.%s' % (count, img_type.split('/')[-1])
                            with open(downPath, 'wb') as f:
                                f.write(img_file.content)
                        else:
                            print('网站图片无法加载,下载失败')
                    except requests.exceptions.RequestException as e:
                        print(e)
                        print('网站图片无法加载,下载失败')
            print('网页' + str(i) + '第%s页图片已下载完成!\n'%page)
        except requests.exceptions.RequestException as e:
            print(e)
            print('网站加载失败')

issue_start = input("请输入爬取哪一期开始(例:2019年第1期:输入2019001)\n")
while issue_start.isdigit() == False or issue_start=='':
    print('请好好输!\n')
    issue_start = input("请输入爬取哪一期开始(例:2019年第1期:输入2019001)\n")
issue_end = input("请输入爬取哪一期结束(例:2019年第96期:输入2019096)\n")
while issue_end.isdigit() == False or issue_end=='':
    print('请好好输!\n')
    issue_end = input("请输入爬取哪一期结束(例:2019年第100期:输入2019100)\n")
issue_start=int(issue_start)
issue_end = int(issue_end) + 1

# 创建两个线程同时下载
thread1 = threading.Thread(target=scrawler,args=(issue_start,issue_end,str(1)))
thread2 = threading.Thread(target=scrawler,args=(issue_start,issue_end,str(2)))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

print('已全部下载完成!请在当前路径下查看\n')
print('Enjoy it')
print('Powered by Wanglu')
key = input('按回车键退出\n')
while key!='':
    key = input('按回车键退出\n')
