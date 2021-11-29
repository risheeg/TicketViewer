import requests
import credentials
import display

PAGE_SIZE = 25

#Retrieves the inital page of tickets, and then calls on display function to display retrieved tickets,
#finally calls upon show menu to allow user to naviagate to remaining ticket pages
def getInitalPage():
    requestURL = credentials.URL + '/api/v2/tickets' + '?page[size]=' + str(PAGE_SIZE) +'&sort=updated_at'
    ticketPage = requests.get(requestURL, auth = myAuth)
    if (ticketPage.ok):
        display.displayTicketList(ticketPage.json()['tickets'])
        showMenu(False, True, ticketPage.json())
    else:
        print("There was an error loading the initial page")
        handleError(ticketPage)    

#generates and displays contextual menu based on exsisitance of next and prev page
#to get user input on going to next/prev page
def showMenu (hasPrev, hasNext, currTicketPage):
    print("Please type the following menu options and enter to interact with the Ticket Viewer")
    nextOptionText = "1. Next " + str(PAGE_SIZE) + " tickets \n"
    prevOptionText = "-1. Previous " + str(PAGE_SIZE) + " tickets\n"
    exitOptionText = "0. Exit \n"
    viewOptionText = "2. View a speific ticket \n"
    print(exitOptionText)
    validInputs ={"0", "2"}
    if hasNext: #builds menu
        validInputs.add("1")
        print(nextOptionText)
    if hasPrev: #builds menu
        validInputs.add("-1")
        print(prevOptionText)
    print(viewOptionText)    
    
    choice = input()
    if choice not in validInputs: 
        print("Invalid Input")
        return showMenu(hasPrev, hasNext, currTicketPage)
    if choice == "0": # exit 
        return()
    elif choice == "2": # View a specific ticket
        getTicketByID()
        return showMenu(hasPrev, hasNext, currTicketPage)  
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
    if (newTicketPage.ok):
        if incOrDec == "-1":
            hasPrev = checkPage(newTicketPage.json()['links']['prev'])
        if incOrDec == "1":
            hasNext = checkPage(newTicketPage.json()['links']['next'])
        display.displayTicketList(newTicketPage.json()['tickets'])
        showMenu(hasPrev, hasNext, newTicketPage.json())
    else:
        print("There was an issue getting the desired page")
        handleError(newTicketPage)    

#return true, if the requestURL page contains a non-empty list of tickets
def checkPage(requestURL):
    ticketPage = requests.get(requestURL, auth = myAuth)
    if(ticketPage.ok):
        return (len(ticketPage.json()['tickets']) != 0)
    else:
        print("An error was encountered trying to determine if the surrounding pages were valid")
        handleError(ticketPage)    
#Gets and displays desired ticket number from user
def getTicketByID():
    ticket_id = input("Please enter your Ticket Id or press 0 to exit:\n")
    if (ticket_id == 0):
        return
    requestURL = credentials.URL + "/api/v2/tickets/" + ticket_id
    ticketDetails = requests.get(requestURL, auth=myAuth)
    if(ticketDetails.ok):
        display.displayTicket(ticketDetails.json()['ticket'])
    else:
        handleError(ticketDetails)
        return getTicketByID()
#Prints corresponding error message to error status code
def handleError(requestData):
    if (requestData.status_code == 400):
        print("The request could not be understood. Try inputting it in differently")
    elif (requestData.status_code == 404):
        print("Couldn't find a corresponding entry to your request. If you were looking for a ticket then a ticket with that ID could not be found. Try a different number.")
    elif (requestData.status_code == 500):
        print("The service is down. Try again later")   
    elif (requestData.status_code == 429):
        print("Too many reuests, try after a while")
    elif (requestData.status_code == 401):
        print("There was an error with your credentials. Make sure you've inputted in your details in credentials.py")    
    else:
        print("An unidentified error occured. Let us know!")            
  
myAuth = (credentials.USERNAME, credentials.TOKEN) 
getInitalPage()









