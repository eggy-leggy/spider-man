# -*- coding: utf-8 -*-
import requests
import json

app_key = 'b1dc4915a336b3d8f4cb88161c5aba51'


def key_exists(d_dict, d_key):
    if d_key in d_dict.keys():
        return str(d_dict[d_key])
    return '-'


def geocode_regeo(lls):
    url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location=%s&key=' + app_key + \
          '&radius=1&extensions=base&batch=true'
    print("regeo start")
    res = requests.get(url % lls)
    res.encoding('utf-8')
    print('res', res)
    if res.status_code != 200:
        return []
    js = json.loads(res.text)
    print("start", js)
    res_list = list()
    if 'regeocodes' in js:
        for i in range(len(js['regeocodes'])):
            print(lls.split("|")[i])
            js['regeocodes'][i]['addressComponent']['coordinates'] = str(lls.split("|")[i])
            res_list.append([key_exists(js['regeocodes'][i], 'formatted_address'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'country'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'province'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'city'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'citycode'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'district'),
                             key_exists(js['regeocodes'][i]['addressComponent'], 'township'),
                             str(lls.split("|")[i])])
    print("regeo end")
    return res_list


def geocode_geo(addrs):
    url = 'https://restapi.amap.com/v3/geocode/geo?address=%s&key=' + app_key + '&batch=true'
    print("geo start")
    res = requests.get(url % addrs)
    res.encoding = 'utf-8'
    if res.status_code != 200:
        return []
    js = json.loads(res.text)
    # print('js', js)
    res_list = list()
    if 'geocodes' in js:
        for i in range(len(js['geocodes'])):
            print(addrs.split("|")[i])
            js['geocodes'][i]['address'] = str(addrs.split("|")[i])
            lat = '-'
            lon = '-'
            if ',' in key_exists(js['geocodes'][i], 'location'):
                [lat, lon] = key_exists(js['geocodes'][i], 'location').split(',')
            res_list.append([str(addrs.split("|")[i]),
                             key_exists(js['geocodes'][i], 'formatted_address'),
                             key_exists(js['geocodes'][i], 'country'),
                             key_exists(js['geocodes'][i], 'province'),
                             key_exists(js['geocodes'][i], 'city'),
                             key_exists(js['geocodes'][i], 'citycode'),
                             key_exists(js['geocodes'][i], 'district'),
                             lat, lon])
    print("geo end")
    return res_list


if __name__ == '__main__':
    # 110101005, 北新桥街道办事处北京市市辖区东城区北新桥街道办事处
    # 110101006, 东四街道办事处北京市市辖区东城区东四街道办事处
    # 110101007, 朝阳门街道办事处北京市市辖区东城区朝阳门街道办事处
    addr_list = geocode_geo('北新桥街道办事处北京市市辖区东城区北新桥街道办事处|东四街道办事处北京市市辖区东城区东四街道办事处'
                            '|朝阳门街道办事处北京市市辖区东城区朝阳门街道办事处')
    import pandas as pd

    df = pd.DataFrame(addr_list)
    print(df)
