#this is what I used to set up the mariadb tables 

from __future__ import print_function
import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()
dbUser=os.getenv('DB_USER')
dbPass=os.getenv("DB_PASSWORD")
dbHost=os.getenv('DB_HOST')
dbDatabase=os.getenv('DB_DATABASE')

#connecting to the server
cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbDatabase)
cursor = cnx.cursor()

#defining options table note: they are only temporarily set to varchar so I can make sure that rest actually works the format will be changed later 
tableDescription = (
    "CREATE TABLE `options` ("
    "  id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "  `altVenusBoard` VARCHAR(40) ,"
    "  `aresExtension` VARCHAR(40) ,"
    "  `boardName` VARCHAR(40) ,"
    "  `bannedCards` TEXT ,"
    "  `includedCards` TEXT ,"
    "  `ceoExtension` VARCHAR(40) ,"
    "  `coloniesExtension` VARCHAR(40) ,"
    "  `communityCardsOption` VARCHAR(40) ,"
    "  `corporateEra` VARCHAR(40) ,"
    "  `draftVariant` VARCHAR(40) ,"
    "  `escapeVelocityMode` VARCHAR(40) ,"
    "  `escapeVelocityBonusSeconds` VARCHAR(40) ,"
    "  `fastModeOption` VARCHAR(40) ,"
    "  `includeFanMA` VARCHAR(40) ,"
    "  `includeVenusMA` VARCHAR(40) ,"
    "  `initialDraftVariant` VARCHAR(40) ,"
    "  `moonExpansion` VARCHAR(40) ,"
    "  `pathfindersExpansion` VARCHAR(40) ,"
    "  `preludeDraftVariant` VARCHAR(40) ,"
    "  `preludeExtension` VARCHAR(40) ,"
    "  `prelude2Expansion` VARCHAR(40) ,"
    "  `promoCardsOption` VARCHAR(40) ,"
    "  `politicalAgendasExtension` VARCHAR(40) ,"
    "  `removeNegativeGlobalEvents` VARCHAR(40) ,"
    "  `showOtherPlayersVP` VARCHAR(40) ,"
    "  `showTimers` VARCHAR(40) ,"
    "  `shuffleMapOption` VARCHAR(40) ,"
    "  `solarPhaseOption` VARCHAR(40) ,"
    "  `soloTR` VARCHAR(40) ,"
    "  `randomMA` VARCHAR(40) ,"
    "  `requiresMoonTrackCompletion` VARCHAR(40) ,"
    "  `requiresVenusTrackCompletion` VARCHAR(40) ,"
    "  `turmoilExtension` VARCHAR(40) ,"
    "  `twoCorpsVariant` VARCHAR(40) ,"
    "  `venusNextExtension` VARCHAR(40) ,"
    "  `undoOption` VARCHAR(40) ,"
    "  `underworldExpansion` VARCHAR(40) , "
    "  PRIMARY KEY (id)"
    ") ENGINE=InnoDB")

#defining scorebycategory table 
tableDescription2 = (
    "CREATE TABLE `ScoreByCategory` ("
    "  id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "  `tr` SMALLINT SIGNED,"
    "  `milestones` SMALLINT ,"
    "  `awards` SMALLINT ,"
    "  `greeneries` SMALLINT ,"
    "  `cities` SMALLINT ,"
    "  `ev` SMALLINT SIGNED ," #Escape Velocity
    "  `habitats` SMALLINT ,"
    "  `mines` SMALLINT ,"
    "  `roads` SMALLINT ,"
    "  `pathfinders` SMALLINT ," #Planetary Tracks
    "  `cards` SMALLINT SIGNED,"
    "  `total` SMALLINT SIGNED,"
    "  PRIMARY KEY (id)"
    ") ENGINE=InnoDB")

#defining score by generation table
tableDescription3 = (
    "CREATE TABLE `ScoreByGeneration` ("
    "  id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "  `gen1` SMALLINT, "
    "  `gen2` SMALLINT, "
    "  `gen3` SMALLINT, "
    "  `gen4` SMALLINT, "
    "  `gen5` SMALLINT, "
    "  `gen6` SMALLINT, "
    "  `gen7` SMALLINT, "
    "  `gen8` SMALLINT, "
    "  `gen9` SMALLINT, "
    "  `gen10` SMALLINT, "
    "  `gen11` SMALLINT, "
    "  `gen12` SMALLINT, "
    "  `gen13` SMALLINT, "
    "  `gen14` SMALLINT, "
    "  `gen15` SMALLINT, "
    "  `gen16` SMALLINT, "
    "  `gen17` SMALLINT, "
    "  `gen18` SMALLINT, "
    "  `gen19` SMALLINT, "
    "  `gen20` SMALLINT, "
    "  PRIMARY KEY (id)"
    ") ENGINE=InnoDB")

#Note: All non fan made expansions is 400 cards, average card character length is at most 20 so we need varchar(8000) however there is fan made and accounting for extra expansions etc... Therefore to be safe I will store it as text which has a limit of ~2^16(65536) versus varchar which cna go up to 16383(~2^14) 

tableDescription4 = (
    "CREATE TABLE `CardsPlayed` ("
    "  id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "  `cards` TEXT,"
    "  PRIMARY KEY (id)"
    ") ENGINE=InnoDB")

tableDescription5 = (
    "CREATE TABLE `metaData` ("
    " id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    " `rawData` MEDIUMTEXT,"
    " `playerName` VARCHAR(100),"
    " `won` TINYINT,"
    " `solo` TINYINT,"
    " `generation` SMALLINT,"
    " `insertTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , "
    "  `gameNumber` SMALLINT, "
    " PRIMARY KEY (id) "
    ") ENGINE=InnoDB")
    
#executing the commands and then closing the connection 
cursor.execute(tableDescription)
cursor.execute(tableDescription2)
cursor.execute(tableDescription3)
cursor.execute(tableDescription4)
cursor.execute(tableDescription5)

cursor.close()
cnx.close()
