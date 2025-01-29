import os
import csv
import re
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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