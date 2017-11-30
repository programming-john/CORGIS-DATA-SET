from flask import Flask, url_for, render_template, request, Markup, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

with open('immigration.json') as immigrants_data:
        data = json.load(immigrants_data)

def get_years():
    options = ""
    firstYear = 2004
    for c in data:
        if c["Year"] != firstYear:
            options += Markup("<option value=" +'"'+ str(c["Year"]) +'"' +">" + str(c["Year"]) + "</option>")
            firstYear = c["Year"]
    return options

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
           fact += Markup("<p>"+ "Immigration from "+"<b>"+ c["Country"]+": </b>"+str(c["Data"]["Legal permanant residences"]["Last Residence"])+"<br>" + "Legal Residents by Birth: " + str(c["Data"]["Legal permanant residences"]["Birth"])+"<br>"+"Naturalizations by birth: "+ str(c["Data"]["Naturalizations (Birth)"])+"<br>"+"Year: "+ str(c["Year"]) +"</p>")
    return fact

def get_country_enforcement(country):
    fact = ""
    for c in data:
        if c["Country"] == country:
           fact += Markup("<p>"+"Government action taken for: <b>" + c["Country"] + "</b><br>"+ "Non-Criminal: " + str(c["Data"]["Enforcement"]["Non-criminal"]) + "<br>" + "Criminal: " + str(c["Data"]["Enforcement"]["Criminal"]) + "<br>" + "Apprehended: "+ str(c["Data"]["Enforcement"]["Apprehended"]) + "<br>" + "Inadmissable: " + str(c["Data"]["Enforcement"]["Inadmissable"]) + "<br>" + "Year: "+ str(c["Year"]) + "</p>")
    return fact

def get_country_highest(country):
    fact = ""
    li = []
    for c in data:
        if c["Country"] == country:
           li.append(c["Data"]["Naturalizations (Birth)"])
    highest = li[0]
    for it in li:
        if highest < it:
           highest = it
    year = 0
    for c in data:
        if c["Country"] == country:
           if highest == c["Data"]["Naturalizations (Birth)"]:
                year = c["Year"]
    fact = Markup("<p>" + "The highest Naturalizations by birth in <b>" + country + "</b> is " + str(highest) + " in <b>" + str(year) +"</b></p>")
    return fact
    
def get_immigration_totals(year):
    total = 0
    for c in data:
        if c["Year"] == year:
            if c["Data"]["Naturalizations (Birth)"] != -1:
                total += c["Data"]["Naturalizations (Birth)"]
    return total
    
def get_bilrstat(type, country, year):
    stat = 0
    if type == 1:
        for c in data:
            if c["Country"] == country:
                if c["Year"] == int(year):
                     bi = c["Data"]["Nonimmigrant Admissions"]["Birth"]
                     lr = c["Data"]["Nonimmigrant Admissions"]["Last Residence"]
                     whole = bi + lr
                     stat = (bi/whole)*100
    if type == 2:
        for c in data:
            if c["Country"] == country:
                if c["Year"] == int(year):
                     bi = c["Data"]["Nonimmigrant Admissions"]["Birth"]
                     lr = c["Data"]["Nonimmigrant Admissions"]["Last Residence"]
                     whole = bi + lr
                     stat = (lr/whole)*100               
    return stat
        
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
    
@app.route("/bargraph")
def render_bargraph():
    return render_template('bar.html',fiv = get_immigration_totals(2005),six = get_immigration_totals(2006),sev = get_immigration_totals(2007),eig = get_immigration_totals(2008),nin = get_immigration_totals(2009),ten = get_immigration_totals(2010),ele = get_immigration_totals(2011),twe = get_immigration_totals(2012),thi = get_immigration_totals(2013),fou = get_immigration_totals(2014))

@app.route("/pie")
def render_pie():
        return render_template('piechart.html',country=get_countries(), anos=get_years())

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
    
@app.route("/piechart", methods=['GET','POST'])
def render_piechart():
    place = request.args['daf']
    years  = request.args['leyears']
    return render_template('piechart.html', country=get_countries(), anos = get_years(), bi = get_bilrstat(1,place, years), lr = get_bilrstat(2,place, years), year = years, palace = place)


if __name__=="__main__":
    app.run(debug=True, port=54321)
