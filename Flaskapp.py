from flask import Flask, render_template
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from mongodb import MissionMarsDB

# Get the Data from MongoDc
mmars = MissionMarsDB()
result = mmars.find_top_1()
#If collection is empty insert data
if result == None:
    mmars.insert_data()
    result = mmars.find_top_1()

print(result)

app = Flask(__name__)
#

#
# @app.route('/showLineChart')
# def line():
#     pass
