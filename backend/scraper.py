#Request HTML page (requests library)
#https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
import requests

#Scrape HTML page (BeautifulSoup library)
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

#Export data collected (Pandas library)
#https://pandas.pydata.org/docs/user_guide/index.html#user-guide
import pandas as pd

#Scraper function
def scrape_page(url):
    '''Scrape the awarded contract page for metadata'''

    #Send GET request to desired webpage using requests
    response = requests.get(url)

    #Create a 'soup' object of the HTML page requested
    #.text is a property from the requests object
    #Using lxml as a parser for faster response times
    soup = BeautifulSoup(response.text, "lxml")

    #Create dictionary to hold contract data
    #Add URL to contract
    contract = {"Contract URL": url}

    #Find title
    #Use find method of BeautifulSoup to extract information
    title = soup.find("h1", class_="govuk-heading-l break-word")
    #Use get_text method to strip any HTML + whitespace and extract pure text
    #Add data to Title if title is found, or No title if not
    contract["Title"] = title.get_text(strip=True) if title else "No title"

    #Find metadata in h4 tags
    h4_tags = soup.find_all("h4")
    for tag in h4_tags:
        #Collect subtitle and strip all HTML
        subtitle = tag.get_text(strip=True)

        #Collect industry data
        #ADD OPTION FOR WHEN THERE IS MORE THAN 1 INDUSTRY-----------
        if subtitle == "Industry":
            #Target the ul after the subtitle (Unique to industry only)
            ul = tag.find_next_sibling("ul")
            if ul:
                #If there is a ul, find the li element
                li = ul.find("li")
                if li:
                    #If there is a li element, get the text from it and strip HTML
                    contract["Industry"] = li.get_text(strip=True)

        #Collect location of contract
        elif subtitle == "Location of contract":
            #Target the p element after the subtitle
            p = tag.find_next_sibling("p")
            #Add location to contract data
            contract["Location of contract"] = p.get_text(strip=True) if p else "Unknown"
        
        #Collect value of contract
        elif subtitle == "Value of contract":
            #Target the p element after the subtitle
            p = tag.find_next_sibling("p")
            #Add location to contract data
            contract["Value"] = p.get_text(strip=True) if p else "Unknown"

        #Collect Published date
        elif subtitle == "Published date":
            #Target the p element after the subtitle
            p = tag.find_next_sibling("p")
            #Add location to contract data
            contract["Published Date"] = p.get_text(strip=True) if p else "Unknown"

            
    return contract

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
