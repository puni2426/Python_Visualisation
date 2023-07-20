import pandas as pd
#Reading data from CSV
df = pd.read_csv('/home/ee212821/Documents/power_bi_dataset.csv')
# Printing First five rows `
print(df.head())
print(df.info())
df_cln = df.dropna()
df_flt = df[df['Type_of_order'] == 'Snacks']
mean_v = df['Time_taken'].mean()
print("Describe the Table")
df1 = df.describe()
print(df1['Vehicle_condition'])
print(df[[]])