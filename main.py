import os
import json
import requests
from google.cloud import bigquery
from datetime import datetime


secret_content = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if secret_content:
    # This cleans the text and saves it as a real file for the robot to use
    with open("google_key.json", "w") as f:
        f.write(secret_content.strip())
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
    print("✅ Key file created.")
else:
    print("❌ ERROR: Secret GOOGLE_APPLICATION_CREDENTIALS_JSON is missing!")


client = bigquery.Client()
project_id = "stock-tracker-491608"
table_id = f"{project_id}.STOCK_DATA.FACT_STOCK_PRICES"

symbols = ['AAPL', 'MSFT', 'GOOGL']
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY")

for s in symbols:
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={s}&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    
    if 'Global Quote' in data and data['Global Quote']:
        quote = data['Global Quote']
        rows_to_insert = [{
            "SYMBOL": s, 
            "PRICE_DATE": str(datetime.now().date()), 
            "CLOSE_PRICE": float(quote['05. price']), 
            "VOLUME": int(quote['06. volume'])
        }]

query = f"SELECT DISTINCT SYMBOL, PRICE_DATE FROM `{table_id}`"
existing_data = client.query(query).to_dataframe()

final_rows = []
for row in rows_to_insert:
    # Check if this specific combo exists
    exists = existing_data[(existing_data['SYMBOL'] == row['SYMBOL']) & 
                           (existing_data['PRICE_DATE'] == row['PRICE_DATE'])]
    
    if exists.empty:
        final_rows.append(row)
    else:
        print(f"Skipping {row['SYMBOL']} for {row['PRICE_DATE']} - Already exists!")

if final_rows:
    job = client.load_table_from_json(final_rows, table_id, job_config=job_config)
    job.result()
    print("New data added successfully!")
else:
    print("No new data to add today.")
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        try:
            job = client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
            job.result()
            print(f"✅ {s} price added to BigQuery.")
        except Exception as e:
            print(f"❌ BigQuery Error for {s}: {e}")
    else:
        print(f"⚠️ Could not get data for {s}. Check your API Key.")
