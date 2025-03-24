from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Fetch the webpage
url = "https://enam.gov.in/web/dashboard/trade-data"
driver.get(url)

# Allow time for JavaScript to load the table
time.sleep(5)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Locate the table
table_div = soup.find("div", class_="col-md-12 table-responsive")
if table_div:
    table = table_div.find("table")
    if table:
        rows = table.find_all("tr")

        # Extract headers
        headers = [header.text.strip() for header in rows[0].find_all("th")]

        # Extract rows
        data = []
        for row in rows[1:]:
            cols = row.find_all("td")
            data.append([col.text.strip() for col in cols])

        # Save to CSV
        with open("enam_trade_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

        print("Data successfully saved to 'enam_trade_data.csv'")
    else:
        print("Table not found on the page.")
else:
    print("Table container not found on the page.")

# Close the driver
driver.quit()
