#TODO:
#-Add attribution for mars image
#-Seperate page for each connection
#-Settings 

#importing all potential dependices for fasthtml
from IPython import display
from enum import Enum
from pprint import pprint
from fasthtml.common import *
from fasthtml.common import Table as TB 
from fastcore.test import *
from starlette.testclient import TestClient
from starlette.requests import Headers
from starlette.datastructures import UploadFile
from fastapi.staticfiles import StaticFiles

from fh_bootstrap import *
from itertools import chain
from markdown import markdown

#importing all dependecies for the back end
from PIL import Image
import time
import numpy as np #requirement for matplotlib
import random 
import matplotlib.pyplot as plt #plotting
import mysql.connector #database
import tabulate #table formatting
import sys #system specific parameters and functions
import subprocess #running shell commands
import io #this and the below are for making matplotlib work with fasthtml by converting the graph into a base64 image =
from io import BytesIO
import base64
import csv #writing csv file 
from html2image import Html2Image 
import pandas as pd #for the table to image function


css = Style('html, body {background-image: url(/static/800px-VallesMarinerisHuge.jpg); background-size: cover; background-position: center; background-repeat: no-repeat; height: 100%; margin: 0; padding: 0;}',
            '''
            .table-container {
                width: 100%;
                overflow-x: auto;
            }
            table {
                table-layout: auto;
                width: auto !important;
                height: auto !important;
                min-width: 100%;
                background-color: rgba(255, 255, 255, 0.8);
            }
            table tr td {
                border: 1px solid black;
                color: black;
                white-space: nowrap;
                padding: 5px;
                width: 1px !important;
                text-shadow: 0px 0px 0px black;
            }
            table tr td:last-of-type {
                border: 1px solid black;
            }

            body {
                color: white;
                text-shadow: 1px 1px 1px black;
            }

            ''')
app = FastHTML(hdrs=(picolink,css), static_dir='./static')
app.mount("/static", StaticFiles(directory="static"), name="static")
client=TestClient(app)

def pageSelect():
    pages = (
        )
    
    navbar_css = """
    .navbar {

        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }   
    .navbar a {
        float: left;
        color: #ffffff;
        text-align: center;
        padding: 14px 30px;
        text-decoration: none;
        font-size: 25px;
    }
    .navbar a:hover {
        background-color: #3aa69f;
        color: black;
    }
    
    """

    n = Div(
        A('Insert', href="/"),
        A("Game Statistics Tables", href="/GStatsT"),
        A("Game Statistics Graphs", href="/GStatsG"),  
        A("Help & Info", href="/info"),
        cls="navbar"
    )

    return (Head(Title("FastHTML Navbar"),Style(navbar_css)),Body(n))

def htmlTableToCSV(hTable):
    r=pd.read_html(hTable)[0]
    csv=r.to_csv(index=False)
    return csv

def Table(cmd):
    #opening connection
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()
    
    #getting information from the database
    cursor.execute(cmd)
    fieldNames=[i[0] for i in cursor.description]
    result=cursor.fetchall()

    #building table 
    table=()
    headers=()
    nColumn=len(fieldNames)
    for i in range(nColumn):
        headers+=(Th(fieldNames[i]),)
    
        
    table+=Tr(headers),
    for i in range(len(result)):
        data=()
        for j in range(nColumn):
            data+=Td(result[i][j]),
        table+=Tr(data),

    #closing connection 
    cursor.close()
    cnx.close()

    #returning table
    return(Div(TB(table), cls="table-container"))

def scatter2columns(xName, xData, yName, yData,labels):

    plt.xlabel(labels[0])  #adding labels 
    plt.ylabel(labels[1])
    #calculating the trendline equation and converting it to right form 
    b=np.polyfit(xData, yData, 1)
    p=np.poly1d(b)
    
    #defining graphs 
    plt.scatter(xData, yData)
    plt.plot(xData, p(xData), color='red') #trendline

    #modifying axis(and adding axis lines)
    
    plt.axhline(0,color='black') 
    plt.axvline(0,color='black') 
        
    lim=max(max(xData),max(yData))+10
    m=min([min(xData),min(yData)])
    print(m)
    if m>(-10):
        plt.xlim(-10,lim)
        plt.ylim(-10,lim)
    else:
        plt.xlim(m,lim)
        plt.ylim(m,lim)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    #converting to base64
    buf=io.BytesIO()
    plt.savefig(buf, format='png')
    string=base64.b64encode(buf.getbuffer()).decode('utf-8')
    plt.clf()

    return f'data:image/png;base64,{string}'
    

def dataFetch(table,column):
    ##print(table,column)
    #opening connection
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()

    #getting data from the database
    cursor.execute("select " + column + "  from " + table)
    value=cursor.fetchall()

    for i in range(len(value)):       #looping over the columns and converting them from tuple to int 
        try:
            value[i]=int(value[i][0])
        except ValueError:
            input("collumn must only contain floats")

    #closing connection 
    cursor.close()
    cnx.close()
    return(value)
    
