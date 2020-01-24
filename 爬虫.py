import requests
from bs4 import BeautifulSoup as BS
import os
import re

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'aliyungf_tc=AQAAAK3K+CE/zgAAFF+bc64asauqvW1I; wdcid=77772f17911cb769; sfr=1; sso_c=0; _people_ip_new_code=730000; wdses=5896a4b46142a29d; 4de1d0bdb25d4625be2481a1b9e1350f=WyIyNzA4MzA1Mzg2Il0; wdlast=1574955294; JSESSIONID=BE3856E4E40D41620EDA4DAA5F9F3CE7',
'Host': 'liuyan.people.com.cn',
'Referer': 'http://liuyan.people.com.cn/forum/list?fid=539',
'Upgrade-Insecure-Requests': '1',
'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

memory =[]

def geturl(url,prov):
    try:
        html = requests.get(url, headers=headers).text
        soup = BS(html, 'lxml')
        os.chdir(prov)
        locations=[]
        leadernames = soup.find_all("a",class_="forumName")
        leadermessages = soup.find_all("a",class_="message_index")
        for i in range(len(leadernames)):
            if leadernames[i].get_text().replace(' ','') not in memory:
                memory.append(leadernames[i].get_text().replace(' ',''))
                os.mkdir(leadernames[i].get_text().replace(' ',''))
                with open(leadernames[i].get_text().replace(' ','')+r'\url.txt','a+') as fh:
                    fh.write('http://liuyan.people.com.cn' + leadermessages[i].get('href'))
        for i in soup.find_all(class_='count-limit'):
            if i.get_text() not in memory:
                memory.append(i.get_text())
                os.mkdir(i.get_text().replace(' ',''))
                with open(i.get_text().replace(' ','')+r'\llurl.txt','a+') as fh:
                    fh.write('http://liuyan.people.com.cn' + i.get('href'))
            locations.append(i.get_text())
        for i in locations:
            os.chdir(i)
            with open(r'llurl.txt','r') as fr:
                url = fr.read()
            html1 = requests.get(url,headers=headers).text
            soup1 = BS(html1,'lxml')
            leadernames = soup1.find_all("a", class_="forumName")
            leadermessages = soup1.find_all("a", class_="message_index")
            for j in range(len(leadernames)):
                if leadernames[j].get_text() not in memory:
                    memory.append(leadernames[j].get_text().replace(' ',''))
                    os.mkdir(leadernames[j].get_text().replace(' ',''))
                    with open(leadernames[j].get_text().replace(' ','') + r'\url.txt', 'a+') as fh:
                        fh.write('http://liuyan.people.com.cn' + leadermessages[j].get('href'))
            for j in soup1.find_all(class_='count-limit'):
                if j.get_text() not in memory:
                    memory.append(j.get_text())
                    os.mkdir(j.get_text().replace(' ',''))
                    with open(j.get_text().replace(' ','') + r'\url.txt', 'a+') as fh:
                        fh.write('http://liuyan.people.com.cn' + j.get('href'))
            os.chdir('..')
        os.chdir('..')
        print('prov'+'done')
    except Exception as err:
        print(str(err))
def main():
    with open('省份网址','r') as fh:
        for line in fh.read().split('\n'):
            line = line.split(',')
            try:
                if line[0] not in memory:
                    memory.append(line[0])
                    os.mkdir(line[0])
                    geturl(line[1],line[0])
            except Exception:
                pass
    with open('memory.txt','a+') as fh:
        fh.writelines(memory)
main()