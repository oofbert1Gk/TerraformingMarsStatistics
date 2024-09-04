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
import numpy as np
import random       
import matplotlib.pyplot as plt
import mysql.connector
import tabulate
import sys

css = Style(':root { --pico-font-size: 100%; --pico-font-family: Pacifico;}','table tr td {\r\n  border-right: 1px solid blue;\r\n  color: black\r\n}\r\n\r\ntable tr td:last-of-type {\r\n  border: none;\r\n}')
app = FastHTML(hdrs=(picolink, css))
client=TestClient(app)

display=()

#opening connection
cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints

def Table(cmd):
    cnx = mysql.connector.connect(user='pythonRead', password='Ehaid4Zah5vootheeCh3euh1thie4A',host='127.0.0.1',database='tfm')
    cursor = cnx.cursor()

    cursor.execute(cmd)
    fieldNames=[i[0] for i in cursor.description]
    result=cursor.fetchall()

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
    
    return(display)

serve()
    

