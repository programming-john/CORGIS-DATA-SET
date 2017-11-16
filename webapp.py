from flask import Flask, url_for, render_template, request, Markup, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

with open('immigration.json') as immigrants_data:
        data = json.load(immigrants_data)

def get_countries():
    op = ""
    for c in data:
        op += Markup("<option value=" +'"'+ c["Country"] +'"' +">" + c["Country"] + "</option>")
    return op

def get_country_facts(country):
    fact = ""
    for c in data:
        if c["Country"] == country:
           fact += Markup("<p>"+ "Immigration from "+ c["Country"]+": "+str(c["Data"]["Legal permanant residences"]["Last Residence"])+"<br>" + "Legal Residents by Birth: " + str(c["Data"]["Legal permanant residences"]["Birth"])+"<br>"+"Year: "+ str(c["Year"]) +"</p>")
    return fact

def get_country_enforcement(country):
    fact = ""
    for c in data:
        if c["Country"] == country:
           fact += Markup("<p>"+"Non-Criminal: "+str(c["Enforcement"]["Non-criminal"])+"<br>"+ "Criminal: "+ str(c["Enforcement"]["Criminal"])+"<br>"+"Apprehended: "+ str(c["Enforcement"]["Apprehended"]) +"<br>"+ "Inadmissable: "+str(c["Enforcement"]["Inadmissable"]) +"<br>"+"Year: "+ str(c["Year"]) + "</p>")
    return fact
        
@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/stats")
def render_stats():
    return render_template('countrystats.html', country= get_countries())

@app.route("/enforcement")
def render_enforcement():
    return render_template('enforcement.html')

@app.route("/act", methods=['GET','POST'])
def render_result():
    place = request.args['dat']
    return render_template('countrystats.html', country=get_countries(), info=get_country_facts(place))

@app.route("/enf", methods=['GET','POST'])
def render_resultenforce():
    place = request.args['da']
    return render_template('countrystats.html', country=get_countries(), info=get_country_enforcement(place))


if __name__=="__main__":
    app.run(debug=False, port=54321)
