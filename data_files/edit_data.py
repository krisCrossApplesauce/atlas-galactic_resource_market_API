import pandas as pd

df = pd.read_csv('planet_data.csv')

df.sort_values(by=['name'])

# df.insert(0, 'id', range(1, len(df) + 1))

df.to_csv('planet_data.csv', index=False)
