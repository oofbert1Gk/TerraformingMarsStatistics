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
import numpy as np #numerical python
import random 
import matplotlib.pyplot as plt #plotting
import mysql.connector #database
import tabulate #table formatting
import sys #system specific parameters and functions
import subprocess #running shell commands

css = Style(':root { --pico-font-size: 100%; --pico-font-family: Pacifico;}','table tr td {\r\n  border-right: 1px solid blue;\r\n  color: black\r\n}\r\n\r\ntable tr td:last-of-type {\r\n  border: none;\r\n}')
app = FastHTML(hdrs=(picolink, css))
client=TestClient(app)

subprocess.run(["bash","getter.sh",""])

@app.get("/")
def home():
    return [
        Form([
            Label("Link:"),
            Input(type="text", name="user_input", placeholder="Type here..."),
            Button("Submit", type="submit")
        ], action="/", method="post")
    ]

serve()