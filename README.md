# automated-stock-data-pipeline

This is my project where I built an end-to-end data pipeline using **Python**, **GitHub Actions**, and **Google BigQuery**. It basically collects stock price data automatically and helps in real-time reporting using **Power BI**.

### Project Overview
In this project, I wanted to automate the ETL process (Extract, Transform, Load) for daily stock market data. Instead of me running the script every day, I used GitHub Actions to schedule it. Now, the latest data is automatically saved in the cloud (BigQuery) so I can see the trends whenever I want without any manual work.

### Why I built this?
The main goal was to learn how to handle real-time data and store it in a professional cloud warehouse like BigQuery. It helps in tracking how different stocks are performing and makes it easy to create a dashboard for analysis.

### Features
* **Automatic Data Fetching:** It gets stock prices using APIs (like yfinance) every day.
* **Cloud Storage:** All the data goes directly into Google BigQuery.
* **Automation:** I used GitHub Actions so the code runs on its own.
* **Data Cleaning:** Used Python Pandas to make sure the data is in the right format.
* **Dashboard:** Connected the BigQuery data to Power BI for clear charts.

### Tools I Used
1. **Python:** For writing the main logic and cleaning data.
2. **GitHub Actions:** To schedule and run the scripts automatically.
3. **Google BigQuery:** As my cloud database to store all records.
4. **Power BI:** To create the final report and see the trends.
5. **SQL:** To manage the tables inside BigQuery.

### How the Pipeline Works
1. **Extraction:** A Python script runs on a set schedule to pull the latest prices.
2. **Loading:** The script connects to Google Cloud using a service account and pushes the data to a BigQuery table.
3. **Visualization:** Power BI is connected to that table, so the dashboard refreshes with new data.

### Things I Analyzed
* **Price Changes:** Checking how much the price went up or down daily.
* **Moving Averages:** To see the long-term trend of the stocks.
* **Volume:** Tracking how many shares are being traded.

### How to use it
* First, you need to set up your **Google Cloud Credentials** in the GitHub Secrets section.
* You can change the stock names in the `main.py` file.
* Check the `.github/workflows/daily_run.yml` to see when the script will run.
* Finally, open the Power BI file and refresh it to see the latest data.

### Author
Janani Priya
