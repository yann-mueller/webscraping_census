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
