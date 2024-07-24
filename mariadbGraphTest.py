#Notes about graphs. I want, as much as possible that the graphs to be as adaptable while being easy to make.

import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#Creating scatter plot which compares two columns, this will only work if both of the collumns only contain ints
tablex=input("Enter table for x collumn: ")
tabley=input("Enter table for y collumn: ")
x=input("Enter collumn to select for x:")
y=input("Enter collumn to select for y:")


cursor.close()
cnx.close()


#testing scatter graphs  
x = np.array([1,3,2,5,7])
y = np.array([1,2,3,4,5])

plt.scatter(x,y)
plt.show()
