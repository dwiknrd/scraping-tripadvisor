import pandas as pd

df = pd.read_csv('universal_studio_branches.csv')

print(df.info())
print(df.isnull().sum())