import assignment_scraper
import api_handler
import checker
import runner

run = True
while run:
    command = int(input("""What command do you want to use? (Input a number)\n1) Scrape Assignments \t 2) Retrieve API Info
3)Check Config \t\t 4) Make Emails\n5) Exit\n"""))
    match command:
        case 1:
            assignment_scraper.scrape_assignments()
        case 2:
            api_handler.canvas_api()
        case 3:
            checker.check()
        case 4:
            runner.make_emails()
        case 5:
            run = False
