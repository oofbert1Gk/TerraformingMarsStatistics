#Notes about graphs. I want, as much as possible that the graphs to be as adaptable while being easy to make.

import numpy as np
import random 
import matplotlib.pyplot as plt
import mysql.connector
import tabulate
import sys



#opening connection
cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints

def getData(name):

    #getting table name input
    xTable=input("Enter table for " + name +" column: ")
    name=input("Enter column to select from "+ xTable +": ")
    
    #reading data 
    xQuery=cursor.execute("select " + name + "  from " + xTable)
    value=cursor.fetchall()

    for i in range(len(value)):       #looping over the columns and converting them from tuple to int 
        try:
            value[i]=int(value[i][0])
        except ValueError:
            input("collumn must only contain floats")
    return([value,name])

def scatter2columns():
    x=getData("x")
    y=getData("y")

    plt.xlabel("points from " + x[1])  #adding labels 
    plt.ylabel("points from" + y[1])

    #calculating the trendline equation and converting it to right form 
    b=np.polyfit(x[0], y[0], 1)
    p=np.poly1d(b)
    
    #defining graphs 
    plt.scatter(x[0], y[0])
    plt.plot(x[0], p(x[0]), color='red')
    
    plt.show()

def customQueryToTable():

    
    cursor.execute(input("Enter mysql query: "))
    fieldNames=[i[0] for i in cursor.description]
    result=tabulate.tabulate(cursor.fetchall(), headers=fieldNames, tablefmt='psql')
    print(result)


def infoDump2columns():

    x=getData("x")
    y=getData("y")
 
    
    #Making Table
    table=""
    for i in range(len(x[0])):
        
        a=str(x[0][i])+"|"+str(y[0][i])+"\n"
        
        
        for i in range(len(a)):
            a=a+"-"
        
        table=table+"\n"+a
        
    
    print(table)
    
customQueryToTable()
cursor.close()
cnx.close()
