from bs4 import BeautifulSoup as BS
import re
from selenium import webdriver
import requests
from selenium import common
import csv
import os
import time
from multiprocessing import Process, cpu_count
from threading import Thread, Lock
import math

lock = Lock()

chrome_options = webdriver.ChromeOptions()


def split_list(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def get_info(url):
    try:
        while True:
            try:
                ip_port = 'secondtransfer.moguproxy.com:9001'
                appKey = "ZURUNGhDRE55YkVuVHMzaDpCWlFEYXdPcFJ6Z0RWZFNn"
                headers = {"Proxy-Authorization": 'Basic ' + appKey,
                           "U ser-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
                           "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"}
                #proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
                #html = requests.get(url, proxies=proxy, headers=headers, verify=False, allow_redirects=False)
                html=requests.get(url)
                soup = BS(html.text, 'lxml')
                title = soup.find(class_='context-title-text').get_text()
                domian = [i.get_text() for i in soup.find_all(class_='domainType')]
                tmp = soup.find('span', class_='').get_text().replace(' ', '').replace('\t', '').replace('\r',
                                                                                                         '').replace(
                    '\xa0', '')
                tmp = tmp.split('\n')
                username = tmp[3]
                time = tmp[5]
                content = soup.find(class_='zoom content').get_text()
                status = soup.find(class_='red').get_text()
                if status != '待回复':
                    office = status
                    status = soup.find(class_='green').get_text()
                    solution = soup.findAll(class_='zoom')[1].get_text()
                    retime = soup.find('em', class_='grey2').get_text().replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                else:
                    office = ''
                    solution = ''
                    retime = ''
                return [title, status, ' '.join(domian), username, time, content, office, solution, retime]
            except Exception:
                print('error1 finishing...')
                try:
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--disable-gpu')
                    driver = webdriver.Chrome(
                        executable_path=r"chromedriver.exe",
                        options=chrome_options)
                    driver.get(url)
                    soup = BS(driver.page_source, 'lxml')
                    title = soup.find(class_='context-title-text').get_text()
                    domian = [i.get_text() for i in soup.find_all(class_='domainType')]
                    tmp = soup.find('span', class_='').get_text().replace(' ', '').replace('\t', '').replace('\r',
                                                                                                             '').replace(
                        '\xa0', '')
                    tmp = tmp.split('\n')
                    username = tmp[3]
                    time = tmp[5]
                    content = soup.find(class_='zoom content').get_text()
                    status = soup.find(class_='red').get_text()
                    if status != '待回复':
                        office = status
                        status = soup.find(class_='green').get_text()
                        solution = soup.findAll(class_='zoom')[1].get_text()
                        retime = soup.find('em', class_='grey2').get_text().replace('\t', '').replace('\n', '').replace(
                            '\r', '')
                    else:
                        office = ''
                        solution = ''
                        retime = ''
                    return [title, status, ' '.join(domian), username, time, content, office, solution, retime]
                except Exception:
                    print('error2 finishing...')
                    pass
    except:
        pass


def main(url, filename):
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=r"F:\LZU&DC\MathModel\CUMCM\chromedriver_win32\chromedriver.exe",
                              options=chrome_options)
    driver.get(url)
    try:
        while True:
            try:
                driver.find_element_by_css_selector("[class='showMorehandle more']").click()
            except common.exceptions.ElementNotInteractableException:
                pass
    except:
        print(filename + 'start')
        pass
    soup = BS(driver.page_source, 'lxml')
    driver.quit()
    with open(filename + '.csv', 'a', newline='', encoding='utf-8') as f:
        content = csv.writer(f, dialect='excel')
        content.writerow(['标题', '状态', '领域', '用户名', '时间', '内容', '回复单位', '回复内容', '回复时间'])
    ccount = 0
    acount = 0
    for i in soup.find_all('a', href=re.compile(r'tid')):
        if i.get_text() != '[查看全文]':
            info = get_info(r'http://liuyan.people.com.cn' + i.get('href'))
            acount += 1
            if info:
                ccount += 1
                with open(filename + '2.csv', 'a', newline='', encoding='utf-8') as f:
                    content = csv.writer(f, dialect='excel')
                    content.writerow(info)
    lock.acquire()
    print(filename + ' Done!' + '---------------------------total:%s done:%s' % (acount, ccount))
    lock.release()


def run_city(citys, prov):
    for city in citys:
        print('start', city, '---')
        if os.path.exists(prov + '\\' + city + r'\url.txt'):
            if not os.path.exists(prov + '\\' + city + '\\' + city + '2.csv'):
                with open(prov + '\\' + city + r'\url.txt', 'r') as f:
                    url = f.read()
                main(url, prov + '\\' + city + '\\' + city)
        else:
            for i in os.listdir(prov + '\\' + city):
                if i != 'llurl.txt':
                    if not os.path.exists(prov + '\\' + city + '\\' + i + '\\' + i + '2.csv'):
                        with open(prov + '\\' + city + '\\' + i + r'\url.txt', 'r') as f:
                            url = f.read()
                        main(url, prov + '\\' + city + '\\' + i + '\\' + i)
        print(city, 'Done')


def run_prov(provs):
    threads = []
    for prov in provs:
        print('start', prov, '---')
        cityss = split_list(os.listdir(prov), 5)
        for citys in cityss:
            threads.append(Thread(target=run_city(citys, prov)))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        print(prov, 'Done')


if __name__ == '__main__':
    os.chdir('各省资料')
    provss = os.listdir(os.getcwd())
    provss = [provss[i:i + 5] for i in range(len(provss)) if i % 5 == 0]
    proc = []
    for provs in provss:
        proc.append(Process(target=run_prov(provs)))
    for i in proc:
        i.start()
    for i in proc:
        i.join()
    print('end---')
