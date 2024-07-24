#this is what I used to set up the mariadb tables 

from __future__ import print_function

import mysql.connector

#connecting to the server
cnx = mysql.connector.connect(user='python', password='pythonPassword',
                              host='127.0.0.1',
                              database='testF')
cursor = cnx.cursor()

#defining options table note: they are only temporarily set to varchar so I can make sure that rest actually works the format will be changed later 
tableDescription = (
    "CREATE TABLE `options` ("
    "  id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "  `altVenusBoard` VARCHAR(40) ,"
    "  `aresExtension` VARCHAR(40) ,"
    "  `boardName` VARCHAR(40) ,"
    "  `bannedCards` VARCHAR(40) ,"
    "  `includedCards` VARCHAR(40) ,"
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
    "  `insertTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , "
    "  `gameNumber` SMALLINT, "
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
    "  `gameNumber` SMALLINT, "
    "  `insertTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , "
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
    "  `insertTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , "
    "  `gameNumber` SMALLINT, "
    "  PRIMARY KEY (id)"
    ") ENGINE=InnoDB")

#executing the commands and then closing the connection 
cursor.execute(tableDescription)
cursor.execute(tableDescription2)
cursor.execute(tableDescription3)
cursor.close()
cnx.close()
