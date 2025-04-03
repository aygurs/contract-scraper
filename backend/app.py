#https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
#Use Flask to allow backend and frontend to interact
from flask import Flask, request, jsonify
#Import scraper functions from scraper.py
from selenium_nav import navigate_search, save_to_csv, save_to_excel

#Create instance of class
app = Flask(__name__)

#Declare what route will trigger function
#Make Flask only respond to GET requests
@app.route("/scrape", methods=["GET"])
def scrape_data():
    '''Run the scraper and return a summary as JSON'''

    data = navigate_search()
    save_to_csv(data)
    save_to_excel(data)

    #Return response in JSON format using jsonify
    return jsonify({
        "message": "Scraping completed successfully",
        "data_found": len(data)
    })

#Only run when script is run directly, not imported
if __name__ == "__main__":
    #Debug true temporarily for dev testing
    app.run(debug=True)