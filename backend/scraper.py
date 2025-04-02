#Request HTML page (requests library)
#https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
import requests

#Scrape HTML page (BeautifulSoup library)
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

#Export data collected (Pandas library)
#https://pandas.pydata.org/docs/user_guide/index.html#user-guide
import pandas as pd

#Parameters we need to add to HTTP request (key:value pairs)
#Can change page by using key:value pairs in parameters
#Can add further filters down the line
PARAMS = {
    "awardNoticeFilter": "Yes",
    "page": 1
}

#Scraper function
#Default page number to 1 if no page number is given
def scrape_page(page=1):
    '''Scrape a single page of the awarded contracts results'''

    #Update page in params to page requested
    PARAMS["page"] = page

    #Send GET request to desired webpage using requests
    response = requests.get("https://www.contractsfinder.service.gov.uk/Search/Results", params=PARAMS)

    #Create a 'soup' object of the HTML page requested
    #.text is a property from the requests object
    #Using lxml as a parser for faster response times
    soup = BeautifulSoup(response.text, "lxml")

    #Create list to hold dictionaries of data
    contracts = []

    #Find all awarded contracts on page and assign them to the variable
    #Will be a list of all found search results separated by commas
    #Gov website uses class search_result in each result div
    search_results = soup.find_all("div", class_="search-result")

    #Loop through each found contract to extract the data from them
    for result in search_results:
        #Title is held as a link on Gov website, extract title and link
        #Use find method of BeautifulSoup to extract information
        #Also use get_text method to strip any HTML + whitespace and extract pure text
        title_tag = result.find("a", class_="search-result-header__title")
        #Handle case of no title
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = "No title"

        #Extract link from result title
        raw_link = result.find("a")
        #If there is no link, the url is then just None, instead of returning a link with None at the end
        if raw_link and raw_link.get("href"):
            result_link = "https://www.contractsfinder.service.gov.uk" + raw_link.get("href")
        else:
            result_link = None

        #Start of the dictionary of this specific contract
        contract = {
            "Title": title,
            "URL": result_link
        }

        #Extract remaining metadata from the entries and add to dictionary
        entries = result.find_all("div", class_="search-result-entry")
        for entry in entries:
            #Finds the part of the data in bold
            key_value = entry.find("strong")
            if key_value:
                key = key_value.get_text(strip=True)
                #Handles case where there is no more text after a bold section
                if key_value.next_sibling:
                    value = key_value.next_sibling.strip()
                else:
                    value = None
                #Add data to contracts list
                contract[key] = value
        
        #Add dictionary to main contracts list
        contracts.append(contract)
    
    #Return the completed contracts list
    return contracts

#Save function to csv file
def save_to_csv(data, filename="contracts.csv"):
    '''Saves scraped contract data as a csv file'''
    
    #Creates a data frame using pandas (pd) and puts data into a table structure
    contracts_dataframe = pd.DataFrame(data)

    #Convert to csv file, don't include index numbers in file
    contracts_dataframe.to_csv(filename, index=False)

    #Prints confirmation to console
    print(f"Saved {len(data)} contracts to {filename}")

#Save function to excel file
def save_to_excel(data, filename="contracts.xlsx"):
    '''Saves scraped contract data as a excel file'''
    
    #Creates a data frame using pandas (pd) and puts data into a table structure
    contracts_dataframe = pd.DataFrame(data)

    #Convert to csv file, don't include index numbers in file
    #Pandas uses openpyxl library to create excel file
    contracts_dataframe.to_excel(filename, index=False)

    #Prints confirmation to console
    print(f"Saved {len(data)} contracts to {filename}")
