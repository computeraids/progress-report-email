import os
import csv
import json
import requests
import configparser
import time
import re


# logic that sets working directory to current. required for runtime on linux
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

### imported from checker ###
# Check is a function that makes sure that files which are scraped (and put into assignments.txt) are properly set up.
# honestly, we need something better than this long term, but its better to have it than not.
def check():

    # open the api file
    with open("api.json", "r") as file:
        # the strips on the below line help remove random whitespace from canvas imports
        api_assignments = list(map(str.rstrip, list(json.load(file).keys())))
        file.close()

    # open the assignments json (handmade)
    with open("assignments.json", "r") as file:
        assignment_dict = json.load(file)
        # the strips on the below line help remove random whitespace from canvas imports
        current_assignments = list(map(str.rstrip, list(assignment_dict.keys())))
        file.close()

    # open the modules json (handmade)  
    with open("modules.json", "r") as file:
        week_map = json.load(file)
        # this is a temp list used to hold all the assignments which have modules ("weeks").
        assignments_in_modules = []
        # this just adds all assignments in each module to the list
        for week in list(week_map.keys()):
            assignments_in_modules += week_map[week]["assignments"]
        # same thing, strips whitespace
        assignments_in_modules = list(map(str.rstrip, assignments_in_modules))
        file.close()


    # this pulls the assignment names from output of the scraper.
    assignments = []
    with open("assignments.txt", "r") as file:
        for line in file:
            assignments.append(line.rstrip())
        
    for assignment in assignments:
        if assignment not in current_assignments:
            print(f"\nWarning! '{assignment}' from assignments.txt not in assignments.json!")

    for assignment in current_assignments:
        if assignment not in assignments_in_modules:
            print(f"\nWarning! '{assignment}' from assignments.json not in modules.json!")
        if assignment_dict[assignment]["missingif"] == 'api':
            if assignment not in api_assignments:
                print(f"\nCRITICAL WARNING!!! '{assignment}' from assignments.json not in api.json! (run api_handler.py)")

    for assignment in assignments_in_modules:
        if assignment not in current_assignments:
            print(f"\nCRITICAL WARNING!!! '{assignment}' from modules.json not in assignments.json!")
    print("\n")



### imported from api_handler ###
def canvas_api():
    config = configparser.ConfigParser()
    config.read('userdata/config.ini')
    apikey = str(config["API"]["apikey"])
    course = str(config["API"]["course"])
    print(apikey)

    with open("assignments.json", "r") as file:
        assignment_dict = json.load(file)
        file.close()
        
    with open("modules.json", "r") as file:
        week_map = json.load(file)
        weeks = week_map.keys()
        file.close()

    current_week = str(input("Please enter the number corresponding to the week (i.e. '2')"))
    weeks_to_send = [current_week]

    for week in weeks:
        if float(week) < float(current_week):
            weeks_to_send.append(week)

    workfile = ""

    current_assignments = []
    for week in weeks_to_send:
        current_assignments += week_map[week]["assignments"]

    missing_dict = {}
    for assignment in current_assignments:

        if assignment_dict[assignment]["missingif"] == "api":
            assignment_id = assignment.split("(")[-1][:-1]
            missing_dict[assignment] = []

            page = 1
            print(f"Requesting page {page} of {assignment}...")
            r = requests.get("https://uncc.instructure.com/api/v1/courses/"+course+"/assignments/"+assignment_id+"/submissions?access_token="+apikey+"&per_page=100&page=1&include[]=submission_history")
            while r.status_code == 403:
                print(f"Status Code 403, rerequesting page {page} of {assignment}...")
                time.sleep(5)
                r = requests.get("https://uncc.instructure.com/api/v1/courses/"+course+"/assignments/"+assignment_id+"/submissions?access_token="+apikey+"&per_page=100&page=1&include[]=submission_history")
            print("Done!")
            while r.text != "[]":
                page += 1
                submissions = json.loads(r.text)
                for submission in submissions:
                    if submission["missing"]:
                        missing_dict[assignment].append(submission["user_id"])
                print(f"Requesting page {page} of {assignment}...")
                r = requests.get("https://uncc.instructure.com/api/v1/courses/"+course+"/assignments/"+assignment_id+"/submissions?access_token="+apikey+"&per_page=100&page="+str(page)+"&include[]=submission_history")
                while r.status_code == 403:
                    print(f"Status Code 403, rerequesting page {page} of {assignment}...")
                    time.sleep(2)
                    r = requests.get("https://uncc.instructure.com/api/v1/courses/"+course+"/assignments/"+assignment_id+"/submissions?access_token="+apikey+"&per_page=100&page="+str(page)+"&include[]=submission_history")
                print("Done!")
            print(f"Page {page} empty, moving on...")
    print("All assignments scraped.")
    with open("api.json", "w") as file:
        json.dump(missing_dict, file, indent=4)



