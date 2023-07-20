import pandas_pgm as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load data into dataframe
df = pd.read_csv('/home/ee212821/Documents/power_bi_dataset.csv')

# Concatenate all text into a single string
text = ' '.join(df['Delivery_person_ID'].astype(str))

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud
plt.figure(figsize=(12, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
