import pandas as pd

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

# access the "Total Charged" column by its exact name
df["Total Owed"] = df["Total Owed"].str.replace('$','').astype(float)
print(df.head())

print(df["Total Owed"].sum())
print(df["Total Owed"].mean())