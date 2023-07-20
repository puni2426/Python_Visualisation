import pandas_pgm as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle

# Load data into dataframe
df = pd.read_csv('/home/ee212821/Documents/power_bi_dataset.csv')

# Group data by category and count the number of occurrences
counts = df['Type_of_vehicle'].value_counts()

# Create waffle chart
fig = plt.figure(
    FigureClass=Waffle,
    rows=10,
    values=counts,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)},
    colors=['#008080', '#FFA500', '#00BFFF'] # set custom colors for each category  FFC0CB
)
plt.title('Waffle Chart')
plt.show()
