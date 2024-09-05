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
import numpy as np #numerical python
import random 
import matplotlib.pyplot as plt #plotting
import mysql.connector #database
import tabulate #table formatting
import sys #system specific parameters and functions
import subprocess #running shell commands

css = Style(':root { --pico-font-size: 100%; --pico-font-family: Pacifico;}','table tr td {\r\n  border-right: 1px solid blue;\r\n  color: black\r\n}\r\n\r\ntable tr td:last-of-type {\r\n  border: none;\r\n}')
app = FastHTML(hdrs=(picolink, css), static_dir='./static')
client=TestClient(app)

def pageSelect():
    pages = [('Insert', "/"), ("Game Statistics", "/GStats"), ("Card Statistics", "/CStats"), ("Help&Info", "/info")]
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

@app.get("/")
def home():
    return Main(pageSelect(),P("Insert Link:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/", method="post"))

@app.post("/")
def add_message(data:str):
    print("getting data")
    subprocess.run(["bash","getter.sh",data])
    return home()

tableView=()
      
@app.get("/GStats")
def page2():
    return Main(pageSelect(),P("Enter mysql query:"),
                Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/GStats", method="post"),tableView)

@app.post("/GStats")
def add_message(data:str):
    global tableView
    tableView=(Table(data),)+tableView
    return page2()  

serve()

