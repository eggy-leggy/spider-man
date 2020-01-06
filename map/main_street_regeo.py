# -*- coding: utf-8 -*-
import pandas as pd
from map.util.gaode import geocode_geo
import os

# 通过gaode API实现逆地理编码，并导出文件

csv_file = r'C:\Users\chunqiangfan\work\github\spider-man\township\result.csv'

if __name__ == '__main__':
    df_r = pd.DataFrame()
    if os.path.isdir('./result_local.csv'):
        df_r = pd.read_csv('./result_local.csv', header=None)
    df = pd.read_csv(csv_file)
    df_col = df['p_name'] + df['c_name'] + df['d_name'] + df['s_name']
    count = 0
    address = ''
    for col in df_col.values.tolist():
        if not df_r.empty and col in df_r[0].values:
            continue
        address = address + '|' + col
        count = count + 1
        if count == 9:
            result = pd.DataFrame(geocode_geo(address[1:]))
            if not result.empty:
                result.to_csv('./result_local.csv', mode='a', header=False, index=False)
            count = 0
            address = ''
    result = pd.DataFrame(geocode_geo(address[1:]))
    if not result.empty:
        result.to_csv('./result_local.csv', mode='a', header=False, index=False)
