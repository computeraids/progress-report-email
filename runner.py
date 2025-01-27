import os
import csv
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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
    assignmentlist += "- "+assignment.split(" (")[0]+"\n"

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
        current_row = next(gradebook)
        name_to_index["SIS Login ID"] = assignments.index("SIS Login ID")
        try:
            while True:
                current_row = next(gradebook)
                student = current_row[0].split(", ")[-1]
                email = current_row[name_to_index["SIS Login ID"]]+"@charlotte.edu"

                module_completed = assignment_count
                for assignment in week_map[current_week]["assignments"]:
                    try:
                        if float(current_row[name_to_index[assignment]]) == assignment_dict[assignment]["missingif"]:
                            module_completed -= 1
                    except:
                        if current_row[name_to_index[assignment]] == assignment_dict[assignment]["missingif"]:
                            module_completed -= 1
                                

                actualcompleted = totalcomplete
                late_assignment_list = ""
                for week in weeks_to_send:
                    for assignment in week_map[week]["assignments"]:
                        try:
                            if float(current_row[name_to_index[assignment]]) == assignment_dict[assignment]["missingif"]:
                                actualcompleted -= 1
                                late_assignment_list += "- "+assignment.split(" (")[0]+"\n"
                        except:
                            if current_row[name_to_index[assignment]] == assignment_dict[assignment]["missingif"]:
                                actualcompleted -= 1
                                late_assignment_list += "- "+assignment.split(" (")[0]+"\n"

                if actualcompleted != totalcomplete:
                    late_assignment_list = "In order to catch up, you can complete the following assignments:\n" + late_assignment_list

                data.append({"Email Address":email, "Student":student, "Module":module, "Assignment Count":assignment_count,
                 "Assignment List":assignmentlist, "Module Completed":module_completed, "Actual Completed Assigments":actualcompleted,
                 "Total Assignments in Course":totalcourse, "Total Complete":totalcomplete, "Late Assignments":late_assignment_list})

        except StopIteration:
            print("done!")
        file.close()
    if ":" in week_map[week]['name']:
        file = open(f"exports/Report - {week_map[week]['name'].split(":")[0]}.csv", "w", newline="")
    else:
        file = open(f"exports/Report - {week_map[week]['name']}.csv", "w", newline="")
    writer = csv.DictWriter(file, fieldnames=["Email Address", "Student", "Module", "Assignment Count", "Assignment List",
    "Module Completed", "Actual Completed Assigments", "Total Assignments in Course", "Total Complete", "Late Assignments"])
    writer.writeheader()
    writer.writerows(data)
    file.close()
