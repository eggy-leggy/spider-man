# -*- coding: utf-8 -*-
import requests
import re
from retrying import retry
import pandas as pd
import os

url_head = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

status_count = 0
# result_list = list()
#
# timeout_url_list = list()
patt = '<a href=\'([\\d/]+)\\.html\'>([^a-zA-Z0-9].*?)<'

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,fr;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36 '
}


@retry(stop_max_attempt_number=5)  # 最大重试5次，5次全部报错，才会报错
def _parse_url(url):
    response = requests.get(url, headers=headers, timeout=3)  # 超时的时候回报错并重试
    assert response.status_code == 200  # 状态码不是200，也会报错并充实
    return response


def request_url(code):
    url = url_head + code + ".html"
    print(url)
    try:
        req = _parse_url(url=url)
        req.encoding = 'gbk'
        res_sub = req.text
        return str(res_sub)
    except requests.exceptions.RequestException as e:
        print(e)
    return []


def get_city_list(code_str, this_patt=patt):
    res_str = request_url(code_str)
    citys = re.findall(this_patt, res_str)
    return pd.DataFrame(citys)


if __name__ == '__main__':
    print("start")
    file_lv1 = list()
    file_lv2 = list()
    file_lv3 = list()
    file_lv4 = list()
    file_lv5 = list()
    file_list = os.listdir('./data/')
    for file_name in file_list:
        if file_name[:6] == 'level1':
            file_lv1.append(file_name)
            continue
        if file_name[:6] == 'level2':
            file_lv2.append(file_name)
            continue
        if file_name[:6] == 'level3':
            file_lv3.append(file_name)
            continue
        if file_name[:6] == 'level4':
            file_lv4.append(file_name)
            continue
        if file_name[:6] == 'level5':
            file_lv5.append(file_name)
            continue
    if len(file_lv1) > 0:
        # print("read lv1 from ", 'level1.csv')
        df1 = pd.read_csv('./data/level1.csv')
    else:
        df1 = get_city_list("index")
        if df1.empty:
            print("未查询到省份信息")
            exit("1")
        df1.to_csv('./data/level1.csv', index=False)
        df1.columns = ['0', '1']
    for province_code in df1['0'].values.tolist():
        if ('level2_%s.csv' % province_code) in file_lv2:
            # print("read lv2 from ", ('level2_%s.csv' % province_code))
            df2 = pd.read_csv(('./data/level2_%s.csv' % province_code))
        else:
            df2 = get_city_list(province_code)
            if df2.empty:
                continue
            df2.to_csv('./data/level2_%s.csv' % province_code, index=False)
            df2.columns = ['0', '1']
        for city_code in df2['0'].values.tolist():
            if ('level3_%s.csv' % city_code.split('/')[1]) in file_lv3:
                # print("read lv3 from ", ('level3_%s.csv' % city_code.split('/')[1]))
                df3 = pd.read_csv(('./data/level3_%s.csv' % city_code.split('/')[1]))
            else:
                df3 = get_city_list(city_code)
                if df3.empty:
                    continue
                df3.to_csv('./data/level3_%s.csv' % city_code.split('/')[1], index=False)
                df3.columns = ['0', '1']
            for district_code in df3['0'].values.tolist():
                p_code = district_code.split('/')[1][:2]
                this_code = district_code.split('/')[1]
                df4 = pd.DataFrame()
                if len(this_code) == 6:
                    if ('level4_%s.csv' % this_code) in file_lv4:
                        # print("read lv4 from ", ('level4_%s.csv' % this_code))
                        df4 = pd.read_csv(('./data/level4_%s.csv' % this_code))
                    else:
                        df4 = get_city_list(p_code + '/' + district_code)
                        if df4.empty:
                            continue
                        df4.to_csv('./data/level4_%s.csv' % this_code, index=False)
                        df4.columns = ['0', '1']
                else:
                    # print('处理县级市 镇信息','level5_%s.csv' % this_code)
                    if ('level5_%s.csv' % this_code) in file_lv5:
                        # print("read lv5 from ", ('level4_%s.csv' % this_code))
                        df5 = pd.read_csv(('./data/level5_%s.csv' % this_code))
                    else:
                        df5 = get_city_list(p_code + '/' + district_code,
                                            r'<td>(\d+)</td><td>(\d+)</td><td>([^a-zA-Z0-9].*?)</td></tr>')
                        if df5.empty:
                            continue
                        df5.to_csv('./data/level5_%s.csv' % this_code, index=False)
                if df4.empty:
                    continue
                for street_code in df4['0'].values.tolist():
                    c_code = street_code.split('/')[1][2:4]
                    if ('level5_%s.csv' % street_code.split('/')[1]) not in file_lv5:
                        df5 = get_city_list(p_code + '/' + c_code + '/' + street_code,
                                            r'<td>(\d+)</td><td>(\d+)</td><td>([^a-zA-Z0-9].*?)</td></tr>')
                        if df5.empty:
                            if status_count > 10:
                                exit(1)
                            print("there is no data for level5")
                            status_count = status_count + 1
                            continue
                        df5.to_csv('./data/level5_%s.csv' % street_code.split('/')[1], index=False)
    print("end")
