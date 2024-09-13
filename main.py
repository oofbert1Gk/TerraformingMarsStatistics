#TODO:
#-Add attribution for mars image

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
import base64

css = Style(':root { --pico-font-size: 100%; --pico-font-family: Pacifico;}','table tr td {\r\n  border-right: 1px solid blue;\r\n  color: black\r\n}\r\n\r\ntable tr td:last-of-type {\r\n  border: none;\r\n}')
app = FastHTML(hdrs=(picolink, css), static_dir='./static')
client=TestClient(app)

def pageSelect():
    pages = [('Insert', "/"), ("Game Statistics Tables", "/GStatsT"), ("Card Statistics", "/CStats"), ("Help&Info", "/info"), ("Game Statistics Graphs", "/GStatsG")]
    return Container(Navbar('nav', 'selidx', items=pages, cls='navbar-light bg-secondary rounded-lg',
                            image='logo.svg', hdr_href="http://0.0.0.0:5001/",
                            placement=PlacementT.Default, expand=SizeT.Md, toggle_left=False))  

def Table(cmd):
    #opening connection
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()
    
    #getting information from the database
    cursor.execute(cmd)
    fieldNames=[i[0] for i in cursor.description]
    result=cursor.fetchall()

    #defining table 
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

    cursor.close()
    cnx.close()
    #table=Table(table)
    return(TB(table))

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
        
    lim=max(max(xData),max(yData))
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
    return Main(pageSelect(),P("Insert Link:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/Insert", method="post"))

@app.post("/Insert")
def add_message(data:str):
    print("getting data")
    subprocess.run(["bash","getter.sh",data])
    return home()

tableView=()
      
@app.get("/GStatsT")
def page2():
    return Main(pageSelect(),P("Enter mysql query:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/Table", method="post"),
                     tableView)

@app.post("/Table")
def add_message(data:str):
    global tableView
    tableView=(Table(data),)+tableView
    return page2()  

graphsQuestions=["Table for X","Column for X","Table for Y","Column for Y"]
graphData=[]
graphView=()

@app.get("/GStatsG")
def page3():
    return Main(pageSelect(),P("Enter "+graphsQuestions[len(graphData)]+":"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/Graph", method="post"),
                     graphView)

@app.post("/Graph")
def processGraphData(data:str):
    global graphData
    global graphView
    graphData.append(data)
    if len(graphData)==4:
        labels=[graphData[1],graphData[3]]
        graphData[1]=dataFetch(graphData[0],graphData[1])
        graphData[3]=dataFetch(graphData[2],graphData[3])

        graphView=Img(src=scatter2columns(graphData[0],graphData[1],graphData[2],graphData[3],labels), alt="Scatter")+graphView,
        graphData=[]
        
    return page3()

serve()

