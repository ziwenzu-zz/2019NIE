import pandas as pd
import os
import re
import collections
import numpy as np
import jieba
from PIL import Image
import  matplotlib.pyplot as plt
from snownlp import SnowNLP,classification
import chinese_classification as c

'''
def process():
    datas = []
    for root, dirs, files in os.walk(r'各省资料'):
        for file in files:
            if re.search(r'2.csv', file):
                path = os.path.join(root, file)
                data = pd.read_csv(path, header=0, names=['标题', '状态', '领域', '用户名', '时间', '内容', '回复单位', '回复内容', '回复时间'],
                                   parse_dates=['回复时间'])
                d1 = root.split('\\')[1]
                d2 = root.split('\\')[2]
                d3 = file[:-5]
                data.insert(0, '省份', d1)
                data.insert(1, '地区', d2)
                data.insert(2, '负责人', d3)
                datas.append(data)
    dataframe = pd.concat(datas, ignore_index=True)
    return dataframe


def count():
    all = []
    for test_txt in status_true['内容']:
        words = []
        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        test_txt = re.sub(pattern, '', test_txt)  # 将符合模式的字符去除
        seg_list_exact = jieba.cut(test_txt, cut_all=False)  # 精确模式分词
        object_list = []
        with open('hlt_stop_words.txt', 'r', encoding='utf-8') as f:
            remove_words = f.read().split('\n') + ['\xa0']
        for word in seg_list_exact:  # 循环读出每个分词
            if word not in remove_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表

        # 词频统计
        word_counts = collections.Counter(object_list)  # 对分词做词频统计
        word_counts_top3 = word_counts.most_common(3)  # 获取前10最高频的词
        for word in word_counts_top3:
            words.append(word[0])
        all.append(words)
    return all
    # 输出检查


def write():
    domain1 = []
    domain2 = []
    for i in status_true['领域']:
        x = i.split(' ')
        if x[0] == '其他':
            x[0] = None
        if x[1] == '其他':
            x[1] = None
        domain1.append(x[0])
        domain2.append(x[1])
    del status_true['领域']
    status_true['domain1'] = domain1
    status_true['domain2'] = domain2
    all = count()
    status_true['top1'] = [i[0] for i in all]
    status_true['top2'] = [i[1] for i in all]
    status_true['top3'] = [i[2] for i in all]
    status_true.to_csv('status_true.csv', index=False)
'''


# time = []
# date = []
# for i in total['时间']:
#     date.append(i[:len('2019-07-07')])
#     time.append(i[len('2019-07-07'):])
# total['time'] = time
# total['date'] = date
# del total['时间']
#
# total.to_csv('total.csv',index=False)
# total['province'] = total['省份']
# total['area'] = total['地区']
# total['to_leader'] = total['负责人']
#
# total['title'] = total['标题']
# username = []
# for i in total['用户名']:
#     if i[0] == '匿':
#         username.append(1)
#     else:
#         username.append(0)
# total['username'] = username
#
# status =[]
# for i in total['状态']:
#     if i != '已办理':
#         status.append(1)
#     else:
#         status.append(0)
# print(status)
# total['status'] = status
#
# domain = []
# type = []
# for i in total['领域']:
#     data = i.split(' ')
#     domain.append(data[0])
#     type.append(data[1])
# total['domain'] = domain
# total['type'] = type
#
# total['content'] = total['内容']
# total['re_office'] = total['回复单位']
# total['re_content'] = total['回复内容']
# total['re_time'] = total['回复时间']
#
# total['domain'] = total.date.dt.domain
# total['month'] = total.date.dt.month
# total['day'] = total.date.dt.day
#
# delete = ['回复时间','回复内容','回复单位','内容','领域','状态','用户名','负责人','标题','地区','省份']
# for d in delete:
#     del total[d]
# print(total.head())
# print(total.info())
# total.to_csv('total_c.csv',index=False)

# total = pd.read_csv('total_c.csv',header=0,parse_dates=['time','date'])
# years = list(total['domain'].unique())
# sums = []
# re_sums = []
# re_per = []
# no_re_sums = []
# no_re_per = []
# for year in years:
#     data = total[total['domain']==domain]
#     sums.append(data['status'].size)
#     re_sums.append(data[data['status']==1]['status'].size)
#     no_re_sums.append(data[data['status'] == 0]['status'].size)
#     re_per.append("%.2f%%" % ((data[data['status']==1]['status'].size/data['status'].size) * 100))
#     no_re_per.append("%.2f%%" % ((data[data['status']==0]['status'].size/data['status'].size) * 100))
#
# tongji = {'years':years,'no_re_sums':no_re_sums,'no_re_per':no_re_per,'re_sums':re_sums,'re_per':re_per,'sum':sums}
# data = pd.DataFrame(data=tongji)
# data.to_csv('tongji_v1_shanghai.csv',index=False)


total = pd.read_csv('total_c.csv',header=0,parse_dates=['time','date'])
domains = list(total['domain'].unique())
# sums = []
# # re_sums = []
# # re_per = []
# # no_re_sums = []
# # no_re_per = []
# # for domain in domains:
# #     data = total[total['domain'] == domain]
# #     sums.append(data['status'].size)
# #     re_sums.append(data[data['status']==1]['status'].size)
# #     no_re_sums.append(data[data['status'] == 0]['status'].size)
# #     re_per.append("%.2f%%" % ((data[data['status']==1]['status'].size/data['status'].size) * 100))
# #     no_re_per.append("%.2f%%" % ((data[data['status']==0]['status'].size/data['status'].size) * 100))
# #
# # tongji = {'domain':domains,'no_re_sums':no_re_sums,'no_re_per':no_re_per,'re_sums':re_sums,'re_per':re_per,'sum':sums}
# # data = pd.DataFrame(data=tongji)
# # data.to_csv('tongji_v1_shanghai_domain.csv',encoding='utf-8',index=False)
for domain in domains:
    print(domain)