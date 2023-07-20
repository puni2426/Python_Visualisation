import pandas as pd
df = pd.read_csv('/home/ee212821/Downloads/Dataset1.csv')
# Now, you can perform different pandas operations:
print(df.info())

# 1. Display the DataFrame
print(df)

# 2. Filter rows based on a condition
filtered_df = df[df["Delivery_person_Age"] > 20]
print(filtered_df)

# 3. Calculate the mean of Delivery_person_Ratings
mean_ratings = df["Delivery_person_Ratings"].mean()
print(mean_ratings)

# 4. Group data by City and calculate the average Time_taken
grouped_by_city = df.groupby("City")["Time_taken"].mean()
print(grouped_by_city)

# 5. Sort the DataFrame based on Time_taken in ascending order
sorted_df = df.sort_values(by="Time_taken", ascending=True)
print(sorted_df)

# 6. Count the occurrences of each value in Festival column
festival_counts = df["Festival"].value_counts()
print(festival_counts)

# Assuming you already have the DataFrame 'df' from the previous code


# 1. Access specific columns

print(df["Delivery_person_ID"])  # Access the 'Delivery_person_ID' column


# 2. Filtering with multiple conditions

filtered_df = df[(df["Time_taken"] > 20) & (df["Weatherconditions"] == "Sandstorms")]

print(filtered_df)


# 3. Selecting rows and columns with loc and iloc

selected_rows = df.loc[[0, 2, 4]]  # Select specific rows

selected_columns = df.loc[:, ["Delivery_person_Age", "Type_of_order"]]  # Select specific columns


# 4. Aggregation functions

max_time_taken = df["Time_taken"].max()  # Maximum value in the 'Time_taken' column

min_time_taken = df["Time_taken"].min()  # Minimum value in the 'Time_taken' column


# 5. Updating values in the DataFrame

df.loc[df["Time_taken"] > 30, "Type_of_order"] = "Special Drinks"  # Updating 'Type_of_order' for rows where 'Time_taken' > 30


# 6. Adding a new calculated column

df["Delivery_distance"] = ((df["Delivery_location_latitude"] - df["Restaurant_latitude"]) ** 2 +

                           (df["Delivery_location_longitude"] - df["Restaurant_longitude"]) ** 2) ** 0.5


# 7. Dropping unnecessary columns

df.drop(columns=["ID"], inplace=True)


# 8. Renaming columns

df.rename(columns={"Type_of_vehicle": "Vehicle_Type"}, inplace=True)


# 9. Handling missing values (if any)

# For example, fill missing 'Time_taken' values with the mean value

mean_time_taken = df["Time_taken"].mean()

df["Time_taken"].fillna(mean_time_taken, inplace=True)


# 10. Value counts and unique values

print(df["Road_traffic_density"].value_counts())  # Count occurrences of each value

unique_festivals = df["Festival"].unique()  # Get unique values


# 11. Saving the DataFrame to a CSV file

df.to_csv("delivery_data.csv", index=False)


# 12. Filtering with the 'query()' method

filtered_df = df.query("Delivery_person_Ratings > 4.0 and Time_taken < 30")


# 13. Pivot table

pivot_table = df.pivot_table(index="Type_of_order", columns="Weatherconditions", values="Time_taken", aggfunc="mean")


# 14. Apply a function to a column

df["Order_Date"] = pd.to_datetime(df["Order_Date"])  # Convert 'Time_Orderd' to datetime type


# 15. Handling datetime columns

df["Order_Date"] = pd.to_datetime(df["Order_Date"])  # Convert 'Order_Date' to datetime type

df["Order_month"] = df["Order_Date"].dt.month  # Extract month from 'Order_Date'


# 16. Grouping and aggregating based on multiple columns

grouped_df = df.groupby(["City", "Festival"]).agg({"Time_taken": "mean", "Delivery_person_Age": "median"})


# 17. Plotting data with pandas

import matplotlib.pyplot as plt

df["Delivery_person_Age"].plot(kind="hist", bins=10)
plt.show()


