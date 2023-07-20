import matplotlib.pyplot as plt
import pandas_pgm as pd
df=pd.read_csv("/home/ee212821/Documents/power_bi_dataset.csv")
# print(df.head())
# df_head = df.head()
# df_loc = df.iloc[:,[1]]
# df_grp = df.groupby('City',axis=0   ).sum()
# df_head['Time_taken'].plot(kind='bar')
df_values = df['Type_of_vehicle'].value_counts()
df_values.plot(kind='pie')
plt.title("Graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()
