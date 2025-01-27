import os
import csv

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
        if "(" in assignment:
            writefile.write(assignment+"\n")