# 18. Merging DataFrames (if you have more data to merge)

# Example: Create a new DataFrame with delivery ratings

ratings_data = {

    "Delivery_person_ID": ["BANGRES19DEL01", "DEL2023RATINGS"],

    "Delivery_person_Ratings": [4.4, 4.8]

}

ratings_df = pd.DataFrame(ratings_data)


# Merge the ratings DataFrame with the original DataFrame

merged_df = pd.merge(df, ratings_df, on="Delivery_person_ID", how="left")


# 19. Handling duplicates

df.drop_duplicates(subset=["Delivery_person_ID", "Order_Date"], keep="first", inplace=True)


# 20. String operations

df["Delivery_person_ID_upper"] = df["Delivery_person_ID"].str.upper()


# 21. Resetting the index

df.reset_index(drop=True, inplace=True)

# ... and many more!

# Assuming you already have the DataFrame 'df' from the previous code


# 1. Handling Categorical Data

# Convert categorical columns to categorical data type

df["City"] = df["City"].astype("category")

df["Weatherconditions"] = df["Weatherconditions"].astype("category")


# 2. Grouping and calculating multiple statistics

grouped_stats = df.groupby("Type_of_order").agg({

    "Time_taken": ["mean", "median", "min", "max"],

    "Delivery_person_Ratings": "mean",

})


# 3. Reshaping the DataFrame using pivot_table or melt

pivot_table = df.pivot_table(index="Type_of_order", columns="Festival", values="Time_taken", aggfunc="mean")

melted_df = pd.melt(df, id_vars=["Type_of_order"], value_vars=["Time_Orderd", "Time_Order_picked"], var_name="Time_Event")


# 4. String methods for text data

df["Restaurant_latitude_str"] = df["Restaurant_latitude"].astype(str)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

df["Day_of_week"] = df["Order_Date"].dt.day_name()


# 5. Handling outliers and filtering

q1 = df["Time_taken"].quantile(0.25)

q3 = df["Time_taken"].quantile(0.75)

iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr

upper_bound = q3 + 1.5 * iqr

filtered_outliers_df = df[(df["Time_taken"] >= lower_bound) & (df["Time_taken"] <= upper_bound)]


# 6. Applying a function to a DataFrame

def calculate_speed(row):

    distance = ((row["Delivery_location_latitude"] - row["Restaurant_latitude"]) ** 2 +

                (row["Delivery_location_longitude"] - row["Restaurant_longitude"]) ** 2) ** 0.5

    return distance / row["Time_taken"]


df["Delivery_speed"] = df.apply(calculate_speed, axis=1)


# 7. Handling datetime intervals

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

df["Next_order_date"] = df.groupby("Delivery_person_ID")["Order_Date"].shift(-1)


# 8. Joining DataFrames

ratings_data = {

    "Delivery_person_ID": ["BANGRES19DEL01", "DEL2023RATINGS"],

    "Delivery_person_Ratings": [4.4, 4.8]

}

ratings_df = pd.DataFrame(ratings_data)


merged_df = df.merge(ratings_df, on="Delivery_person_ID", how="left")


# 9. Time Series operations

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

df.set_index("Order_Date", inplace=True)

weekly_orders = df.resample("W").count()


# 10. Applying a function element-wise

df["Delivery_person_Age_category"] = df["Delivery_person_Age"].apply(lambda age: "Young" if age <= 25 else "Senior")


# 11. Handling NULL/NaN values

df.fillna(0, inplace=True)  # Fill all NaN values with 0


# 12. Checking for duplicate rows

duplicates_exist = df.duplicated().any()


# 13. Creating dummy variables for categorical columns

df = pd.get_dummies(df, columns=["City", "Type_of_order"])


# 14. Using the 'cut' function to create bins for continuous variables

df["Delivery_time_category"] = pd.cut(df["Time_taken"], bins=[0, 20, 40, 60], labels=["Fast", "Moderate", "Slow"])


# 15. Time-based rolling calculations

df["Time_taken_rolling_mean"] = df["Time_taken"].rolling(window=3).mean()


# ... and many more!