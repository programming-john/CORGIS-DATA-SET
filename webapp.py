from flask import Flask, url_for, render_template, request, Markup, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

with open('immigration.json') as immigrants_data:
        data = json.load(immigrants_data)

def get_countries():
    country = data[0]["Country"]
    op = ""
    for c in data:
        if country != c["Country"]:
            op += Markup("<option value=" + country +">" + country + "</option>")
            state = c["Country"]
    return op        
        
@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/stats")
def render_stats():
    return render_template('countrystats.html', country= get_countries())

if __name__=="__main__":
    app.run(debug=False, port=54321)
