# -*- coding: utf-8 -*-
import requests
import json

key = 'b1dc4915a336b3d8f4cb88161c5aba51'


def geocode_regeo(lls):
    url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location=%s&key=' + key + \
          '&radius=1&extensions=base&batch=true'
    print("regeo start")
    res = requests.get(url % lls)
    res.encoding('utf-8')
    if res.status_code != 200:
        return []
    js = json.loads(res.text)
    res_list = list()
    if 'regeocodes' in js:
        for i in range(len(js['regeocodes'])):
            print(lls.split("|")[i])
            js['regeocodes'][i]['addressComponent']['coordinates'] = str(lls.split("|")[i])
            res_list.append([js['regeocodes'][i]['formatted_address'],
                             js['regeocodes'][i]['addressComponent']['country'],
                             js['regeocodes'][i]['addressComponent']['province'],
                             js['regeocodes'][i]['addressComponent']['city'],
                             js['regeocodes'][i]['addressComponent']['citycode'],
                             js['regeocodes'][i]['addressComponent']['district'],
                             js['regeocodes'][i]['addressComponent']['township'],
                             str(lls.split("|")[i])])
    print("regeo end")
    return res_list


def geocode_geo(addrs):
    url = 'https://restapi.amap.com/v3/geocode/geo?address=%s&key=' + key + '=1&extensions=base&batch=true'
    print("geo start")
    res = requests.get(url % addrs)
    res.encoding('utf-8')
    if res.status_code != 200:
        return []
    js = json.loads(res.text)
    res_list = list()
    if 'geocodes' in js:
        for i in range(len(js['geocodes'])):
            print(addrs.split("|")[i])
            js['geocodes'][i]['address'] = str(addrs.split("|")[i])
            res_list.append([str(addrs.split("|")[i]),
                             js['geocodes'][i]['formatted_address'],
                             js['geocodes'][i]['country'],
                             js['geocodes'][i]['province'],
                             js['geocodes'][i]['city'],
                             js['geocodes'][i]['citycode'],
                             js['geocodes'][i]['district'],
                             js['geocodes'][i]['location']])
    print("geo end")
    return res_list


if __name__ == '__main__':
    addr_list = geocode_geo()
