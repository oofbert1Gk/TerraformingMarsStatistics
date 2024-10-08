#fasthtml
from fasthtml.common import *
from fasthtml.common import Table as TB 
from fastcore.test import *

from starlette.responses import RedirectResponse #redirects
from fastapi.staticfiles import StaticFiles #static files
from urllib.parse import urlparse #url parsing
from fastapi import Request #requests
from fh_bootstrap import * #for bootstrap for ft 

#importing all dependecies for the back end
import numpy as np #matplotlib requirement
import matplotlib.pyplot as plt #graphs and tables
import mysql.connector #database acess
import subprocess #running scripts
import io #this and below are for tpye conversion
import base64
import csv #writing csv file 
import pandas as pd #for the table to image function
import uuid #for individual sessions for each connection
from dotenv import load_dotenv #secure variables

load_dotenv()

dbUser = os.getenv('DB_USER')
dbPass = os.getenv('DB_PASSWORD')
dbHost= os.getenv('DB_HOST')
dbDatabase = os.getenv('DB_DATABASE')

css = Style('html, body {background-image: url(/static/800px-VallesMarinerisHuge.jpg); background-size: cover; background-position: center top; background-repeat: repeat-y; height: 100%; margin: 0; padding: 0;}',
            '''
            .table-container {
                width: 100%;
                overflow-x: auto;
                padding: 20px 100px 0px 100px;
                box-sizing: border-box;
                
            }
            table {
                table-layout: auto;
                width: auto !important;
                height: auto !important;
                min-width: 100%;
                
                
            }
            table tr td {
                color: white;
                white-space: nowrap;
                padding: 5px;
                width: 1px !important;
                text-shadow: 1px white;
                background-color: #fb913dce;

            }

            body {
                color: white;
                text-shadow: 1px 1px 1px black;
            }
            .footer {
                font-size: 0.75em;
                position: fixed;
                bottom: -5px;
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


def handleError(request: Request, e: str):
    sessionId = getOrCreateSessionId(request)
    referer = request.headers.get('referer')
    if not referer:
        referer = "/"
    
    path=urlparse(referer).path
    redirectUrl=f"{path}?session_id={sessionId}&error={e}"
    return RedirectResponse(redirectUrl, status_code=303)

def getOrCreateSessionId(request: Request):
    if 'session_id' in request.query_params:
        return request.query_params['session_id']
    elif 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())
    return request.session['session_id']

def backgroundImageAttribution():
 return(Div(P("Background Image: cropped from Valles Marineris huge by NASA / JPL-Caltech / USGS from https://photojournal.jpl.nasa.gov/catalog/PIA00422", cls="footer")))

def pageSelect(session_id, classes):

    navbar_css = """
    .navbar {

        overflow: hidden;
        display: flex;
        justify-content: flex-start !important;
        align-items: left;
        margin-right: 5%;
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

    .navbar a.on {
        background-color: #E7D27C;
        color: #000000;
    }

    .navbar a:hover {
        background-color: #3aa69f;
        color: #333333 !important;
    }
    
    """

    n = Div(
        P("Terraforming Mars Game Scraper", style="font-family: 'Pacifico',cursive; text-align: center; color: white; font-size: 3em; margin: auto; margin-left: 2.5% !important;"),
        A('Insert', href=f"/?session_id={session_id}", cls=classes[0]),
        A("Game Statistics Tables", href=f"/GStatsT?session_id={session_id}", cls=classes[1]),
        A("Game Statistics Graphs", href=f"/GStatsG?session_id={session_id}", cls=classes[2]),  
        A("Help & Info", href="/info", cls=classes[3]),
        cls="navbar"
    )

    return (Head(Title("FastHTML Navbar"),Style(navbar_css)),Body(n))

def htmlTableToCSV(hTable):
    r=pd.read_html(hTable)[0]
    csv=r.to_csv(index=False)
    return csv

def Table(cmd):
    #opening connection
    cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbDatabase)
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
    
    #opening connection
    cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbDatabase)
    cursor = cnx.cursor()

    #getting data from the database
    cursor.execute("select " + column + "  from " + table)
    value=cursor.fetchall()

    #closing connection 
    cursor.close()
    cnx.close()
    return(value)


@app.get("/")
async def home(request: Request):
    sessionId=getOrCreateSessionId(request)
    errorMessage = request.query_params.get('error')
    return Main(
        #heading is currently commented out, it didn't right but I left it here for reference and because it may be implemnted later 
        #H1("Insert", style="color: white; font-size: 4em; display: flex; text-shadow: 2px 2px ;justify-content: center; align-items: center; height: 100px; width: 100%;"),
        pageSelect(sessionId,["on","","",""]),
        P(errorMessage, style="color: red;") if errorMessage else None,
 
        Form(Div(
                Div(Input(type="text", name="data",placeholder="Enter game link:", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15 15px; border-radius: 10px;"),
                    style="display: flex; align-items: middle; justify-content: center;"),
            ),
            style="padding: 20px 20px 0px 20px;",
            action="/Insert",
            method="post"
        ),
        H3("Recent Games", style="color: white; padding: 0px 0px 0px 100px; font-size: 2em;"),
        Table("SELECT id, playerName, won, generation, insertTime FROM metaData ORDER BY id desc LIMIT 10"),
        backgroundImageAttribution()
    )

@app.post("/Insert")
def addTable(data:str, request: Request):
    try:
        subprocess.run(["bash","getter.sh",data], cwd="./static")
        subprocess.run(["python3.12","filter.py"], cwd="./static")
    except subprocess.CalledProcessError as e:
        return handleError(request, f"Error in subprocess: {e}")
    
    sessionId=getOrCreateSessionId(request)
    return RedirectResponse(url=f"/?session_id={sessionId}", status_code=303)
      
@app.get("/GStatsT")
async def page2(request: Request):
    sessionId=getOrCreateSessionId(request)
    errorMessage = request.query_params.get('error')

    #defining input types
    types=[("Show Table","/Table"),("Download as CSV","/DownloadCSV"),("Download as PNG","/DownloadIMG")]

    currentTables=Div(*tableViews.get(sessionId,[]))

    return Main(pageSelect(sessionId,["","on","",""]),
                P(style="font-size: 2em; color: #8fffdf"),
                P(errorMessage, style="color: red;") if errorMessage else None,
                P(style="font-size: 2em; color: #8fffdf"),
                Form(
                    
                    Input(type="text", placeholder="Enter Mysql Query", name="data", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Select(
                        *[Option(label, value=query) for label, query in types],
                        name="action",
                        style="flex-grow: 1; margin-right: 10px; height: 52px; max-width: 200px; padding: 15px 15px;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15px 15px; border-radius: 10px;"),
                    style="display: flex; align-items: stretch; justify-content: center; padding: 20px;",
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
    errorMessage = request.query_params.get('error')

    if sessionId not in graphData:
        graphData[sessionId]=[]
    if sessionId not in graphView:
        graphView[sessionId]=()
        
    return Main(pageSelect(sessionId, ["","","on",""]),
                P(style="font-size: 1.2em;"),
                P(errorMessage, style="color: red;") if errorMessage else None,
                P(style="font-size: 1.2em;"),
                Form(
                    Input(type="text", name="data", placeholder=f"Enter {graphsQuestions[len(graphData[sessionId])]}:", style="flex-grow: 1; margin-right: 10px; max-width: 50%;"),
                    Button("Submit", style="height: 52px; width: 200px; padding: 15 15px; border-radius: 10px;"),
                    style="display: flex; align-items: stretch; justify-content: center; padding: 20px;",
                    action="/Graph", 
                    method="post"),
                    graphView[sessionId],
                    backgroundImageAttribution())
paragraphs=[]
paragraphs.append(("This is a project made for scraping data off your herokuapp terraforming mars games and then analyses the data, it takes a link to the endgame situation and extracts the data and input it into a mariadb database, the graphical interface contains this, mysql queries to the database as well as a scatter graph between two columns in the database. All the code for the website can be found in the github page,",A('https://github.com/oofbert1Gk/TerraformingMarsStatistics/'),". This is also where to report bugs or make suggestions."))
paragraphs.append(("For a perfect representation of the database structure see", A('https://github.com/oofbert1Gk/TerraformingMarsStatistics/blob/main/tablemaker.py'), "which defines it. To find all columns which a table has input into Game Statistics Tables: select * from insert_table_name limit 0 . There are 5 tables:"))
paragraphs.append("options : this has a column for each setting")
paragraphs.append("ScoreByCategory : this specifies how much score one has for each category ")
paragraphs.append("ScoreByGeneration : This has a column for twenty generations(yes, if your game is longer than 20 generations it will cut cause bugs), they are simply named gen{number}, for example gen1 or gen2")
paragraphs.append("CardsPlayed : this only contains one list, 'cards' which contains every single card played by the player")
paragraphs.append("metaData : This table contains metadata and some other things, some of it's columns are displayed on the homepage, the columns are rawData,playerName,won,solo,generation,insertTime,gameNumber It is important that you will never want to select raw data because it is very big and so may cause problem when displaying.")
paragraphs.append("Insert: Paste in a link to a finsiehd tfm game then press enter or press the submit button")
paragraphs.append("Type a mysql query, then select the output format(show, download data, download image) then press enter or submit. The basic mysql select structure is 'select {columns} from {table}'. For example:")
paragraphs.append("select gen1 from ScoreByGeneration (selects the generation one column from the ScoreByGeneration Table)")
paragraphs.append("select gen1, gen2, gen4 from scoreByGeneration (selects the generation 1,2 and 4 columns from the ScoreByGeneration table)")
paragraphs.append("select * from ScoreByCategory (selects all columns from the ScoreByCategory Table)")
paragraphs.append("If you don't understand this or you want more complex queries then there is a number of great mysql select tutorials online")
paragraphs.append("Choose a table and from that table a column that will be the x axis data then choose a table and then a column that will be the y axis data. This is for seeing the relationship between two columns. For example:")
paragraphs.append((Li("Input1: ScoreByGeneration"),Li("Input2: cities"),Li("Input3: ScoreByGeneration"),Li("Input4: greeneries")))
paragraphs.append("This will produce a scatter plot with the points from cities on the x axis and the points from greeneries on the y axis. The two tables do not have to be the same table and this will remove all elements that aren't floats and if either x or y data is empty then it will return an error that looks something like this:")
paragraphs.append("Error in processGraphData: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (19,) inhomogeneous part.")
paragraphs.append("This means that you have entered columns for which there is either no data, or no data that is a float. ")

@app.get("/info")
async def helpAndInfo(request: Request):
    sessionId=getOrCreateSessionId(request)
    return (
        pageSelect(sessionId, ["","","","on"]),
        P("", style="height: 2vh"), #this text is here to add padding which wasn't working because of margin: auto
        Div(
            H2("Overview"),
            P(paragraphs[0]),
            H2("Usage"),
            H4("Insert"),
            P(paragraphs[8]),
            H4("Game Statistics Tables"),
            P(paragraphs[9]),
            Ul(*[Li(text) for text in paragraphs[9:12]]),
            P(paragraphs[12]),
            H4("Game Statistics Graphs"),
            P(paragraphs[13]),
            Ul(paragraphs[14]),
            P(paragraphs[15]),
            Ul(paragraphs[16]),
            P(paragraphs[17]),
            H2("List of Tables"),
            P(paragraphs[1]),
            Ul(*[Li(text) for text in paragraphs[2:7]]),
            style="margin: auto; background-color: white; !important; text-shadow: 0px white !important; padding: 20px; width: 75vw; border-radius: 20px;"
            ),
        backgroundImageAttribution()
        ),
        


@app.post("/HandleAction")
async def handleAction(action:str, data:str, request: Request):
    try:    
        if action=="/Table":
            return await printTable(data, request)
        elif action=="/DownloadCSV":
            return downloadCSV(data)
        elif action=="/DownloadIMG":
            return downloadIMG(data)
        else:
            return await page2(request) #in case of error
    except Exception as e:
        return handleError(request, f"Error in handleAction: {e}")

@app.post("/DownloadIMG")
def downloadIMG(data:str):
    #downloading the table as an image requires a webdriver, which I don't want to add to the project and so I am using matplotlib to make a table and then convert that to png 
    
    #opening connection
    cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbDatabase)
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
    cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbDatabase)
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
    return RedirectResponse(url=f"/GStatsT?session_id={sessionId}", status_code=303)

@app.post("/Graph")
def processGraphData(data:str, request: Request):
    
    try:
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
        
            for d in xData:
                try:
                    float(d[0])
                except TypeError:
                    xData=[i for i in xData if i !=d]

            for e in yData:
                try:
                    float(e[0])
                except TypeError:
                    yData=[i for i in yData if i !=e]

            for i in range(len(yData)):
                yData[i]=float(yData[i][0])
                xData[i]=float(xData[i][0])

            graphView[sessionId]=Img(
                src=scatter2columns(xData,yData,labels), 
                alt="Scatter", 
                style="width: 100%; max-height: 80vh; object-fit: contain;",
                title=f"Value: {graphData[sessionId][1]} and {graphData[sessionId][3]}"
                )+graphView[sessionId]
            graphData[sessionId]=[]
        return RedirectResponse(url=f"/GStatsG?session_id={sessionId}", status_code=303)
    except Exception as e:
        graphData[sessionId]=[]
        return handleError(request, f"Error in processGraphData: {e}")

serve()

