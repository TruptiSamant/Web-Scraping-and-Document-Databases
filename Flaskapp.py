from flask import Flask, render_template
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from mongodb import MissionMarsDB
from  datetime import datetime

#############################################################################
def scrap_data():
    # Get the Data from MongoDc
    mmars = MissionMarsDB()
    result = mmars.find_top_1()
    #If collection is empty insert data
    if result == None:
        mmars.insert_data()
        result = mmars.find_top_1()

    return result
##############################################################################

app = Flask(__name__)

####################################################################################
@app.route('/')
def index():
    print("index ScrapeData")
    text = ""
    result = scrap_data()

    return render_template("index.html", text=text, result=result)

#################################################################################
@app.route('/scrape')
def scrape():
    print("ScrapeData")
    text=""
    mmars = MissionMarsDB()
    if (mmars.insert_data() == False):
        text = "Data up-to-date. Last update: " + datetime.now().strftime("%Y-%m-%d")

    result = mmars.find_top_1()
    return render_template("index.html", text=text, result=result)
################################################################################
################################################################################
if __name__ == '__main__':
    app.run(debug=True)
