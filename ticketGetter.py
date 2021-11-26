import requests
import json
import credentials

myAuth = (credentials.USERNAME, credentials.TOKEN)
requestURL = credentials.URL + '/api/v2/tickets'
ticketList = requests.get(requestURL, auth = myAuth)
print(ticketList.json())