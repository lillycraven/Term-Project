from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def chart():
    df = pd.read_csv('Retail.OrderHistory.1.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip()
    df["Total Owed"] = pd.to_numeric(df["Total Owed"], errors='coerce')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    monthly_totals = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Total Owed'].sum()

    fig, ax = plt.subplots()
    ax.bar(monthly_totals.index.strftime('%b %Y'), monthly_totals.values, color='pink')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Purchases')
    ax.set_title('Total Purchases by Month')
    
    monthly_pct_change = monthly_totals.pct_change()
    for i, val in enumerate(monthly_pct_change):
        if val > 0:
            ax.text(i, monthly_totals[i], f'+{val:.2%}', ha='center', va='bottom', color='green')
        elif val < 0:
            ax.text(i, monthly_totals[i], f'{val:.2%}', ha='center', va='top', color='red')
    avg_budget = monthly_totals.mean()
    ax.axhline(avg_budget, color='red', linestyle='--', linewidth=2, label=f'Average Monthly Budget: ${avg_budget:.2f}')
    ax.legend()
    
    # Save the chart to a bytes buffer
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    
    # Encode the bytes as a base64 string for embedding in HTML
    img_base64 = base64.b64encode(img_bytes.read()).decode()
    
    # Render the chart on a web page
    return render_template('index.html', image=img_base64)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run()