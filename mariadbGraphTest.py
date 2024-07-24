#Notes about graphs. I want, as much as possible that the graphs to be as adaptable while being easy to make.

import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints
xTable=input("Enter table for x collumn: ")
yTable=input("Enter table for y collumn: ")
xColumn=input("Enter collumn to select for x: ")
yColumn=input("Enter collumn to select for y: ")

xQuery=cursor.excecute("select " + xColumn + "  from " + xTable)
yQuery=cursor.excecute("select " + yColumn + "  from " + yTable)

x=cursor.execute(xQuery)
y=cursor.execute(yQuery)
print(x)
print(y)
cursor.close()
cnx.close()


#testing scatter graphs  
x = np.array([1,3,2,5,7])
y = np.array([1,2,3,4,5])

plt.scatter(x,y)
plt.show()
