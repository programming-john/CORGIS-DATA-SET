from flask import Flask, url_for, render_template, request, Markup, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

with open('immigration.json') as immigrants_data:
        data = json.load(immigrants_data)

def get_countries():
    cc = data[0]["Country"]
    countryset = []
    for c in data:
        countryset.append(c["Country"])
    countryset.sort()
    options = ""
    for country in countryset:
        if cc != country:
           options += Markup("<option value=" +'"'+ country +'"' +">" + country + "</option>")
           cc = country
    return options

def get_country_facts(country):
    fact = ""
    for c in data:
        if c["Country"] == country:
           fact += Markup("<p>"+ "Immigration from "+"<b>"+ c["Country"]+": </b>"+str(c["Data"]["Legal permanant residences"]["Last Residence"])+"<br>" + "Legal Residents by Birth: " + str(c["Data"]["Legal permanant residences"]["Birth"])+"<br>"+"Year: "+ str(c["Year"]) +"</p>")
    return fact

def get_country_enforcement(country):
    fact = ""
    for c in data:
        if c["Country"] == country:
           fact += Markup("<p>"+"Government action taken for: <b>" + c["Country"] + "</b><br>"+ "Non-Criminal: " + str(c["Data"]["Enforcement"]["Non-criminal"]) + "<br>" + "Criminal: " + str(c["Data"]["Enforcement"]["Criminal"]) + "<br>" + "Apprehended: "+ str(c["Data"]["Enforcement"]["Apprehended"]) + "<br>" + "Inadmissable: " + str(c["Data"]["Enforcement"]["Inadmissable"]) + "<br>" + "Year: "+ str(c["Year"]) + "</p>")
    return fact

def get_country_highest(country):
    fact = ""
    highest = data[0]["Data"]["Naturalizations (Birth)"]
    for c in data:
        if c["Country"] == country:
           if highest > c["Data"]["Naturalizations (Birth)"]:
                highest = c["Data"]["Naturalizations (Birth)"]
                fact = Markup("<p><b>" + c["Country"] + "</b> Highest naturalizations by birth is: " + str(highest) + " in "+ str(c["Year"]) + "</p>")
    return fact
        
@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/stats")
def render_stats():
    return render_template('countrystats.html', country= get_countries())

@app.route("/enforcement")
def render_enforcement():
    return render_template('enforcement.html',country=get_countries())

@app.route("/naturalizations")
def render_nat():
    return render_template('natbbirth.html',country=get_countries())

@app.route("/act", methods=['GET','POST'])
def render_result():
    place = request.args['dat']
    return render_template('countrystats.html', country=get_countries(), info=get_country_facts(place))

@app.route("/enf", methods=['GET','POST'])
def render_resultenforce():
    place = request.args['da']
    return render_template('enforcement.html', country=get_countries(), info=get_country_enforcement(place))

@app.route("/nat", methods=['GET','POST'])
def render_resultnat():
    place = request.args['d']
    return render_template('natbbirth.html', country=get_countries(), info=get_country_highest(place))


if __name__=="__main__":
    app.run(debug=False, port=54321)
