import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup


def GetUrl(number):
    dict = {}
    for i in range(1,3):
        try:
            response = requests.get('https://fulibus.net/{}.html/{}'.format(number,i))
            soup = BeautifulSoup(response.content, 'lxml')
            data = soup.find_all('p')
            img_number = 0
            for d in data:
                imgs = d.find_all('img')
                for img in  imgs:
                    img_number += 1
                    picture_url = img.get('src')
                    route_url= '{}-{}-{}'.format(number,i,img_number)
                    dict[route_url] = picture_url
        except requests.exceptions.RequestException as e:
            print(e)
            print('网站无法加载，链接：{}'.format('https://fulibus.net/{}.html/{}'.format(number,i)))
    return dict

def GetPicture(route_url,picture_url):
    route_url_list = route_url.split('-')
    path = os.getcwd()
    path = path + '/{}/{}'.format(route_url_list[0],route_url_list[1])
    os.makedirs(path,exist_ok=True)
    try:
        HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Accept-Encoding': 'gzip, deflate', }
        headers = HEADERS
        headers['user-agent'] = "Mozilla/5.0+(Windows+NT+6.2;+WOW64)+AppleWebKit/537.36+" \
                                "(KHTML,+like+Gecko)+Chrome/45.0.2454.101+Safari/537.36"
        img_file = requests.get(picture_url,allow_redirects=False,timeout=(60, 60),headers=headers)
        if img_file.status_code == 200:
            img_type = img_file.headers.get('content-type')
            if img_type.split('/')[-1] == 'jpeg':
                downPath = path + '/{}.jpg'.format(route_url_list[2])
            else:
                downPath = path + '/{}.{}'.format(route_url_list[2], img_type.split('/')[-1])
            with open(downPath, 'wb') as f:
                f.write(img_file.content)
            return '网站图片下载成功，链接：{}'.format(picture_url)
        else:
            return '网站图片无法加载，下载失败。链接：{}'.format(picture_url)
    except requests.exceptions.RequestException as e:
        print(e)
        return '网站图片无法加载，下载失败。链接：{}'.format(picture_url)


if __name__ == '__main__':
    starttime = time.time()
    issue_start = input("请输入从哪一期开始爬取（例：2020年第1期：输入2020001）\n")
    while issue_start.isdigit() == False or issue_start == '':
        print('请好好输！\n')
        issue_start = input("请输入从哪一期开始爬取（例：2020年第1期：输入2020001）\n")
    issue_end = input("请输入从哪一期结束爬取（例：2020年第58期：输入2020058）\n")
    while issue_end.isdigit() == False or issue_end == '' or issue_end < issue_start:
        print('请好好输！\n')
        issue_end = input("请输入从哪一期结束爬取（例：2020年第58期：输入2020058）\n")
    issue_start = int(issue_start)
    issue_end = int(issue_end) + 1
    print('开始下载，请稍候。。。。。。')
    task_list = []
    init_data = {}
    with ThreadPoolExecutor(max_workers=16) as executor:
        for i in range(issue_start, issue_end):
            task = executor.submit(GetUrl,i)
            task_list.append(task)
        for res in as_completed(task_list):
            init_data.update(res.result())
    # pprint(init_data)
    task_list = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for key in init_data:
            task = executor.submit(GetPicture,key,init_data[key])
            task_list.append(task)
        for res in as_completed(task_list):
            print(res.result())
    endtime = time.time()
    print('已全部下载完成！请在当前路径下查看！用时：{}'.format(endtime - starttime))
    print('Enjoy it')
    print('Powered by 所向披靡\n')
    key = input('按回车键退出\n')
    while key != '':
        key = input('按回车键退出\n')