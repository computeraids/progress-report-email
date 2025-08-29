import funcs

run = True

# this is the most basic thing, but it just runs a interactive terminal thing for the tool. We can interact with any supporting functions from funcs, 
# but use this file to write software logic.
while run:
    command = int(input("""What command do you want to use? (Input a number)
    0) Setup Userdata
    1) Scrape Assignments \t 2) Retrieve API Info
    3) Check Config \t\t 4) Make Emails
    5) Exit\n"""))
    match command:
        case 0:
            funcs.setup_data(["assignments","modules","api"])
        case 1:
            funcs.api_scrape()
        case 2:
            funcs.canvas_api()
        case 3:
            funcs.check()
        case 4:
            funcs.make_emails()
        case 5:
            run = False
        case 6:
            funcs.api_scrape()
        case 9:
            ans = input("You are about to reset userdata. Are you sure you want to do this? (Y/N)")
            if ans == "Y" or ans == "y":
                funcs.setup_data(["config"])