# -*- coding: utf-8 -*-
import pandas as pd
from map.util.gaode import geocode_geo

csv_file = r'/Users/chqiang_f/workspace/github/eggyleggy/spider-man/township/result.csv'

if __name__ == '__main__':
    df_r = pd.read_csv('./result_local.csv', header=None)
    df = pd.read_csv(csv_file)
    df_col = df['p_name'] + df['c_name'] + df['d_name'] + df['s_name']
    count = 0
    address = ''
    for col in df_col.values.tolist():
        if col in df_r[0].values:
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