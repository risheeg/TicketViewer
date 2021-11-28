import requests
from prettytable import PrettyTable #Note must install PrettyTable
import credentials

PAGE_SIZE = 1

#Retrieves the inital page of tickets, and then calls on display function to display retrieved tickets,
#finally calls upon show menu to allow user to naviagate to remaining ticket pages
def getInitalPage():
    requestURL = credentials.URL + '/api/v2/tickets' + '?page[size]=' + str(PAGE_SIZE)
    ticketPage = requests.get(requestURL, auth = myAuth)
    displayTicket(ticketPage.json()['tickets'])
    showMenu(False, True, ticketPage.json())

#generates and displays contextual menu based on exsisitance of next and prev page
#to get user input on going to next/prev page
def showMenu (hasPrev, hasNext, currTicketPage):
    print("Please type the following menu options and enter to interact with the Ticket Viewer")
    nextOptionText = "1. Next " + str(PAGE_SIZE) + " tickets \n"
    prevOptionText = "-1. Previous " + str(PAGE_SIZE) + " tickets\n"
    exitOptionText = "0. Exit \n"
    validInputs ={"0"}
    if hasNext:
        validInputs.add("1")
        print(nextOptionText)
    if hasPrev:
        validInputs.add("-1")
        print(prevOptionText)
    print(exitOptionText)
    choice = input()
    if choice not in validInputs:
        print("Invalid Input")
        return showMenu(hasPrev, hasNext, currTicketPage)
    if choice == "0": # exit 
        return()
    else:
        navigateToPage(currTicketPage, choice)

#Takes in parameter of increment or decrement page and then displays the new page with a relevent menu    
def navigateToPage(ticketPage, incOrDec):
    if incOrDec == "-1":
        pageOption = 'prev'
        hasNext = True
    if incOrDec == "1":
        pageOption = 'next'
        hasPrev = True
    requestURL = ticketPage['links'][pageOption]
    newTicketPage = requests.get(requestURL, auth = myAuth)
    if incOrDec == "-1":
        hasPrev = checkPage(newTicketPage.json()['links']['prev'])
    if incOrDec == "1":
        hasNext = checkPage(newTicketPage.json()['links']['next'])
    displayTicket(newTicketPage.json()['tickets'])
    showMenu(hasPrev, hasNext, newTicketPage.json())

#return true, if the requestURL page contains a non-empty list of tickets
def checkPage(requestURL):
    ticketPage = requests.get(requestURL, auth = myAuth)
    return (len(ticketPage.json()['tickets']) != 0)

#Given a list of tickets, ticketList, prints all the tickets in a PrettyTable
def displayTicket(ticketList):
    if ticketList == []:
        print("There are no more ticket")
    else:    
        ticketTable = PrettyTable(["ID", "Status", "Priority", "Subject", "RequesterID", "Updated"])
        for ticket in ticketList:
            ticketTable.add_row([ticket['id'], ticket['status'], ticket['priority'], ticket['subject'], str(ticket['requester_id']), ticket['updated_at']])
        print(ticketTable)

        
myAuth = (credentials.USERNAME, credentials.TOKEN) 
getInitalPage()









