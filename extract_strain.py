import pandas as pd
import numpy as np
from pathlib import Path

Bace_Dir = Path(__file__).parent
Process_Dir = Bace_Dir/'data'/'case1'
data_path = Process_Dir/'accumulate_result.csv'
out_Dir = Process_Dir/'output'
out_Dir.mkdir(exist_ok=True)

result_test = pd.read_csv(data_path, index_col='Distance (m)')
result_df = result_test.copy()
# set the range of strain data
index_ch1 = (result_df.index > 13.961) & (result_df.index < 26.125)
index_ch2 = (result_df.index > 28.555) & (result_df.index < 40.752)
index_ch3 = (result_df.index > 43.020) & (result_df.index < 55.180)
index_ch4 = (result_df.index > 57.599) & (result_df.index < 69.800)

# check the length of range
index_chn = [index_ch1, index_ch2, index_ch3, index_ch4]
range_ch = [index_ch.sum() for index_ch in index_chn]
# print(range_ch) 

diff = max(range_ch) - range_ch
for i, ch in enumerate(range_ch):
    start = np.where(index_chn[i])[0][0]
    end = np.where(index_chn[i])[0][-1]
    if diff[i] == 0:
        pass
    else:
        right = diff[i] // 2
        left = diff[i] - right
        start = start -left
        end = end + right
    index_chn[i][start : end + 1] = True
range_ch_new = [index_ch.sum() for index_ch in index_chn]
# print(range_ch_new)
# print(result_df[index_ch1]["2.5-2.5"].head())
# print(result_df[index_ch1]["2.5-2.5"][::-1].tail())

L = 10
column_list = np.linspace(0., L, max(range_ch))
for i in range(1, 13):
    ch1 = result_df.loc[index_ch1, f"{2.5*i}-{2.5*i}"]
    ch2 = result_df.loc[index_ch2, f"{2.5*i}-{2.5*i}"][::-1]
    ch3 = result_df.loc[index_ch3, f"{2.5*i}-{2.5*i}"]
    ch4 = result_df.loc[index_ch4, f"{2.5*i}-{2.5*i}"][::-1]
    df = pd.DataFrame({
        'ch1': ch1.values,
        'ch2': ch2.values,
        'ch3': ch3.values,
        'ch4': ch4.values
    }, index = column_list)
    out_path = Process_Dir/'output'/f'output{2.5*i}-{2.5*i}.csv'
    df.to_csv(out_path)





# def reverse_strain()
