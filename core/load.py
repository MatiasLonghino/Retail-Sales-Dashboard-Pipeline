import pandas as pd
import numpy as np

#LOAD
def save_csv(df, path):

    df.to_csv(path, index=False, sep=';', encoding='utf-8-sig')