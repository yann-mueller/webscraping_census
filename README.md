# Web Scraping Moroccan Micro Census Data
The Federal Statistics Office in Morocco conducts a census every 10 years. Some of the data is prepared in Excel files while other data is only available on the website. The following presents code and instructions how to webscrape specific data for every municipality and store the results in a .csv file.

The code is written to scrape for the [RGPH 2004](https://applications-web.hcp.ma/hpmc/frmmarocenchiffres.aspx).

**Table of content:**
  - [Data Source](#data-source)
  - [Website Structure](#website-structure)
  - [Python Webscraping Code](#python-webscraping-code)


**Scraped Files:**
Employed Labor per Municipality (![.csv](https://github.com/yann-mueller/webscraping_census/blob/main/mor_scraping_example.csv))


## Data Source
1) On the top left of the page, you can choose the region, province, and municipality (Commune, MU, AR, or AC)

![Municipality](https://github.com/user-attachments/assets/0850c288-66f3-48b8-997a-6d2f5aafa681)

2) Right below, one can choose among the available census categories
   
![Screenshot 2025-03-12 at 10-59-20 Page sans titre](https://github.com/user-attachments/assets/400c12e6-1272-41c3-b521-1f523d280c5e)

3) All available indicators for that category in the chosen municpality are shown

![Screenshot 2025-03-12 at 11-12-52 Page sans titre](https://github.com/user-attachments/assets/650fd564-8b43-4173-b992-c070aaf2f01f)

 ## Website Structure
The indicators for every municipality are listed in an *n x 3* table. The HTML code for <ins>one specific row</ins> is structured as follows:

```
<tr>
  <td class="xl27"> Economic Indicator </td>
  <td class="xl25"> 11 821</td>
  <td class="xl25"> 9.2</td>
</tr>
```
The name of the indicator is in the first *\<td>* block while the total number of the indicator and the percentage are in the second and third *\<td>* block, respectively. The second and third block have class *"xl25"* while the class of the first *\<td>* block varies with the indicator. So the idea of the code is to search for a *\<td>* block that contains the text of a specific indicator. Then, the value within the subsequent *\<td class="xl25">* block is stored together with the municipality name.

 ## Python Webscraping Code
 **Essentials** *(Adjust code as nessecary)*


 The following contains some notes on the functioning of the webscraping code.
 ```
# Category
indicator_category = 'typeProfil_2'

# Properties
indicator_website_name = ['Actifs', 'Actifs occupés et chômeurs ayant déjà travaillés']
indicator_class = ['xl26', 'xl24']
indicator_csv_name = ['active_population', 'employed_labor']
```
**Indicator Category:**
- Démographiques Générales: *'typeProfil_0'*
- Sociales: *'typeProfil_1'*
- Economies: *'typeProfil_2'*
- Condition d'Habitat des Ménages: *'typeProfil_3'*

**Indicator Properties:**  
In the beginning of the code, enter the amount of desired indicators you want to scrape. You can scrape as many as you wish from on specific category. For every indicator, also store the corresponding *\<td>* block class and the corresponding name in the final *.csv* file.

---

 **Optional** *(Code explanations, no adjustments nessecary)*

 ```
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
```
The above code loops through all regions, provinces, and municipalities for which the given indicator category is selected.

```
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
```
This code snippet creates a dataframe that stores the results of indicators that were selected. The correct elements on the webpage are located using the Selenium package with the *find_element()* function. The elements are located using *By.XPATH* while the first *\<td>* block is located by looking for the given class reference and the value is then selected from the subsequent *\<td class="xl25">* block.
