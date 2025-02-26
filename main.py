from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

webdriver_path = "chromedriver.exe"

service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

model_class = ".WoAzt.dzuXc._titleText_4bb51_15"
price_class = ".WoAzt.f7iqP._priceText_4bb51_113"

wait = WebDriverWait(driver, 10)

csv_file = "cars.csv"

for i in range(1, 11):
    page_url = f"https://www.cargurus.ca/Cars/spt-used-cars-Winnipeg_L284483#resultsPage={i}"
    driver.get(page_url)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, model_class)))
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        models = soup.select(model_class)
        prices = soup.select(price_class)

        models = [model.get_text(strip=True) for model in models]
        prices = [int(price.get_text(strip=True).replace("$", "").replace(",", "")) for price in prices]

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            for model, price in zip(models, prices):
                df = pd.DataFrame({
                    "model": [model],
                    "price": [price]
                })

                df.to_csv(file, header=False, index=False)

    except Exception as e:
        print(f"Error on page {i}: {e}")
        continue

driver.quit()

data = pd.read_csv("cars.csv")
data.sort_values(by=["price"], ascending=True, inplace=True)
data.to_csv("cars.csv")

print("\n\nBest Cars By Price\n\n")
print(pd.read_csv("cars.csv").head(10))