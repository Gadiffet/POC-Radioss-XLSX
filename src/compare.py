import pandas as pd
import numpy as np

df1 = pd.read_excel('test/fichierCompare.xlsx')
df2 = pd.read_excel('test/fichierEntree.xlsx')
df1.equals(df2)

comparison_values = df1.values == df2.values
rows, cols = np.where(comparison_values is False)
for item in zip(cols):
    df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])

print(comparison_values)
