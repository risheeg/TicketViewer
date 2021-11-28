from prettytable import PrettyTable #Note must install PrettyTable

# A function to print out the relevent details of a ticket given the ticket section of a json
def displayTicket(ticketInfo):
    print("--------------")
    print("Ticket #", ticketInfo['id'], ticketInfo['subject'],"["+ticketInfo['status']+"]")
    print("Priority", ticketInfo['priority'],"| Assigned to:", ticketInfo['assignee_id'], )
    print("\nDescription:\n", ticketInfo['description']+"\n")
    print("Created at:", ticketInfo['created_at'])
    print("Due:", ticketInfo['due_at'])
    print("Last updated at", ticketInfo['updated_at'])
    print("View more info at:", ticketInfo['url'])
    print("--------------")

#Given a list of tickets, ticketList, prints all the tickets in a PrettyTable
def displayTicketList(ticketList):
    if ticketList == []:
        print("There are no more ticket")
    else:    
        ticketTable = PrettyTable(["ID", "Status", "Priority", "Subject", "RequesterID", "Updated"])
        for ticket in ticketList:
            ticketTable.add_row([ticket['id'], ticket['status'], ticket['priority'], ticket['subject'], str(ticket['requester_id']), ticket['updated_at']])
        print(ticketTable)
