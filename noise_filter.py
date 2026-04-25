import numpy as np
import pandas as pd
from pathlib import Path
from scipy.signal import medfilt
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

BASE_DIR = Path(__file__).parent
FILE_DIR = BASE_DIR/'data'/'case1'/'output'

# 尝试用hampel filter来过滤开头的noise
def hampel_filter(s, window_size=31, n_sigmas=3):
    s = s.copy()
    rolling_median = s.rolling(
        window = window_size,
        center = True
    ).median()

    diff = np.abs(s - rolling_median)
    # MAD可以理解为局部串口里的典型偏差，算中位数可以知道这个窗口正常波动大概是1
    mad = diff.rolling(
        window = window_size,
        center = True
    ).median() 

    threshold = n_sigmas * 1.4826 * mad

    outliers = diff > threshold

    s[outliers] = rolling_median[outliers]

    return s

fig = plt.figure(figsize=(20,10))

for i in range(1,13):
    df = pd.read_csv(FILE_DIR/f'output{2.5*i}-{2.5*i}.csv', index_col=0)
    signal = df.copy()
    # mask1 = signal.index < 0.07
    # mask2 = signal.index < 0.07
    mask

    # 这个会改变mask范围内的所有点，但我们其实只需要处理异常点
    # signal.loc[mask, 'ch1'] = medfilt(signal.loc[mask, 'ch1'], kernel_size=7)
    # signal.loc[mask, 'ch2'] = medfilt(signal.loc[mask, 'ch2'], kernel_size=7)
    # signal.loc[mask, 'ch3'] = medfilt(signal.loc[mask, 'ch3'], kernel_size=7)
    # signal.loc[mask, 'ch4'] = medfilt(signal.loc[mask, 'ch4'], kernel_size=7)

    # 用完之后发现一些detail没有了
    # smoothed = savgol_filter(signal, window_length=21, polyorder=3, axis=0)
    
    # use hampel_filter
    # 用完这个发现还是不管用，
    # signal.loc[mask, 'ch1'] = hampel_filter(signal.loc[mask, 'ch1'])
    # signal.loc[mask, 'ch2'] = hampel_filter(signal.loc[mask, 'ch2'])
    # signal.loc[mask, 'ch3'] = hampel_filter(signal.loc[mask, 'ch3'])
    # signal.loc[mask, 'ch4'] = hampel_filter(signal.loc[mask, 'ch4'])

    # 直接设置为0
    signal.loc[mask, 'ch1'] = 0
    signal.loc[mask, 'ch2'] = 0
    signal.loc[mask, 'ch3'] = 0
    signal.loc[mask, 'ch4'] = 0

    # signal = pd.DataFrame(signal, index = signal.index, columns= signal.columns)
    signal.to_csv(FILE_DIR/f'processed{2.5*i}-{2.5*i}.csv')

    ax = fig.add_subplot(3,4,i)
    ax.set_title(f"{2.5*i}-{2.5*i}")
    ax.plot(signal)

plt.show()
