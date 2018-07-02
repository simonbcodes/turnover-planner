# Turnover Planner
This script matches classrooms together based on computer type and location in a way that minimizes the total number of computers moved.

This script takes in 2 CSVs from 2 seperate weeks of classes and generates a CSV of pairings that minimize the number of computers that need to be moved between the different locations. The code handles new classes being added and old classes being removed, which means that it can handle the different situations that occur during the running of the class schedule.

# Basic Operation
To generate a pairing, the file can be run as follows:
```
python3 turnover_planner.py [past_week.csv] [new_week].csv
```
This outputs a pairings.csv that contains the classrooms to match.
