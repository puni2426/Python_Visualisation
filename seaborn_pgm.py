import pandas_pgm as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data into DataFrame
df = pd.read_csv('/home/ee212821/Documents/power_bi_dataset.csv')

# Create regression plot
sns.regplot(x='Delivery_person_Age', y='Delivery_person_Ratings', data=df)

# Display plot
plt.show()



# import folium
# w = folium.Map(location=[22.77710235, 75.8961588], zoom_start=4)
# w.show_in_browser()
#
def hello():
    """this is the docstring of the program
    to print """
    return None
print(hello.__doc__)
help(hello)