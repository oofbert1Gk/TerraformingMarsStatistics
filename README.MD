A terraforming mars herokuapp scorescraper and data storage system using mariadb.

Instructions for Building Yourself:

Note: These instructions are experimental and they are for linux debian 11, they might not work if you are on a another system and they are not very detailed and may have omissions 

1. Install Dependencies

python version >= 3.10 
python packages:
       python-fasthtml
       numpy
       matplotlib
       pandas
       dotenv
       urllib
       
mariadb (probably any version that isn't horribly outdated)

2. Set up mariadb

You need to create a database called tfm 
You will need two users(search if you don't know how to): one for inserting which needs permissions to create tables, edit tables and read tables, these need access to tfm 

you will need to create a .env file which contains the details for the read only in the main folder and a .env which contains the information for the writer in the static directory, it needs to be in the following formatfr:
DB_USER=Insert UserName
DB_PASSWORD=Insert Password
DB_HOST=127.0.0.1
DB_DATABASE=tfm

to do this simply open .env in a text editor of your choice and add in the information.
To create the tables run tablemaker.py

3. Start website

At this point all the setup is done, to start the website simply run main.py and then go to http://0.0.0.0:5001/