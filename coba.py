import pandas as pd

df = pd.read_csv('universal_studios.csv')

df['written_date'] = df['written_date'].str.lstrip()
df.to_csv('universal_studios_clean.csv', index=False)