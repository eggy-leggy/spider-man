# -*- coding: utf-8 -*-
import pandas as pd

# 逆地理编码后文件， 取出无用列

file_path = r'C:\Users\chunqiangfan\work\github\spider-man\township\result_local.csv'

if __name__ == '__main__':
    print('start')
    df = pd.read_csv(file_path, header=None)
    df = df[~df[7].str.contains(r'\[\]')]
    df = df[~df[7].str.contains(r',]')]
    df = df[[1, 2, 3, 4, 5, 6, 7]].drop_duplicates()
    df['latitude'] = df[7].map(lambda x: str(x).split(',')[0])
    df['longitude'] = df[7].map(lambda x: str(x).split(',')[1])
    del df[7]
    df.to_csv("./result_format.csv", index=None, header=None)
    print('end')
