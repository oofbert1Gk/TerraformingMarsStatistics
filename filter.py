from __future__ import print_function
import mysql.connector

import re 

reads = open("formattedData","r")
h = reads.read()

#Input is the string and the location (a list with two num elements beginning and end) this is to remove all the spaces newlines etc... that are in the raw data file

def stripSplit(string,location):
    s=(h[location[0]:location[1]]).replace(" ","").replace("\n","").replace('"',"").split(",")
    return(s)

#testing


#Getting options

l=[h.index('"gameOptions": {')+23,h.index('"underworldExpansion": false')+28]
options=stripSplit(h,l)

#formatting options 

for i in range(len(options)):
    begin=options[i].index(":")+1
    end=len(options[i])
    options[i]=options[i][begin:end]

    

#getting score by generation
l=[h.index("victoryPointsByGeneration")+30,h.index("corruption")-13]
ScoreByGeneration=stripSplit(h,l)

#Getting Generation

#note: If the generation number is larger than 10^64 will be read wrong and will everything else shaved off, however if you have played that many generations you have a much bigger problem 
f=h.index('"generation":')+13
generation=re.sub( '[^0-9]','',(h[f:f+64]))


#Getting Score by Category
#note category is in this order: TR, milestones, awards, greeneries, cities, EV, Moonhabs, Moonmines, moonroads, planetary track, VP, total

begin=h.index('"victoryPointsBreakdown"')
end=h.index('"detailsCards": [')
ScoreByCategory=re.sub( '[^0-9,,]','',(h[begin:end])).split(',')
del(ScoreByCategory[12])

#Getting all cards played

begin=h.index('tableau')
end=h.index('"selfReplicatingRobotsCards": [],')

x=h[begin:end]
x=x.replace(" ",'').replace("{",'').replace(",",'').replace('"','')
x=x.split("\n")

cardsPlayed=[]

for i in range(len(x)):
    if "name" in x[i]:
        a=x[i].replace("name:","")
        cardsPlayed.append(a)
print(cardsPlayed)














#logging in to the mariadb database, this is not the permanent account I will be logging in with, if I actually host this then I will change this 
cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')

cursor = cnx.cursor(buffered=True)

#defining the query command 
query = ("SELECT gameNumber FROM ScoreByCategory ORDER BY id desc LIMIT 1")

#excecuting the query 
cursor.execute(query)

#getting the results and formatting them(we only want the number)
b=str(cursor.fetchone())

try:
    result=int(re.sub( '[^0-9]','',(b)))
except:
    r=0
else:
    r=int(re.sub( '[^0-9]','',(b)))+1


    
options.append(str(r))
ScoreByCategory.append(str(r))

cursor.close()
cursor = cnx.cursor()

#defining the mariad statement, this looks very messy but I wanted to have a collumn for each setting
#note: I have defined the mariadb table for score by generation to only have a length of 20 therefore if for some reason it is longer than 20 generations the script will not work (metanote: real games will never take 20 generations)

insert1 = ("INSERT INTO options "
               "(altVenusBoard, aresExtension, boardName, bannedCards, includedCards, ceoExtension, coloniesExtension, communityCardsOption, corporateEra, draftVariant, escapeVelocityMode, escapeVelocityBonusSeconds, fastModeOption, includeFanMA, includeVenusMA, initialDraftVariant, moonExpansion, pathfindersExpansion, preludeDraftVariant, preludeExtension, prelude2Expansion, promoCardsOption, politicalAgendasExtension, removeNegativeGlobalEvents, showOtherPlayersVP, showTimers, shuffleMapOption, solarPhaseOption, soloTR, randomMA, requiresMoonTrackCompletion, requiresVenusTrackCompletion, turmoilExtension, twoCorpsVariant, venusNextExtension, undoOption, underworldExpansion, gameNumber)"
               "VALUES ('" + options[0]+"','"+options[1]+"','"+options[2]+"','"+options[3]+"','"+options[4]+"','"+options[5]+"','"+options[6]+"','"+options[7]+"','"+options[8]+"','"+options[9]+"','"+options[10]+"','"+options[11]+"','"+options[12]+"','"+options[13]+"','"+options[14]+"','"+options[15]+"','"+options[16]+"','"+options[17]+"','"+options[18]+"','"+options[19]+"','"+options[20]+"','"+options[21]+"','"+options[22]+"','"+options[23]+"','"+options[24]+"','"+options[25]+"','"+options[26]+"','"+options[27]+"','"+options[28]+"','"+options[29]+"','"+options[30]+"','"+options[31]+"','"+options[32]+"','"+options[33]+"','"+options[34]+"','"+options[35]+"','"+options[36]+"','"+options[37]+"')")

insert2 = ("INSERT INTO ScoreByCategory "
               "(tr,milestones,awards,greeneries,cities,ev,habitats,mines,roads,pathfinders,cards,total, gameNumber)"
               "VALUES (" + ScoreByCategory[0]+","+ScoreByCategory[1]+","+ScoreByCategory[2]+","+ScoreByCategory[3]+","+ScoreByCategory[4]+","+ScoreByCategory[5]+","+ScoreByCategory[6]+","+ScoreByCategory[7]+","+ScoreByCategory[8]+","+ScoreByCategory[9]+","+ScoreByCategory[10]+","+ScoreByCategory[11]+","+ScoreByCategory[12]+")")

columns=""
for i in range(len(ScoreByGeneration)):
    columns=columns+("gen" + str(i+1)+",")
columns=columns+"gameNumber"

values=""
for i in range(len(ScoreByGeneration)):
    values=values+(ScoreByGeneration[i]+",")
values=values+str(r)

insert3 = ("INSERT INTO ScoreByGeneration"
        "("+columns+")"
        "VALUES ("+values+")")


#Excecuting the command, commiting it to the dataubase and then closing the connection 

cursor.execute(insert1)
cursor.execute(insert2)
cursor.execute(insert3)

cnx.commit()

cursor.close()
cnx.close()
                


