from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ChartType, SymbolType
import webbrowser
import pandas as pd

data = pd.read_csv('total_c.csv',header=0,parse_dates=['time','date'])
areas = list(data[data['province']=='上海']['area'].unique())[2:]
values =[]
values1 =[]
index = []
index1 = []
for area in areas:
    new = data[data['area']==area]
    value = new['status'].size
    values.append((area,value))
    index.append(value)
    value1 = (new[new['status']==1]['status'].size/new['status'].size)*100
    values1.append((area,value1))
    index1.append(value1)


def geo_base() -> Map:
    c = (
        Map()
        .add("上海", values,'上海')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False,color='#99CCFF'))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(type_= "color",min_=min(index),max_=max(index),range_color=['white','#99CCFF']),
            title_opts=opts.TitleOpts(title="图1 上海市各区“地方领导留言板”留言总数分布图"),legend_opts=opts.LegendOpts(is_show=False,
                                                                                                    inactive_color='#99CCFF',legend_icon='circle')
        )
    )
    return c

geo_base().render('f1.html')
webbrowser.open('f1.html')

def geo_base1() -> Map:
    c = (
        Map()
        .add("上海", values1,'上海')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False,color='#99CCFF'))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(type_= "color",min_=min(index1),max_=max(index1),range_color=['white','#99CCFF']),
            title_opts=opts.TitleOpts(title="图1 上海市各区“地方领导留言板”留言回复比例分布图"),legend_opts=opts.LegendOpts(is_show=False,inactive_color='#99CCFF',legend_icon='circle')
        )
    )
    return c

geo_base().render('f2.html')
webbrowser.open('f2.html')