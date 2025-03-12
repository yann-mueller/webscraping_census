# Web Scraping Moroccan Micro Census Data
The Federal Statistics Office in Morocco conducts a census every 10 years. Some of the data is prepared in Excel files while other data is only available on the website. The following presents code and instructions how to webscrape specific data for every municipality and store the results in a .csv file.

The code is written to scrape for the [RGPH 2004](https://applications-web.hcp.ma/hpmc/frmmarocenchiffres.aspx).

**Table of content:**
  - Data Source
  - Website Structure
  - Python Webscraping Code


**Scraped Files:**
Employed Labor per Municipality (.csv)


## Data Source
1) On the top left of the page, you can choose the region, province, and municipality (Commune, MU, AR, or AC)

![Municipality](https://github.com/user-attachments/assets/0850c288-66f3-48b8-997a-6d2f5aafa681)

2) Right below, one can choose among the available census categories
   
![Screenshot 2025-03-12 at 10-59-20 Page sans titre](https://github.com/user-attachments/assets/400c12e6-1272-41c3-b521-1f523d280c5e)

3) All available indicators for that category in the chosen municpality are shown

![Screenshot 2025-03-12 at 11-12-52 Page sans titre](https://github.com/user-attachments/assets/650fd564-8b43-4173-b992-c070aaf2f01f)

 ## Website Structure
The indicators for every municipality are listed in a *n x 3* table. So the HTML code is structure as follows:
> <tr>
> </tr>
