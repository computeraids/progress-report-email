# Grade Report Compiler #

 This repository is made to create a .csv file for exporting the necessary spreadsheet to email students via the template provided. The functions of each file, in addition to how to customize and use them, are provided below, under each section describing each file. Feel free to use this for any course, but be aware the mapping might be difficult in some courses, especially those that include external assignments or resources.

### Quickstart ###

- Run **main.py** from command line via `python3 main.py`. All future instructions refer to running things from this interactive window.
- Use the `Setup Userdata` function in main (value 0)
- Open **./userdata/config.json**. Enter in values for `apikey` and `course`. Make sure they are strings.
- After doing that, run `Get Course Student List`. This only needs to be run a single time for the course.
- Next, run `Get Course Assignments`, which grabs all assignments currently in the course, and grab the modules.
- Open **./userdata/modules.json** Cut and paste assignments from the bottom module, *"Homeless Assignments"* into their respective modules. You do not have to copy everything, but the tool will not report on these assignments.
    - For clarity: every module imported has a list called `assignments` that is empty by default. Add items attached to that module to that list. It's important to cut and paste so that the assignments don't appear in *"Homeless Assignments"* anymore. Everytime you run `Get Course Assignments`
- If you want to report on some metric other than the course modules you have assigned, edit the modules in the **./userdata/modules.json** file to your liking.
- After all this is done, run `Pull Current Assignment Details`, entering in the week/module you want to report on from the list. This will grab the current submission status for all these assignments, and prior ones.
- Finally, run `Make Emails` and check for your export in **./exports**.