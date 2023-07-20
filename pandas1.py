import numpy as np
import pandas as pd
# creating the series
z=pd.Series([1,2,np.NaN,4,5])
print(z)
dates = pd.date_range('20230211',periods=11)
print(dates)
# Creating the dataframe
df = pd.DataFrame(np.random.randn(11, 4), index=dates, columns=list('ABCD'))
print(df)
l = [1,2,3,4]
m = [11,12,13,14]
zz = pd.Series(index=l,data=m)
print(zz)
print("Alternative option")
print(pd.Series(l,m))
np.random.seed(1) # the random values will not change during next execution.
q = pd.DataFrame(np.random.randn(11,2),index='A B C D E F G H I J K'.split(),columns='X Y'.split())
print(q)
#adding another column
q['Z'] = q['X']+q['Y']
print(q)
qq = q.drop('Z',axis=1)
print(qq)
#to get the values of rows and columns
print("Getting the column values")
print(q.X)
print("Getting the row values")
print(q.loc['A'])
print("Getting the values based on index")
print(q.iloc[10])
print("Slicing the rows")
print(q.loc['E':])
print("-------------------------------------")
print("Condition Selection")
print(q[q>0.5])
print(q[q['X']>0.5])   #condition for particular col
print(q[q['X']>0.5]['X'])     #Getting particular col

#using CSV files
df1 = pd.read_csv('/home/ee212821/Downloads/trail1.csv')
# print(df1.count())
df1.dropna(axis=0)
# print(df1.count())
print(q.groupby('X'))
print(q.groupby('X').mean())

