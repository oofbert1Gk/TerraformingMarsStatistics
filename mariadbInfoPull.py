#Notes about graphs. I want, as much as possible that the graphs to be as adaptable while being easy to make.

import numpy as np
import random 
import matplotlib.pyplot as plt
import mysql.connector
import sys



#opening connection
cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints

def scatter2columns():

#getting input
    #xTable=input("Enter table for x collumn: ")
    #yTable=input("Enter table for y collumn: ")
    #xColumn=input("Enter collumn to select for x: ")
    #yColumn=input("Enter collumn to select for y: ")
    xTable="ScoreByCategory"
    yTable="ScoreByCategory"
    xColumn="greeneries"
    yColumn="cities"

#reading data from mariadb 
    xQuery=cursor.execute("select " + xColumn + "  from " + xTable)
    x=cursor.fetchall()
    yQuery=cursor.execute("select " + yColumn + "  from " + yTable)
    y=cursor.fetchall()


    for i in range(len(x)):       #looping over the columns and converting them from tuple to int 
        try:
            x[i]=int(x[i][0])
            y[i]=int(y[i][0])
        except ValueError:
            input("collumn must only contain floats")
            
        
    plt.xlabel("points from " + xColumn)  #adding labels 
    plt.ylabel("points from" + yColumn)

    #calculating the trendline equation and converting it to right form 
    b=np.polyfit(x, y, 1)
    p=np.poly1d(b)
    
    #defining graphs 
    plt.scatter(x, y)
    plt.plot(x, p(x), color='red')
    
    plt.show()


cursor.close()
cnx.close()
