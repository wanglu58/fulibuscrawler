import os
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup


def GetUrl(number):
    dict = {}
    video_list = []
    video_number = 0
    i = 1
    try:
        response = requests.get('https://fulibus.net/{}.html'.format(number))
        soup = BeautifulSoup(response.content, 'lxml')
        page = len(soup.find('div', attrs={'class': 'article-paging'}).find_all('a')) + 2
        for i in range(1,page):
            if i != 1:
                response = requests.get('https://fulibus.net/{}.html/{}'.format(number,i))
                soup = BeautifulSoup(response.content, 'lxml')
            data = soup.find_all('p')
            img_number = 0
            for d in data:
                if i == 1:
                    for item in d.find_all('a'):
                        if item.get('rel') and item.string != item.get('href') and not item.get('title'):
                            video_number += 1
                            video_list.append({
                                'number': video_number,
                                'title': item.string,
                                'href': item['href']
                            })
                for img in  d.find_all('img'):
                    img_number += 1
                    picture_url = img.get('src')
                    route_url= '{}-{}-{}'.format(number,i,img_number)
                    dict[route_url] = picture_url
            if video_list:
                dict['{}'.format(number)] = video_list
    except requests.exceptions.RequestException as e:
        print(e)
        print('{0}期网站无法加载，链接：https://fulibus.net/{0}.html/{1}'.format(number, i))
    return dict

def GetData(route_url,data):
    route_url_list = route_url.split('-')
    path = os.getcwd()
    if len(route_url_list) == 3:
        path = path + '/{}/{}'.format(route_url_list[0],route_url_list[1])
        os.makedirs(path,exist_ok=True)
        try:
            HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Accept-Encoding': 'gzip, deflate', }
            headers = HEADERS
            headers['user-agent'] = "Mozilla/5.0+(Windows+NT+6.2;+WOW64)+AppleWebKit/537.36+" \
                                    "(KHTML,+like+Gecko)+Chrome/45.0.2454.101+Safari/537.36"
            img_file = requests.get(data,allow_redirects=False,timeout=(60, 60),headers=headers)
            if img_file.status_code == 200:
                img_type = img_file.headers.get('content-type')
                if img_type.split('/')[-1] == 'jpeg':
                    downPath = path + '/{}.jpg'.format(route_url_list[2])
                else:
                    downPath = path + '/{}.{}'.format(route_url_list[2], img_type.split('/')[-1])
                with open(downPath, 'wb') as f:
                    f.write(img_file.content)
                return '{}期第{}页第{}张图片下载成功，链接：{}'.format(
                    route_url_list[0],route_url_list[1],route_url_list[2],data)
            else:
                return '{}期第{}页第{}张图片下载失败，链接：{}'.format(
                    route_url_list[0], route_url_list[1], route_url_list[2], data)
        except requests.exceptions.RequestException as e:
            print(e)
            return '{}期第{}页第{}张图片下载失败，链接：{}'.format(
                route_url_list[0], route_url_list[1], route_url_list[2], data)
    else:
        path = path + '/{}'.format(route_url_list[0])
        os.makedirs(path, exist_ok=True)
        with open(path+'/热门视频.txt','w',encoding='utf-8') as f:
            for i in data:
                f.write('{}、{}'.format(i['number'],i['title']))
                f.write('\n')
                f.write(i['href'])
                f.write('\n')
        return '{}期热门视频链接保存成功。'.format(route_url)


if __name__ == '__main__':
    issue_start = input("请输入从哪一期开始爬取（例：2020年第1期：输入2020001）\n")
    while issue_start.isdigit() == False or issue_start == '':
        print('请好好输！\n')
        issue_start = input("请输入从哪一期开始爬取（例：2020年第1期：输入2020001）\n")
    issue_end = input("请输入从哪一期结束爬取（例：2020年第60期：输入2020060）\n")
    while issue_end.isdigit() == False or issue_end == '' or issue_end < issue_start:
        print('请好好输！\n')
        issue_end = input("请输入从哪一期结束爬取（例：2020年第60期：输入2020060）\n")
    issue_start = int(issue_start)
    issue_end = int(issue_end) + 1
    starttime = datetime.datetime.now()
    print('开始下载，请稍候。。。。。。')
    task_list = []
    init_data = {}
    with ThreadPoolExecutor() as executor:
        for i in range(issue_start, issue_end):
            task = executor.submit(GetUrl,i)
            task_list.append(task)
        for res in as_completed(task_list):
            init_data.update(res.result())
    # print(init_data)
    task_list = []
    with ThreadPoolExecutor() as executor:
        for key in init_data:
            task = executor.submit(GetData,key,init_data[key])
            task_list.append(task)
        for res in as_completed(task_list):
            print(res.result())
    endtime = datetime.datetime.now()
    print('已全部下载完成！请在当前路径下查看！用时：{}秒'.format(int((endtime-starttime).total_seconds())))
    print('Enjoy it')
    print('Powered by 所向披靡\n')
    key = input('按回车键退出\n')
    while key != '':
        key = input('按回车键退出\n')