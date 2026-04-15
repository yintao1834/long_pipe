import pandas as pd
import numpy as np
from pathlib import Path
import charset_normalizer

# 
BASE_DIR = Path(__file__).parent
data_path = BASE_DIR/"data"/"case1"/"2(5.0-5.0)_strain.csv"
with open(data_path,'rb') as f:
    rawdata = f.read()
result = charset_normalizer.detect(rawdata)
df = pd.read_csv(data_path, encoding = result['encoding'], usecols=['Distance (m)','Time 1'], 
                 index_col=['Distance (m)'])
df.columns = ['strain']
print(df)
print('vodatre')