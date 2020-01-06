# -*- coding: utf-8 -*-
import pandas as pd
import os
import zipfile

data_path = r'C:\Users\chunqiangfan\work\github\OfflineReverseGeocode\data\data.zip'


######
# 将分散的文件合并为一个文件 (读取zip文件)
# p：省
# c：市
# d：区
# s：街道
# t：城镇（太多暂不处理）
######

def get_df(zf, f_list):
    df = pd.DataFrame()
    for f_path in f_list:
        f = zf.open(f_path)
        df = df.append(pd.read_csv(f))
        f.close()
    return df


if __name__ == '__main__':
    print('start')
    zf_list = zipfile.ZipFile(data_path, 'r')
    file_lv1 = list()
    file_lv2 = list()
    file_lv3 = list()
    file_lv4 = list()
    file_lv5 = list()
    for file_name in zf_list.namelist():
        if file_name[5:11] == 'level1':
            file_lv1.append(file_name)
            continue
        if file_name[5:11] == 'level2':
            file_lv2.append(file_name)
            continue
        if file_name[5:11] == 'level3':
            file_lv3.append(file_name)
            continue
        if file_name[5:11] == 'level4':
            file_lv4.append(file_name)
            continue
        if file_name[5:11] == 'level5':
            file_lv5.append(file_name)
            continue
    df1 = get_df(zf_list, file_lv1)
    df2 = get_df(zf_list, file_lv2)
    df3 = get_df(zf_list, file_lv3)
    df4 = get_df(zf_list, file_lv4)
    # df5 = get_df(zf_list, file_lv5)   文件太多，一次加载时间过长，后期优化
    zf_list.close()
    df1.columns = ['p', 'p_name']
    df2.columns = ['0', 'c_name']
    df3.columns = ['0', 'd_name']
    df4.columns = ['0', 's_name']
    # df5.columns = ['0', 't_type', 't_name']   文件太多，一次加载时间过长，后期优化
    df2['p'] = df2['0'].map(lambda x: int(x[3:5]))
    df2['c'] = df2['0'].map(lambda x: int(x[5:]))
    df3['p'] = df3['0'].map(lambda x: int(x[3:5]))
    df3['c'] = df3['0'].map(lambda x: int(x[5:7]))
    df3['d'] = df3['0'].map(lambda x: int(x[7:]))
    df4['p'] = df4['0'].map(lambda x: int(x[3:5]))
    df4['c'] = df4['0'].map(lambda x: int(x[5:7]))
    df4['d'] = df4['0'].map(lambda x: int(x[7:9]))
    df4['s'] = df4['0'].map(lambda x: int(x[9:]))
    del df2['0']
    del df3['0']
    df4['0'] = df4['0'].map(lambda x: str(x)[3:])
    dff = df4.merge(df1, how='left', on=['p']).merge(df2, how='left', on=['p', 'c']).merge(df3, how='left',
                                                                                           on=['p', 'c', 'd'])
    del dff['p']
    del dff['c']
    del dff['d']
    del dff['s']
    dff.to_csv('./result.csv', index=False)
    print('end')