### imported from assignment_scraper ###
def scrape_assignments():
    with open("assignments.json", "r") as file:
        assignment_dict = json.load(file)
        file.close()

    workfile = ""

    for file in os.listdir():
        if (file.split(".")[-1] == "csv"):
            workfile = file

    if workfile == "":
        print("Error: No Gradebook found")
    else:
        print("Gradebook found, extracting assignments")
        with open(workfile) as file:
            readfile = csv.reader(file)
            stuff = next(readfile)
            
            file.close()

    suggestions_dict = {}
    with open("assignments.txt", "w") as writefile:
        for assignment in stuff:
            if bool(re.match(r".*?\([0-9]+\)", assignment)):
                if assignment not in assignment_dict.keys():
                    writefile.write(assignment+"\n")
                    suggestions_dict[assignment] = {"missingif":"api"}

    with open("suggested_assignments.json", "w") as file:
        json.dump(suggestions_dict, file, indent=4)



### imported from runner ###
def is_missing(assignment, current_row, name_to_index, missing_val):
        #checks for list type, then evaluates all criteria. behaves using "or" logic
        if type(missing_val) == type([]):
            for value in missing_val:
                if is_missing(assignment, current_row, name_to_index, value):
                    return True
        elif missing_val == "api" and int(current_row[1]) in api_dict[assignment]:
            return True
        elif current_row[name_to_index[assignment]] == missing_val:
            return True
        else:
            try: 
                if float(current_row[name_to_index[assignment]]) == missing_val:
                    return True
            except:
                pass
        return False



### imported from runner ###
def make_emails():
    with open("api.json", "r") as file:
        api_dict = json.load(file)
        file.close()

    with open("assignments.json", "r") as file:
        assignment_dict = json.load(file)
        file.close()
        
    with open("modules.json", "r") as file:
        week_map = json.load(file)
        weeks = week_map.keys()
        file.close()

    current_week = str(input("Please enter the number corresponding to the week (i.e. '2')"))
    weeks_to_send = [current_week]

    for week in weeks:
        if float(week) < float(current_week):
            weeks_to_send.append(week)

    workfile = ""

    current_assignments = []
    for week in weeks_to_send:
        current_assignments += week_map[week]["assignments"]

    for file in os.listdir():
        if (file.split(".")[-1] == "csv"):
            workfile = file

    ### GLOBAL STUFF DONE HERE (because I said so) ###
    module = week_map[current_week]["name"]
    assignment_count = len(week_map[current_week]["assignments"])
    assignmentlist = ""
    for assignment in week_map[current_week]["assignments"]:
        final_string = ""
        for piece in assignment.split(" (")[:-1]:
            final_string += piece
        assignmentlist += "- "+final_string+"\n"

    totalcomplete = 0
    for week in weeks_to_send:
        totalcomplete += len(week_map[week]["assignments"])
        
    totalcourse = 0
    for week in weeks:
        totalcourse += len(week_map[week]["assignments"])

    if workfile == "":
        print("Error: No Gradebook found")
    else:
        data = []
        with open(workfile) as file:
            gradebook = csv.reader(file)

            assignments = next(gradebook)
            name_to_index = {}
            for assignment in current_assignments:
                name_to_index[assignment] = assignments.index(assignment)
            current_row = next(gradebook)
            name_to_index["SIS Login ID"] = assignments.index("SIS Login ID")
            try:
                while True:
                    current_row = next(gradebook)
                    student = current_row[0].split(", ")[-1]
                    email = current_row[name_to_index["SIS Login ID"]]+"@charlotte.edu"

                    module_completed = assignment_count
                    for assignment in week_map[current_week]["assignments"]:
                        if is_missing(assignment, current_row, name_to_index, assignment_dict[assignment]["missingif"]):
                            module_completed -= 1

                    actualcompleted = totalcomplete
                    late_assignment_list = ""
                    for week in weeks_to_send:
                        for assignment in week_map[week]["assignments"]:
                            if is_missing(assignment, current_row, name_to_index, assignment_dict[assignment]["missingif"]):
                                actualcompleted -= 1
                                final_string = ""
                                for piece in assignment.split(" (")[:-1]:
                                    final_string += piece
                                late_assignment_list += "- "+final_string+"\n"


                    if actualcompleted != totalcomplete:
                        late_assignment_list = "In order to catch up, you can complete the following assignments:\n" + late_assignment_list

                    data.append({"Email Address":email, "Student":student, "Module":module, "Assignment Count":assignment_count,
                    "Assignment List":assignmentlist, "Module Completed":module_completed, "Actual Completed Assigments":actualcompleted,
                    "Total Assignments in Course":totalcourse, "Total Complete":totalcomplete, "Late Assignments":late_assignment_list})

            except StopIteration:
                print("done!")
            file.close()
        if ":" in week_map[week]['name']:
            file = open(f"exports/Report - {week_map[week]['name'].split(':')[0]}.csv", "w", newline="")
        else:
            file = open(f"exports/Report - {week_map[week]['name']}.csv", "w", newline="")
        writer = csv.DictWriter(file, fieldnames=["Email Address", "Student", "Module", "Assignment Count", "Assignment List",
        "Module Completed", "Actual Completed Assigments", "Total Assignments in Course", "Total Complete", "Late Assignments"])
        writer.writeheader()
        writer.writerows(data)
        file.close()