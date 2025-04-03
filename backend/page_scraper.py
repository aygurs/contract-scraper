from bs4 import BeautifulSoup

def scrape_page(soup, url):

    #Make contract list and add URL first
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