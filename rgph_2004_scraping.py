from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Category
indicator_category = 'typeProfil_2'

# Properties
indicator_website_name = ['Actifs', 'Actifs occupés et chômeurs ayant déjà travaillés']
indicator_class = ['xl26', 'xl24']
indicator_csv_name = ['active_population', 'employed_labor']

# Set up Selenium WebDriver (ensure chromedriver is installed)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("C:/Program Files/Google/chromedriver/chromedriver.exe")  # Path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the website
url = "https://applications-web.hcp.ma/hpmc/frmmarocenchiffres.aspx"
driver.get(url)
time.sleep(5)  # Allow page to load

# Function to get dropdown options
def get_dropdown_options(element_id):
    select = Select(driver.find_element(By.ID, element_id))
    options = [option.get_attribute("value") for option in select.options if option.get_attribute("value")]
    return options

# Get all regions
regions = get_dropdown_options("lRE")

# Data storage
results = []

# Function to get dropdown options (returns both value and text)
def get_dropdown_options_with_text(element_id):
    select = Select(driver.find_element(By.ID, element_id))
    options = select.options
    return [(option.get_attribute("value"), option.text.strip()) for option in options if option.get_attribute("value")]

# Iterate through all regions, provinces, and communes
for region_value, region_text in get_dropdown_options_with_text("lRE"):
    Select(driver.find_element(By.ID, "lRE")).select_by_value(region_value)
    time.sleep(2)

    # Get provinces for the selected region
    for province_value, province_text in get_dropdown_options_with_text("lPR"):
        Select(driver.find_element(By.ID, "lPR")).select_by_value(province_value)
        time.sleep(2)

        # Get communes for the selected province
        for commune_value, commune_text in get_dropdown_options_with_text("lCMA"):
            Select(driver.find_element(By.ID, "lCMA")).select_by_value(commune_value)
            time.sleep(2)

            # Click on the Economics tab
            econ_tab = driver.find_element(By.ID, f"{indicator_category}")
            econ_tab.click()
            time.sleep(2)


            data_dict = {
                "region": region_text,  # Stores the visible region name
                "province": province_text,  # Stores the visible province name
                "municipality": commune_text  # Stores the visible municipality name
            }

            for name, class_, csv_name in zip(indicator_website_name, indicator_class, indicator_csv_name):
                try:
                    value = driver.find_element(
                        By.XPATH,
                        f"//tr[td[@class='{class_}' and contains(., '{name}')]]/td[@class='xl25']"
                    ).text.strip()
                except:
                    value = "N/A"

                # Add new column dynamically
                data_dict[csv_name] = value


            results.append(data_dict)

            dynamic_values = " - ".join([f"{key}: {data_dict[key]}" for key in indicator_csv_name])
            print(
                f"Scraped: {data_dict['region']} - {data_dict['province']} - {data_dict['municipality']} - {dynamic_values}")


# Save results to CSV
df = pd.DataFrame(results)
df.to_csv("mor_economics_data.csv", index=False)

# Close Selenium
driver.quit()

print("Scraping completed and saved to maroc_economics_data.csv")
