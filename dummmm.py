
import pandas_pgm as pd
df = pd.read_csv('/home/ee212821/Documents/power_bi_dataset.csv')
# df = df[df['Time_orderd'] == "NaN"]
df = df.drop(df['Time_orderd'] == "NaN")
print(df)