import funcs

run = True

# this is the most basic thing, but it just runs a interactive terminal thing for the tool. We can interact with any supporting functions from funcs, 
# but use this file to write software logic.
while run:
    command = int(input("""What command do you want to use? (Input a number)\n1) Scrape Assignments \t 2) Retrieve API Info
3)Check Config \t\t 4) Make Emails\n5) Exit\n"""))
    match command:
        case 1:
            funcs.scrape_assignments()
        case 2:
            funcs.canvas_api()
        case 3:
            funcs.check()
        case 4:
            funcs.make_emails()
        case 5:
            run = False
