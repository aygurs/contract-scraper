#Scrape HTML page (BeautifulSoup library)
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

#Export data collected (Pandas library)
#https://pandas.pydata.org/docs/user_guide/index.html#user-guide
import pandas as pd

#Uses selenium to run web browser
#https://www.selenium.dev/documentation/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_scraper import scrape_page

#Scraper function
#WORKS ON CHROME ONLY
def navigate_search():
    '''Navigate gov website and open new tabs of results to scrape'''

    #Make dictionary to hold all contracts scraped
    contracts = []
    
    #Initialise the Chrome webdriver (built in to Selenium)
    driver = webdriver.Chrome()

    try:
        #Navigate to the Contracts Finder search page
        driver.get("https://www.contractsfinder.service.gov.uk/Search")

        #Set up a smart wait, waits for 10 seconds
        wait = WebDriverWait(driver, 10)

        #List of checkbox IDs to untick
        #All ID's taken from gov HTML that need to be un-ticked
        untick_ids = ["speculative", "planning", "tender"]
        
        #Un-tick each checkbox if it is selected
        for checkbox_id in untick_ids:
            #Wait until they have loaded (checks every 0.5s, method of WebDriverWait)
            #EC (expected_conditions) method to check for element
            #By to locate element
            checkbox = wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))
            if checkbox.is_selected():
                checkbox.click()

        #Tick the Awarded contracts checkbox
        awarded_checkbox = wait.until(EC.presence_of_element_located((By.ID, "awarded")))
        if not awarded_checkbox.is_selected():
            awarded_checkbox.click()

        #Click the search button (ID 'adv_search')
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "adv_search")))
        search_button.click()

        #Wait for the search results to load
        #Wait for at least one search result to load before scraping
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-result")))

        #Now results have loaded, capture all WebElement objects with that class
        result_links = driver.find_elements(By.CSS_SELECTOR, "a.govuk-link.search-result-rwh.break-word")

        #Get all URL strings from <a> captured above and store in a list to be used
        urls = [link.get_attribute("href") for link in result_links]

        #Loop through all urls captured
        for url in urls:
            #Use JS to open new tab in selenium window
            driver.execute_script("window.open('');")
            #Switch over to the tab opened
            driver.switch_to.window(driver.window_handles[-1])
            #Put the url into the new tab and direct to it
            driver.get(url)

            #Get the source of the tab open and parse it through BeautifulSoup using lxml
            soup = BeautifulSoup(driver.page_source, "lxml")
            #Use the scrape_page function of page_scraper.py
            contract = scrape_page(soup, url)
            #Add the dictionary of the contract returned to the list of contracts created
            contracts.append(contract)

            #Close the tab once all tasks are completed
            driver.close()
            #Switch back to search results
            driver.switch_to.window(driver.window_handles[0])

        #Return the contracts list
        return contracts

    finally:
        #Close the browser after the process is complete
        driver.quit()

#Save function to csv file
def save_to_csv(data, filename="contracts.csv"):
    '''Saves scraped contract data as a csv file'''
    
    #Creates a data frame using pandas (pd) and puts data into a table structure
    contract_dataframe = pd.DataFrame(data)

    #Convert to csv file, don't include index numbers in file
    contract_dataframe.to_csv(filename, index=False)

    #Prints confirmation to console
    print(f"Saved {len(data)} contracts to {filename}")

#Save function to excel file
def save_to_excel(data, filename="contracts.xlsx"):
    '''Saves scraped contract data as a excel file'''
    
    #Creates a data frame using pandas (pd) and puts data into a table structure
    contract_dataframe = pd.DataFrame(data)

    #Convert to csv file, don't include index numbers in file
    #Pandas uses openpyxl library to create excel file
    contract_dataframe.to_excel(filename, index=False)

    #Prints confirmation to console
    print(f"Saved {len(data)} contracts to {filename}")
