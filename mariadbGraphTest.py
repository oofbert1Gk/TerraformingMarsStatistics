import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')

cursor = cnx.cursor()

cursor.excecute("")

