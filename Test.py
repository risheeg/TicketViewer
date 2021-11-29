import pytest
import ticketGetter
import json
import requests
import credentials

def deleteTickets(startRange, endRange):
    deletionValues = ','.join(map(str, list(range(startRange, endRange))))
    requestURL = credentials.URL + '/api/v2/tickets/destroy_many?ids=' + deletionValues
    requestData = requests.delete(requestURL, auth = myAuth)
    print(requestData)

def createTickets(filePath):
    json_data = json.load(open(filePath))
    requestURL = credentials.URL + "/api/v2/tickets/create_many"
    headers = {'content-type': 'application/json'}
    requestData = requests.post(requestURL, auth=myAuth, data=json.dumps(json_data), headers = headers)
    print(requestData)

myAuth = (credentials.USERNAME, credentials.TOKEN)

#I ran into a couple issues with monkeypatch and mocking the input for my unit tests.
#This could serve as an example of a unit test that I would write, the remaining functions were tested manually
def testGetInitalPage(capsys, monkeypatch):
    createTickets("TestFiles/100tickets.json") 
    monkeypatch.setattr('builtins.input', lambda _:"0")
    ticketGetter.getInitalPage()
    captured, err = capsys.readouterr()
    print(len(captured))
    deleteTickets(1, 101)


