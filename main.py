#TODO:
#-Seperate page for each connection

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
import pandas as pd #for the table to image function
import uuid #for individual sessions for each connection

css = Style('html, body {background-image: url(/static/800px-VallesMarinerisHuge.jpg); background-size: 100% auto; background-position: center top; background-repeat: repeat-y; height: 100%; margin: 0; padding: 0;}',
            '''
            .table-container {
                width: 100%;
                overflow-x: auto;
                padding: 20px;
                box-sizing: border-box;
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
            .footer {
                font-size: 0.75em;
                position: fixed;
                bottom: 10px;
                white-space: nowrap;
                width: 100%;
                color: white;
                padding: 5px 10px;
                border-radius: 10px;
                text-align: center;
            }
            ''')
app = FastHTML(hdrs=(picolink,css), static_dir='./static')
app.mount("/static", StaticFiles(directory="static"), name="static")
client=TestClient(app)

def getOrCreateSessionId(request: Request):
    if 'session_id' in request.query_params:
        return request.query_params['session_id']
    elif 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())
    return request.session['session_id']

def backgroundImageAttribution():
 return(Div(P("Background Image: Valles Marineris huge by NASA / JPL-Caltech / USGS from https://photojournal.jpl.nasa.gov/catalog/PIA00422", cls="footer")))

def pageSelect(session_id):

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
        border-radius: 10px !important;
    }
    .navbar a:hover {
        background-color: #3aa69f;
        color: #333333 !important;
    }
    
    """

    n = Div(
        A('Insert', href=f"/?session_id={session_id}"),
        A("Game Statistics Tables", href=f"/GStatsT?session_id={session_id}"),
        A("Game Statistics Graphs", href=f"/GStatsG?session_id={session_id}"),  
        A("Help & Info", href=f"/info?session_id={session_id}"),
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

def scatter2columns(xData, yData,labels):
    print(xData,yData,labels)
    
    #creating figure
    plt.figure(figsize=(8,8))

    #x and y labels
    plt.xlabel(labels[0]) 
    plt.ylabel(labels[1])


    #calculating the trendline equation and converting it to right form 
    b=np.polyfit(xData, yData, 1)
    p=np.poly1d(b)
    
    #defining graphs 
    plt.scatter(xData, yData)

    #defining limits
    lim=max(max(xData),max(yData))+10
    m=min([min(xData),min(yData)])
    if m>(-10):
        plt.xlim(-10,lim)
        plt.ylim(-10,lim)
    else:
        plt.xlim(m,lim)
        plt.ylim(m,lim)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    # extending trendline indefinitely 
    xMin, xMax = plt.xlim()
    xExtended= np.linspace(xMin,xMax,10000)
    plt.plot(xExtended, p(xExtended), color='red') #trendline

    #modifying axis(and adding axis lines)
    plt.axhline(0,color='black') 
    plt.axvline(0,color='black') 
    
    plt.tight_layout()

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
async def home(request: Request):
    sessionId=getOrCreateSessionId(request)
    return Main(
        pageSelect(sessionId),
        Form(Div(
                Div(Input(type="text", name="data",placeholder="Enter game link:", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15 15px; border-radius: 10px;"),
                    style="display: flex; align-items: middle;"),
            ),
            action="/Insert",
            method="post"
        ),
        Table("select id, playerName, won, generation, insertTime from metaData"),
        backgroundImageAttribution()
    )

@app.post("/Insert")
def addTable(data:str, request: Request):
    subprocess.run(["bash","getter.sh",data], cwd="./static")
    subprocess.run(["python3.12","filter.py"], cwd="./static")

    sessionId=getOrCreateSessionId(request)
    return RedirectResponse(url=f"/?session_id={sessionId}", status_code=303)
      
@app.get("/GStatsT")
async def page2(request: Request):
    sessionId=getOrCreateSessionId(request)

    #defining input types
    types=[("Show Table","/Table"),("Download as CSV","/DownloadCSV"),("Download as PNG","/DownloadIMG")]

    currentTables=Div(*tableViews.get(sessionId,[]))

    return Main(pageSelect(sessionId),P(style="font-size: 2em; color: #8fffdf"),
                Form(
                    
                    Input(type="text", placeholder="Enter Mysql Query", name="data", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Select(
                        *[Option(label, value=query) for label, query in types],
                        name="action",
                        style="flex-grow: 1; margin-right: 10px; height: 52px; max-width: 200px; padding: 15px 15px;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15px 15px; border-radius: 10px;"),
                    style="display: flex; align-items: stretch;",
                    
                    action="/HandleAction", method="post"),
                    currentTables,
                    backgroundImageAttribution())

graphsQuestions=["Table for X","Column for X","Table for Y","Column for Y"]
tableViews={}
graphData={}
graphView={}

@app.get("/GStatsG")
async def page3(request: Request):
    sessionId=getOrCreateSessionId(request)
    types=[("Show Graph", "0"),("Download Graph","2")]

    if sessionId not in graphData:
        graphData[sessionId]=[]
    if sessionId not in graphView:
        graphView[sessionId]=()
        
    return Main(pageSelect(sessionId),P(style="font-size: 1.2em;"),
                Form(
                    Input(type="text", name="data", placeholder=f"Enter {graphsQuestions[len(graphData[sessionId])]}:", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Select(
                        *[Option(label, value=query) for label, query in types],
                        name="action",
                        style="flex-grow: 1; margin-right: 10px; height: 52px; max-width: 175px; padding: 15px 15px;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15 15px; border-radius: 10px;"),
                    style="display: flex; align-items: stretch;",
                    action="/Graph", method="post"),
                    graphView[sessionId],
                    backgroundImageAttribution())

@app.post("/HandleAction")
async def handleAction(action:str, data:str, request: Request):
    if action=="/Table":
        return await printTable(data, request)
    elif action=="/DownloadCSV":
        return downloadCSV(data)
    elif action=="/DownloadIMG":
        return downloadIMG(data)
    else:
        return await page2(request) #in case of error

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
async def printTable(data:str, request: Request):
    sessionId=getOrCreateSessionId(request)
    if sessionId not in tableViews:
        tableViews[sessionId]=[]
    tableViews[sessionId].insert(0, Table(data))
    return await page2(request)  

@app.post("/Graph")
async def processGraphData(action:str, data:str, request: Request):
    sessionId=getOrCreateSessionId(request)
    
    if sessionId not in graphData:
        graphData[sessionId]=[]
    if sessionId not in graphView:
        graphView[sessionId]=()

    graphData[sessionId].append(data)
    if len(graphData[sessionId])==4:
        labels=[graphData[sessionId][1],graphData[sessionId][3]]
        xData=dataFetch(graphData[sessionId][0],graphData[sessionId][1])
        yData=dataFetch(graphData[sessionId][2],graphData[sessionId][3])
        print(graphView[sessionId])
        graphView[sessionId]=Img(
            src=scatter2columns(xData,yData,labels), 
            alt="Scatter", 
            style="width: 100%; max-height: 80vh; object-fit: contain;",
            title=f"Value: {graphData[sessionId][1]} and {graphData[sessionId][3]}"
            )+graphView[sessionId]
        graphData[sessionId]=[]
        
    return await page3(request)

serve()