@app.get("/")
def home():
    return Main(
        Img(src="/static/mars.jpg", alt="Mars"),
        pageSelect(),
        P("Insert Link:", style="font-size: 1.2em;"),
        Form(
            Div(
                Input(type="text", name="data", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                Button("Submit", style="height: 52px; width: 200px; padding: 15 15px;"),
                style="display: flex; align-items: stretch;"
            ),
            action="/Insert",
            method="post"
        )
    )

@app.post("/Insert")
def addTable(data:str):
    print("getting data")
    subprocess.run(["bash","getter.sh",data])
    return home()

tableView=()
      
@app.get("/GStatsT")
def page2():

    #defining input types
    types=[("Show Table","/Table"),("Download as CSV","/DownloadCSV"),("Download as PNG","/DownloadIMG")]

    return Main(pageSelect(),P(style="font-size: 2em; color: #8fffdf"),
                Form(
                    
                    Input(type="text", name="data", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Select(
                        *[Option(label, value=query) for label, query in types],
                        name="action",
                        style="flex-grow: 1; margin-right: 10px; height: 52px; max-width: 200px; padding: 15px 15px;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15px 15px;"),
                    style="display: flex; align-items: stretch;",
                    
                    action="/HandleAction", method="post"),
                    tableView)

graphsQuestions=["Table for X","Column for X","Table for Y","Column for Y"]
graphData=[]
graphView=()

@app.get("/GStatsG")
def page3():
    types=[("Show Graph", "0"),("Download Graph","2")]
    return Main(pageSelect(),P(style="font-size: 1.2em;"),
                Form(
                    
                    Input(type="text", name="data", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Select(
                        *[Option(label, value=query) for label, query in types],
                        name="action",
                        style="flex-grow: 1; margin-right: 10px; height: 52px; max-width: 175px; padding: 15px 15px;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15 15px;"),
                    style="display: flex; align-items: stretch;",
                    action="/Graph", method="post"),
                    graphView)

@app.post("/HandleAction")
def handleAction(action:str, data:str):
    if action=="/Table":
        return addTable(data)
    elif action=="/DownloadCSV":
        return downloadCSV(data)
    elif action=="/DownloadIMG":
        return downloadIMG(data)
    else:
        return page2() #in case of error

@app.post("/DownloadGraph")

@app.post("/DownloadIMG")
def downloadIMG(data:str):
    #downloading the table as an image requires a webdriver, which I don't want to add to the project and so I am using matplotlib to make a table and then convert that to png 
    
    #opening connection
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()
    
    #getting information from the database
    cursor.execute(data)
    fieldNames=[i[0] for i in cursor.description]
    result=cursor.fetchall()
    #converting to pandas format and closign connection
    df=pd.read_sql(data,cnx)
    cnx.close()

    #defining matplotlib table
    fig, ax = plt.subplots(figsize=(12,6))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    #adjust style
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    table.auto_set_column_width(col=list(range(len(df.columns))))
    table.scale(1,1.5)
    fig.tight_layout()
    
    #converting to image
    buf=io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", pad_inches=0.3)
    buf.seek(0)
    img=buf.getvalue()
    plt.clf()
    
    return Response(
        content=img,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=table.png"}
    )


@app.post("/DownloadCSV")
def downloadCSV(data:str):
    #opening connection
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()
    
    #getting information from the database
    cursor.execute(data)
    fieldNames=[i[0] for i in cursor.description]
    result=cursor.fetchall()

    #formatting to csv 
    output=io.StringIO()
    csvWriter = csv.writer(output)
    
    csvWriter.writerow(fieldNames)

    csvWriter.writerows(result)

    #getting string and closing connection
    csvStr=output.getvalue()
    output.close()

    # Closing connection 
    cursor.close()
    cnx.close()
    
    return Response(
        content=csvStr,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )

@app.post("/Table")
def addTable(data:str):
    global tableView
    tableView=(Table(data),)+tableView
    return page2()  

@app.post("/Graph")
def processGraphData(action:str, data:str):
    print(action)
    global graphData
    global graphView
    graphData.append(data)
    if len(graphData)==4:
        labels=[graphData[1],graphData[3]]
        graphData[1]=dataFetch(graphData[0],graphData[1])
        graphData[3]=dataFetch(graphData[2],graphData[3])

        graphView=Img(src=scatter2columns(graphData[0],graphData[1],graphData[2],graphData[3],labels), 
                      alt="Scatter", 
                      style="width: 80%; height: 80%;",
                      title=f"Value: {graphData[1]} and {graphData[3]}")+graphView,
        graphData=[]
        
    return page3()

serve()

