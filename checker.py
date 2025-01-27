import os
import csv
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

with open("assignments.json", "r") as file:
    current_assignments = list(map(str.rstrip, list(json.load(file).keys())))
    file.close()
    
with open("modules.json", "r") as file:
    week_map = json.load(file)
    week_assignments = []
    for week in list(week_map.keys()):
        week_assignments += week_map[week]["assignments"]
    week_assignments = list(map(str.rstrip, week_assignments))
    file.close()

assignments = []
with open("assignments.txt", "r") as file:
    for line in file:
        assignments.append(line.rstrip())
    
for assignment in assignments:
    if assignment not in current_assignments:
        print(f"\nWarning! '{assignment}' from assignments.txt not in assignments.json!")

for assignment in current_assignments:
    if assignment not in week_assignments:
        print(f"\nWarning! '{assignment}' from assignments.json not in modules.json!")

for assignment in week_assignments:
    if assignment not in current_assignments:
        print(f"\nCRITICAL WARNING!!! '{assignment}' from modules.json not in assignments.json!")
print("\n")