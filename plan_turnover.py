import pandas as pd
import sys, os, math
import process_live_numbers

classes = process_live_numbers.classes

old_week_date = str(sys.argv[1])
new_week_date = str(sys.argv[2])

# old_week = pd.read_csv(os.getcwd() + '/' + sys.argv[1]) # current/old week
# new_week = pd.read_csv(os.getcwd() + '/' + sys.argv[2]) # next week

old_week = classes.loc[classes['Start Date'] == old_week_date]
new_week = classes.loc[classes['Start Date'] == new_week_date]

print(old_week)
print(new_week)

def check_perfect_matches(pairings, old_week, new_week):
    for type in computer_types: # iterate through types
        for old_row, old_row_obj in old_week[type].iterrows(): # find classes that exactly match in size
            for new_row, new_row_obj in new_week[type].iterrows():
                if(new_row_obj['Regs'] == old_row_obj['Regs']):
                    # print('{} -> {}, 0'.format(old_row_obj['Course Name'], new_row_obj['Course Name'])) #print match
                    pairings = pairings.append({'Old Class': old_row_obj['Course Name'], 'New Class': new_row_obj['Course Name'], 'Difference': 0, 'Type': type}, ignore_index=True)
                    # print('o:{} n:{}'.format(old_row, new_row))
                    old_week[type].drop(old_row, inplace=True)
                    new_week[type].drop(new_row, inplace=True)
                    break
    return pairings

def check_matches(pairings, old_week, new_week):
    for type in computer_types: # iterate through type
        for row in range(0, min(len(old_week[type]), len(new_week[type]))): # iterate through all classes in type
            if old_week[type].size > 0 and new_week[type].size > 0: # skip types with no classes
                old_name = old_week[type].iloc[row]['Course Name']
                new_name = new_week[type].iloc[row]['Course Name']
                net_change = int(new_week[type].iloc[row]['Regs']) - int(old_week[type].iloc[row]['Regs']) # difference between new class number and old
                # print('{} -> {} = {}'.format(old_name, new_name, net_change)) #print pair and difference (positive difference means add more computers)
                pairings = pairings.append({'Old Class': old_name, 'New Class': new_name, 'Difference': net_change, 'Type': type}, ignore_index=True)
        drop_range = min(len(old_week[type]), len(new_week[type]))
        old_week[type] = old_week[type].iloc[drop_range:] # remove all matches pairs
        new_week[type] = new_week[type].iloc[drop_range:]
    return pairings, old_week, new_week

def leftover_matches(pairings, old_week, new_week):
    for type in computer_types:
        if len(old_week[type]) > 0: # class is removed from old week to new
            for extra_row, row_obj in old_week[type].iterrows():
                pairings = pairings.append({'Old Class': row_obj['Course Name'], 'New Class': '', 'Difference': -int(row_obj['Regs']), 'Type': type}, ignore_index=True)
        if len(new_week[type]) > 0: # new class added from old week to new
            for extra_row, row_obj in new_week[type].iterrows():
                pairings = pairings.append({'Old Class': '', 'New Class': row_obj['Course Name'], 'Difference': int(row_obj['Regs']), 'Type': type}, ignore_index=True)
    return pairings

computer_types = ['A', 'B', 'C', 'BYOD']

filtered_old_by_type = {} # dict of dataframes of filtered only classes. each index is a dataaframe of classes for a specific computer type
filtered_new_by_type = {}
old_grouped_by_type = {} # dict of dataframes of classes. each index is a dataframe of classes for a specific computer type
new_grouped_by_type = {}

for type in computer_types: # filter by classes in filtered
    filtered_old_by_type[type] = old_week.loc[('Adventures' in old_week['Course Name']) & (old_week['Course: Hardware Tier'] == type)].sort_values(by='Regs')
    filtered_new_by_type[type] = new_week.loc[('Adventures' in new_week['Course Name']) & (new_week['Course: Hardware Tier'] == type)].sort_values(by='Regs')

for type in computer_types: # sort the classes by the number of students in the class within computer type (non-filtered)
    # print(type)
    old_grouped_by_type[type] = old_week.loc[(old_week['Course: Hardware Tier'] == type) & ('Adventures' in old_week['Course Name'])].sort_values(by='Regs')
    new_grouped_by_type[type] = new_week.loc[(new_week['Course: Hardware Tier'] == type) & ('Adventures' in new_week['Course Name'])].sort_values(by='Regs')
    old_grouped_by_type[type] = old_week.loc[old_week['Course: Hardware Tier'] == type].sort_values(by='Regs')
    new_grouped_by_type[type] = new_week.loc[new_week['Course: Hardware Tier'] == type].sort_values(by='Regs')

pairings = pd.DataFrame(columns=['Old Class', 'New Class', 'Difference', 'Type'])

pairings = check_perfect_matches(pairings, old_grouped_by_type, new_grouped_by_type) # do 2 sets of perfect matches, filtered and non-filtered
pairings = check_perfect_matches(pairings, filtered_old_by_type, filtered_new_by_type)

pairings, leftovers_old, leftovers_new = check_matches(pairings, old_grouped_by_type, new_grouped_by_type) # check matches for filtered and non-filtered locations
pairings, filtered_leftovers_old, filtered_leftovers_new = check_matches(pairings, filtered_old_by_type, filtered_new_by_type)

for type in computer_types: # combine leftovers
    leftovers_new[type] = leftovers_new[type].append(filtered_leftovers_new[type], sort=False)
    leftovers_old[type] = leftovers_old[type].append(filtered_leftovers_old[type], sort=False)

pairings, leftovers_old, leftovers_new = check_matches(pairings, leftovers_old, leftovers_new) # match leftovers, ignoring type difference
pairings = leftover_matches(pairings, leftovers_old, leftovers_new) # take care of leftovers

print(pairings)
pairings.to_csv('pairings.csv', encoding='utf-8', index=False) # write pairings to CSV
print('Pairings written to CSV')
