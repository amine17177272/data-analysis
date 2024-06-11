import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

# # List of file paths for each month from January to December
# input_files = [
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_January_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_February_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_March_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_May_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_June_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_July_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_August_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_September_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_October_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_November_2019.csv',
#     'learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_December_2019.csv'
# ]

# # Read all CSV files into DataFrames and concatenate them
# df_list = [pd.read_csv(file) for file in input_files]
# combined_df = pd.concat(df_list, ignore_index=True)

# # Write the combined DataFrame to a new CSV file
# combined_df.to_csv('learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/combined_sales_2019.csv', index=False)

# Read the combined CSV file
df = pd.read_csv('learning_ai/pandas_libary/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/combined_sales_2019.csv')

# Data Cleaning
# Drop rows with NaN values in all columns
df = df.dropna(how='all')

# Remove rows with invalid 'Order Date'
df = df[df['Order Date'].str[0:2] != 'Or']

# Convert columns to numeric, forcing errors to NaN
df[['Quantity Ordered', 'Price Each']] = df[['Quantity Ordered', 'Price Each']].apply(pd.to_numeric, errors='coerce')

# Fill NaN values with 0
df = df.fillna(0)

# Calculate total sales
df['total_sales'] = df['Quantity Ordered'] * df['Price Each']

# Extract month from 'Order Date' and create 'month' column
df['month'] = df['Order Date'].str[:2]

# Convert 'Order Date' to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Extract time from 'Order Date' and create 'hour' and 'minute' columns
df['hour'] = df['Order Date'].dt.hour
df['minute'] = df['Order Date'].dt.minute
df['Count'] = 1

# Group products by 'Order ID' for analysis
df1 = df[df['Order ID'].duplicated(keep=False)].copy()
df1['Grouped'] = df1.groupby('Order ID')['Product'].transform(lambda x: ", ".join(x))
df2 = df1[['Order ID', 'Grouped']].drop_duplicates()

# Count pairs of products sold together
count = Counter()
for row in df2['Grouped']:
    row_list = row.split(', ')
    count.update(Counter(combinations(row_list, 2)))

# Print the most common product pairs
for key, value in count.most_common(10):
    print(key, value)

# Extract city from 'Purchase Address' and create 'City' column
def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

df['City'] = df['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

# Group by month and calculate total sales for each month
monthly_sales = df.groupby('month')['total_sales'].sum()
cities_sales = df.groupby('City')['total_sales'].sum()


# Find the month and city with the maximum total sales
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()
best_city = cities_sales.idxmax()
best_city_sales = cities_sales.max()



# Print the best month and city for sales and their corresponding values
print("Best Month for Sales:", best_month)
print("Total Sales in that Month:", best_month_sales)
print("Best City for Sales:", best_city)
print("Total Sales in this City:", best_city_sales)


# Plotting best month sales
months = range(1, 13)
plt.bar(months, monthly_sales[:12])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month Number')
plt.title('Total Sales by Month')
plt.show()

# Plotting best city sales
cities = [city for city, x in df.groupby('City')]
plt.bar(cities, cities_sales)
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.title('Total Sales by City')
plt.show()

# Plotting best time for sales
hours = [hour for hour, x in df.groupby('hour')]
plt.plot(hours, df.groupby(['hour']).count())
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Orders')
plt.title('Order Frequency by Hour of the Day')
plt.grid()
plt.show()

# Group by product and sum the quantity ordered for each product
product_group = df.groupby('Product')['Quantity Ordered'].sum()

# Plotting most pair product sales
keys = product_group.index
plt.bar(keys, product_group)
plt.xticks(keys, rotation='vertical', size=8)
plt.xlabel('Product')
plt.ylabel('Quantity Ordered')
plt.title('Most Popular Products by Quantity Ordered')
plt.show()
# Assuming df is your DataFrame

# Convert 'Price Each' to numeric, coercing errors to NaN
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')

# Drop rows where 'Price Each' is NaN
df = df.dropna(subset=['Price Each'])

# Group by 'Product' and calculate the mean of 'Price Each'
prices = df.groupby('Product')['Price Each'].mean()

# Assuming 'keys' and 'product_group' are already defined
keys = prices.index.tolist()


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(keys, product_group, color='g')
ax2.plot(keys, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(keys, rotation='vertical', size=8)

plt.show()