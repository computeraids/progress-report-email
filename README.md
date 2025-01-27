# Grade Report Compiler #

 This repository is made to create a .csv file for exporting the necessary spreadsheet to email students via the template provided. The functions of each file, in addition to how to customize and use them, are provided below, under each section describing each file. Feel free to use this for any course, but be aware the mapping might be difficult in some courses, especially those that include external assignments or resources.

### Quickstart ###

- Drag and drop an entire gradebook export from your course into the main directory for this repo. Don't worry about the name.
- Run `assignment_scraper.py`. It should produce or update a file called `assignments.txt`.
- From this file, copy all assignments you want to report on into the `assignments.json` file, using the format given by the example.
- Copy all assignments from `assignments.json` into `modules.json`, putting all assignments belonging to each module in a respective list. If you need to create new weeks, make sure their names are numerical, and increasing from previous weeks.
- Name each module / week in `modules.json`.
- After moving all appropriate assignments, run `checker.py`. It will produce output letting you know what files in `assignment.txt` aren't in `assignments.json`, and what files in `assignments.json` aren't in `modules.json`, and what assignments are in `modules.json` that aren't in `assignments.json`. This last one is vitally important; if there are assignments in `modules.json` that aren't in `assignments.json`, the tool **will** crash.
- Once you have validated with `checker.py`, run `runner.py`. It will ask you to provide a number during it's runtime; this number correspondeds to the number you put in `modules.json` for the module you want to export. It will produce an output .csv file named `Report - Content Block.csv`, under the `exports/` directory.
- Upload the exported csv to Google Drive. Make sure you have Yet Another Mail Merger (YAMM) installed (should be for all UNC Charlotte users).
- Utilize the email template provided here, OR write your own following the YAMM format and column headers in exported csv. Either way, save it as a draft under your email. Remember you can personalize the title, too!
- Send the email utilizing YAMM from Google Sheets. You're done!

## File Explanations ##

 This section serves to explain each file, a bit about what it does, and why. For files which require user input, it will describe in detail how to correctly format these files.

### `assignment_scraper.py` ###

 This file takes __the last .csv file__ in the directory and treats it as the gradebook, scraping the column headers for assignments. It does this by searching for all assignments which have " (" located inside them, since all canvas assignments end in their assignment ID in parenthesis. This means if assignments include parentheses, this will not be read correct (since all parts after the "( " are truncated.). If this is an issue, let me know, and I can write something a little bit smarter.

 It is worth noting that the scraper will **not** scrape unpublished assignments, or at least hasn't before. It goes based on what Canvas provides in the entire gradebook export.

If this file isn't working, check to make sure you don't have multiple .csv files in the main directory. Ensure that only the current gradebook is present.

### `assignments.txt` ###

 This file is produced by `assignment_scraper.py`, where every newline should represent an assignment in the course. This mostly exists to allow users to easily copy each assignment into the assignments file.

 Any issues in this file stem from issues with the gradebook, so start there if you have issues.
 
### `assignments.json` ###

 This is a simple JSON file, containing references for each assignment in the course. All this file does is specify, for each assignment, what value in the gradebook represents the assignment being missing. Under each assignment, there is a single key, `missingif`. Each assignment, when checked by `runner.py`, checks to see if the value in the gradebook is the same as `missingif`. If it is, the assignment is considered missing. `missingif` values can be floats, ints, or strings; the checker tries them all to see if the assignment is missing.

 You can have more assignments in `assignments.json` than in `modules.json`, as this file is only used to reference the assignments `runner.py` checks based on `modules.json`. This means you can fill out more assignments than modules, and the tool will work fine; you only need to make sure that all assignments in `modules.json` are in `assignments.json`.
 
### `modules.json` ###

 This is another JSON file, this time matching each week to it's corresponding name and material. The top level key for each which should **always** be a numerical value; it shouldn't matter if it's in string, int, or float format. When `runner.py` recieves a week to export for, it will report that week ***and*** all weeks whose numerical value is less than that number. That means if you have weeks `[1, 2, 3, 3.5, 4]`, and you create a report for `3.5`, the coursewide statistics will include `1`, `2,` `3`, and `3.5`.

 Each top level key also includes two subkeys in it's dictionary; `name` and `assignments`. `name` is simply the cosmetic name for the module / week; This is what will be processed and included as `module` in the final export. For assignments, you must list each assignment corresponding to that content block *exactly as it appears* in `assignments.json`. This is how the tool knows what assignments to check for.

### `checker.py` ###

 This script is meant to be run anytime after adding or updating `assignments.txt`, `assignments.json`, or `modules.json`. This quickly checks the contents of each file, and if they are present in the other files.

 It first checks to see if all assignments in `assignments.txt` are present in `assignments.json`; this simply servers as a reminder if new assignments have been added to the gradebook since the last run, to add them to the `assignments.json` file. This can be ignored, if you don't want the tool to check an assignment yet; it won't hurt anything.

 It then checks if all assignments in `assignments.json` are present in `modules.json`. This mostly serves as another notice if you forgot to move assignments from `assignments.json` into their corresponding content blocks; again, no issues will arise from this when running `runner.py`, so can be ignored.

 Finally, it checks to see if assignments from `modules.json` are present in `assignments.json`; this step is **critical**. Any file in `modules.json` that isn't referenced in `assignments.json` ***will*** throw and error and crash the tool, if the assignment has to be checked for completion. This status is fine for assignments which are in future weeks (and thus unchecked), but cannot be the case if the assignment belongs to the current or previous content blocks.

### `runner.py` ###

 This is the primary file, which generates the export csv which is used for YAMM. It will ask you to input a number; this number needs to match **exactly** to some number on the top level keys of `modules.json`, since this will be the very first week added. It will then check and add all weeks to the report with numbers less than the input.

 It then gathers all needed student and assignment data from the gradebook. In doing this, it utilizes the `missingif` value from `assignments.json` for each assignment to determine if they are missing or not in the report.

 Once it's done, you'll find the output in `exports/Report - Content Block.csv`. "Content Block" is replaced by the `name` value for the current content block.

### `examples/sample_email.txt` ###

This is a sample of a formatted email to be utilized for YAMM using the script; feel free to copy paste it and change it as you wish. If you want to create your own template, make sure to [follow YAMM's guide on doing so](https://support.yet-another-mail-merge.com/hc/en-us/articles/115003400145-Send-your-first-mail-merge-with-YAMM).

### `examples/` ###

This folder is full of example files, namely `assignments.txt`, `assignments.json`, `modules.json`, sample export and sample gradebook. All of this is here so that you can see what a completed and working version of the script does. This examples are provided based on the UNC Charlotte 2181 template course, and contains no student data (the only student in the gradebook is the test student). Look at these for formatting inspiration. Thanks to Braxton Haight (bhaight@charlotte.edu) for providing these examples!

## Utilizing YAMM ##
 
 UNC Charlotte provides a [great tutorial](https://services.help.charlotte.edu/TDClient/33/Portal/KB/ArticleDet?ID=186) on utilize YAMM. The exported csv is already formatted to use this directly, assuming you have an email set up for it.