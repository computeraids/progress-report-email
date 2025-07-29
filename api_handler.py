import os
import csv
import json
import requests
import configparser
import time

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def canvas_api():
    config = configparser.ConfigParser()
    config.read('api.ini')
    apikey = str(config["DEFAULT"]["apikey"])
    course = str(config["DEFAULT"]["course"])

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