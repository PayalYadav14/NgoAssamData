import threading
import pandas as pd
from selenium import webdriver
import pandas as pd
from selenium import webdriver
from selenium import webdriver
import pandas as pd
import openpyxl

import time
from xml.dom.pulldom import END_ELEMENT
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import threading
import pandas as pd
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://ngodarpan.gov.in')
element = driver.find_element(By.PARTIAL_LINK_TEXT, "NGO Directory")
element.click()

time.sleep(5)

element1 = driver.find_element(By.XPATH,"/html/body/div[6]/div/div[1]/ul[1]/li[3]/ul/li[1]/a")
element1.click()

time.sleep(5)

element1 = driver.find_element(By.PARTIAL_LINK_TEXT, "ASSAM")
element1.click()

time.sleep(5)

def scrape_page(url):
    
    table=driver.find_element(By.XPATH,'/html/body/div[9]/div[1]/div[3]/div/div/div[2]/table')
    rows = table.find_elements(By.XPATH, "/html/body/div[9]/div[1]/div[3]/div/div/div[2]/table/tbody/tr")
    data = []
  

    for row_index, row in enumerate(rows[0:], start=0):
        
        link=row.find_element(By.TAG_NAME,'a')
        driver.execute_script("arguments[0].click();", link)
        time.sleep(5)
        table_elements=driver.find_elements(By.XPATH,'/html/body/div[9]/div[3]/div[2]/div/div[2]/div/div/table')
        for keyword in ["Unique Id of VO/NGO","Registered With","Designation","Key Issues","FCRA Available","Address"]:
        
            mytable= driver.find_element(By.XPATH,f"//*[contains(text(),'{keyword}')]")
            parent=mytable.find_element(By.XPATH,"..")
            table_rows=parent.find_elements(By.XPATH,"..")
          
            for a in table_rows:
                cells = a.find_elements(By.TAG_NAME,"tr")
                row_data = [cell.text for cell in cells]            
                data.append(row_data)
                time.sleep(3)

                button=driver.find_element(By.CSS_SELECTOR, '#ngo_info_modal > div.modal-dialog.modal-lg > div > div.modal-header > button')            
                driver.execute_script("arguments[0].click();", button)
                
    driver.quit()
    return data

 
# List of URLs to scrape
base_url = 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/2751/18/'
num_pages = 275
urls = [base_url + str(page_num) + '?' for page_num in range(1, num_pages + 1)]

# Create a thread for each URL and start scraping
threads = []
results = []  # Store the results from each thread

for url in urls:
    thread = threading.Thread(target=lambda: results.append(scrape_page(url)))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# All scraping is complete
print("Scraping finished!")

# Flatten the nested lists
flat_results = [item for sublist in results for item in sublist]

# Create a pandas DataFrame from the results
df = pd.DataFrame(flat_results[1:], columns=flat_results[0])

# Save the DataFrame to an Excel file
df.to_excel("aug.xlsx", index=False)

print("Data saved to data.xlsx")
