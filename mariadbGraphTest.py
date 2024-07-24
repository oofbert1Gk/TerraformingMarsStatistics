#Notes about graphs. I want, as much as possible that the graphs to be as adaptable while being easy to make.

import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints

#xTable=input("Enter table for x collumn: ")
#yTable=input("Enter table for y collumn: ")
#xColumn=input("Enter collumn to select for x: ")
#yColumn=input("Enter collumn to select for y: ")
xTable="ScoreByCategory"
yTable="ScoreByCategory"
xColumn="greeneries"
yColumn="cities"

xQuery=cursor.execute("select " + xColumn + "  from " + xTable)
x=cursor.fetchall()
yQuery=cursor.execute("select " + yColumn + "  from " + yTable)
y=cursor.fetchall()

for i in range(len(x)):
    x[i]=int(x[i][0])
    y[i]=int(y[i][0])

plt.scatter(x,y)
plt.show()



cursor.close()
cnx.close()

#testing scatter graphs  

