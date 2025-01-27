import os
import csv
import re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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
with open("assignments.txt", "w") as writefile:
    for assignment in stuff:
        if bool(re.match(r".*?\([0-9]+\)", assignment)):
            print("match!")
            writefile.write(assignment+"\n")