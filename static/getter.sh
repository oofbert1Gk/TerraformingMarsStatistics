#Note: currently written in bash I will probably later convert this to another language.
#what it does is it gets input for the url(this currently potentially very insecure as this could download from any site) then use wget to get the two data files from there (the game info and the logs) because the page is written in json we use less to output it and then jq to format it into a more human readable form which we then output into files 
url=$1
wget -O testData "${url/the-end/"api/player"}"
wget -O logs "${url/the-end/"api/game/logs"}"
less testData | jq > formattedData
less logs | jq > formattedLogs
