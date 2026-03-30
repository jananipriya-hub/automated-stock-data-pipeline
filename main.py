import os
import json
from google.cloud import bigquery
from datetime import datetime
import requests

if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
  with open("google_key.json", "w") as f:
    f.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
client = bigquery.Client()
project_id = "stock-tracker-491608"
table_id = f"{project_id}.STOCK_DATA.FACT_STOCK_PRICES"

symbols = ['AAPL','MSFT','GOOGL']
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY")

for s in symbols:
  url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={s}&apikey={API_KEY}'
  r = requests.get(url)
  data = r.json()

if 'GLOBAL QUOTE' in data:
  quote = data['GLOBAL QUOTE']
  rows_to_insert = [{"SYMBOL": s,"PRICE_DATE": str(datetime.now().date()),"CLOSE_PRICE": float(quote['05.price']),"VOLUME": int(quote['06.volumje'])}]

job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
try:
  job = client.load_table_from_json(rows_to_insert,table_id,job_config=job_config)
  job.result()
  print(f"Success! {s} added.")
except Exception as e:
  print(f"Error: {e}")
