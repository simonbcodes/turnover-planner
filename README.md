# Turnover Planner
This script matches classrooms together based on computer type and location in a way that minimizes the total number of computers moved.

The script uses download_live_numbers.py to download the current class rosters from a Google Sheet. This output is pickled and loaded into process_live_numbers.py, which drops certain columns and cleans the data before it is used to generate pairings. plan_turnover.py actually generates pairings, taking into account computer type, type of class and number of students. The pairings are generated to minimize the number of computers that need to be moved.

# Basic Operation
To generate a pairing, the file can be run as follows:
```
python3 plan_turnover.py [previous_week_date] [next_week_date]
```
This outputs a pairings.csv that contains the classrooms to match.
