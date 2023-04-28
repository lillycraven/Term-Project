import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import re
def read_data(file_path):
    """
    Reads a CSV file and returns a pandas dataframe.
    """
    df = pd.read_csv(file_path)
    return df
def clean_data(df):
    """
    Cleans a dataframe by filling NaN values with 0 and stripping whitespace from column names.
    """
    df = df.fillna(0)
    df.columns = df.columns.str.strip()
    return df
def calculate_monthly_totals(df):
    """
    Calculates the total amount owed per month and returns a pandas Series.
    """
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    monthly_totals = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Total Owed'].sum()
    return monthly_totals
def plot_monthly_totals(monthly_totals):
    """
    Plots a bar chart of monthly totals and returns the plot object.
    """
    fig, ax = plt.subplots()
    ax.bar(monthly_totals.index.strftime('%b'), monthly_totals.values, color='pink')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Amount in Purchases ($)')
    ax.set_title('Total Purchases by Month (2022)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center')
    return ax
def add_statistics_to_plot(ax, monthly_totals):
    """
    Adds statistics to a plot of monthly totals.
    """
    # calculate statistics
    total_sum = monthly_totals.sum()
    total_mean = monthly_totals.mean()
    total_median = monthly_totals.median()
    total_max = monthly_totals.max()
    total_min = monthly_totals.min()
    # format statistics as text
    text = f"Total: ${total_sum:.2f}\nMean: ${total_mean:.2f}\nMedian: ${total_median:.2f}\nMax: ${total_max:.2f}\nMin: ${total_min:.2f}"
    # add text box to plot
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
def plot_monthly_totals_with_statistics(df, save_path=None):
    """
    Plots a bar chart of monthly totals and adds statistics to the plot.
    """
    monthly_totals = calculate_monthly_totals(df)
    ax = plot_monthly_totals(monthly_totals)
    add_statistics_to_plot(ax, monthly_totals)
    if save_path is not None:
        plt.savefig('static/monthlytotals.png')
    plt.show()
def plot_monthly_totals_with_percentages(monthly_totals, save_path=None):
    """Plot a bar chart of the monthly totals with an average budget line and percentage change labels."""
    monthly_totals = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Total Owed'].sum()
    fig, ax = plt.subplots()
    ax.bar(monthly_totals.index.strftime('%b'), monthly_totals.values, color='pink')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Amount in Purchases($)')
    ax.set_title('Total Purchases by Month (2022)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center')
    # plt.show()
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    # calculate the percent change between each month's total purchases and the previous month's total purchases
    monthly_pct_change = monthly_totals.pct_change()
    # add text labels indicating which months had an increase in purchases
    for i, val in enumerate(monthly_pct_change):
        if val > 0:
            ax.text(i, monthly_totals[i], f'+{val:.2%}', ha='center', va='bottom', color='green')
        elif val < 0:
            ax.text(i, monthly_totals[i], f'{val:.2%}', ha='center', va='top', color='red')
    # calculate the average monthly budget based on total purchases
    avg_budget = monthly_totals.mean()
    user_budget = int(input("Please enter what your expected monthly budget was: "))
    # add a horizontal line to the chart to indicate the average budget
    ax.axhline(avg_budget, color='red', linestyle='--', linewidth=2, label=f'Average Monthly Budget: ${avg_budget:.2f}')
    ax.axhline(user_budget, color='blue', linestyle='--', linewidth=2, label=f'Planned Monthly Budget: ${user_budget:.2f}')
    # display the legend
    ax.legend()
    if save_path is not None:
        plt.savefig('static/monthlytotalswpercent.png')
    plt.show()
def plot_daily_orders(df, save_path=None):
    """
    Plots a bar chart of daily orders.
    """
    df['Order Date'] = pd.to_datetime(df['Order Date']).dt.date
    daily_orders = df.groupby('Order Date')['Total Owed'].sum()
    with plt.style.context('ggplot'):
        fig, ax = plt.subplots(figsize=(20, 10))
        daily_orders.plot(kind='bar', color='#61D199', ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Purchase Total ($)')
        ax.set_title('Total Purchases by Day (2022)')
        ax.set_xticklabels([d.strftime('%b %d') for d in daily_orders.index], rotation=90, ha='center')
        if save_path is not None:
            plt.savefig('static/dailyorders.png')
        plt.show()
def heat_map(df, save_path=None):
    # Convert the Order Date column to a datetime object
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    # Group the orders by day of the week and time of day
    df['Weekday'] = df['Order Date'].dt.weekday
    df['Hour'] = df['Order Date'].dt.hour
    grouped = df.groupby(['Weekday', 'Hour'])['Total Owed'].apply(pd.to_numeric, errors='coerce').sum()
        # Create a pivot table with the total spending for each weekday and hour combination
    pivoted = pd.pivot_table(df, values='Total Owed', index='Hour', columns='Weekday', aggfunc=np.sum)
    # Create a heatmap of the spending by weekday and hour
    plt.figure(figsize=(10,8))
    sns.heatmap(pivoted, cmap='YlGnBu')
    plt.title('Spending by Weekday and Hour')
    plt.xlabel('Weekday')
    plt.ylabel('Hour')
    if save_path is not None:
        plt.savefig('static/heat_map.png')
    plt.show()
def location_graph(df, save_path = None):
    # Extract the zip code from the shipping address using regular expressions
    df['Zip Code'] = df['Shipping Address'].apply(lambda x: re.search(r'\b\d{5}(?:-\d{4})?\b', x).group(0))
    # Group the orders by zip code and count the frequency of each zip code
    zip_counts = df.groupby('Zip Code')['Order ID'].count().reset_index(name='Count')
    # Plot a histogram of the zip code frequency
    plt.bar(zip_counts['Zip Code'], zip_counts['Count'])
    plt.xlabel('Zip Code')
    plt.ylabel('Order Count')
    plt.title('Frequency of Orders by Zip Code')
    if save_path is not None:
         plt.savefig('static/locationgraph.png')
    plt.show()
if __name__ == "__main__":
    # read data
    df = read_data('Retail.OrderHistory.1.csv')
    # clean data
    df = clean_data(df)
    # plot monthly totals with statistics
    plot_monthly_totals_with_statistics(df, save_path='monthly_totals.png')
    plot_monthly_totals_with_percentages(df, save_path='monthly_percentages.png')
    heat_map(df, save_path='heat_map.png')
    plot_daily_orders(df, save_path='daily_orders.png')
    location_graph(df, save_path = 'location_graph.png')