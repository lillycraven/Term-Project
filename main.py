import pandas as pd
import math 
import matplotlib.pyplot as plt

# df = pd.read_csv('Retail.OrderHistory.1.csv')
# print(df.head())


# print(df.shape)

# df = df.fillna(0)
# print(df.head())

# df["Total Charged"] = df["Total Charged"].str.replace('$','').astype(float)
# print(df.head())

# print(df["Total Charged"].sum())

# df["Total Charged"].mean()

df = pd.read_csv('Retail.OrderHistory.1.csv')
print(df.head())
print(df.shape)

df = df.fillna(0)
print(df.head())

# strip leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()


# print(df["Total Owed"].sum())
# print(df["Total Owed"].mean())
# print(df["Total Owed"].median())
# print(df["Total Owed"].max())
# print(df["Total Owed"].min())



# print(df["Shipment Item Subtotal Tax"].sum())
# df["Shipment Item Subtotal Tax"] = pd.to_numeric(df["Shipment Item Subtotal Tax"], errors='coerce')
# df["Total Owed"] = pd.to_numeric(df["Total Owed"], errors='coerce')
# df = df.dropna(subset=["Shipment Item Subtotal Tax", "Total Owed"])

# print(df["Shipment Item Subtotal Tax"].sum() / df["Total Owed"].sum())

df['Order Date'] = pd.to_datetime(df['Order Date'])
print(df.head())

print(df.plot.bar(x='Order Date', y='Total Owed', rot=90))
plt.show()

print(df.plot.bar(x='Order Date', y='Total Owed', rot=90, figsize=(20,10)))
plt.show()

daily_orders = df.groupby('Order Date').sum()["Total Owed"]
daily_orders.head()

print(daily_orders.plot.bar(figsize=(20,10)))
plt.show()

print(daily_orders.plot.bar(figsize=(20, 10), color='#61D199'))
plt.show