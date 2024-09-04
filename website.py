#TODO:
#-Add attribution for mars image

#importing all potential dependices for fasthtml
from IPython import display
from enum import Enum
from pprint import pprint
from fasthtml.common import *
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

css = Style(':root { --pico-font-size: 100%; --pico-font-family: Pacifico;}')
app = FastHTML(hdrs=(picolink, css))
client=TestClient(app)

def table():
    table=Table(Tr(Th('Company'),Th('Contact'),Th('Country')),Tr(Td('Alfreds Futterkiste'),Td('Maria Anders'),Td('Germany')),Tr(Td('Centro comercial Moctezuma'),Td('Francisco Chang'),Td('Mexico')))
    return(table)


def pageSelect():
    pages = [('Insert', "/insert"), ("Game Statistics", "/GStats"), ("Card Statistics", "/CStats"), ("Help&Info", "/info")]
    return Container(Navbar('nav', 'selidx', items=pages, cls='navbar-light bg-secondary rounded-lg',
                            image=Img(src='/assets/logo.jpg'), hdr_href="http://0.0.0.0:5001/",
                            placement=PlacementT.Default, expand=SizeT.Md, toggle_left=False))  

def Sections(h2s, texts):
    colors = 'yellow', 'pink', 'teal', 'blue'
    div_cls = 'py-2 px-3 mt-4 bg-light-{} rounded-tl-lg'
    return chain([Div(H2(h2, id=f'sec{i+1}', cls=div_cls.format(colors[i%4])), Div(txt, cls='px-2'))
                  for i,(h2,txt) in enumerate(zip(h2s, texts))])

@app.get("/")
def home():
    return(pageSelect())


    
@app.get("/insert")
def page1():
    return H1("Insert",table())

@app.get("/GStats")
def page1():
    return H1("Game Statistics")

@app.get("/CStats")
def page1():
    return H1("Cards Statistics")

@app.get("/info")
def page1():
    return H1("Help&Information")

serve()
