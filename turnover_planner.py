import pandas as pd
import sys, os, math

old_week = pd.read_csv(os.getcwd() + '/' + sys.argv[1]) #current/old week
new_week = pd.read_csv(os.getcwd() + '/' + sys.argv[2]) #next week

def check_perfect_matches(pairings, old_week, new_week):
    for type in computer_types: #iterate through types
        for old_row, old_row_obj in old_week[type].iterrows(): #find classes that exactly match in size
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
    for type in computer_types: #iterate through type
        for row in range(0, min(len(old_week[type]), len(new_week[type]))): #iterate through all classes in type
            if old_week[type].size > 0 and new_week[type].size > 0: #skip types with no classes
                old_name = old_week[type].iloc[row]['Course Name']
                new_name = new_week[type].iloc[row]['Course Name']
                net_change = new_week[type].iloc[row]['Regs'] - old_week[type].iloc[row]['Regs'] #difference between new class number and old
                # print('{} -> {} = {}'.format(old_name, new_name, net_change)) #print pair and difference (positive difference means add more computers)
                pairings = pairings.append({'Old Class': old_name, 'New Class': new_name, 'Difference': net_change, 'Type': type}, ignore_index=True)
        drop_range = min(len(old_week[type]), len(new_week[type]))
        old_week[type] = old_week[type].iloc[drop_range:] #remove all matches pairs
        new_week[type] = new_week[type].iloc[drop_range:]
        if len(old_week[type]) > 0: #class is removed from old week to new
            for extra_row, row_obj in old_week[type].iterrows():
                pairings = pairings.append({'Old Class': row_obj['Course Name'], 'New Class': '', 'Difference': -row_obj['Regs'], 'Type': type}, ignore_index=True)
        if len(new_week[type]) > 0: #new class added from old week to new
            for extra_row, row_obj in new_week[type].iterrows():
                pairings = pairings.append({'Old Class': '', 'New Class': row_obj['Course Name'], 'Difference': row_obj['Regs'], 'Type': type}, ignore_index=True)
    return pairings

computer_types = ['A', 'B', 'C', 'BYOD']

stern_old_by_type = {} #dict of dataframes of Stern only classes. each index is a dataaframe of classes for a specific computer type
stern_new_by_type = {}
old_grouped_by_type = {} #dict of dataframes of classes. each index is a dataframe of classes for a specific computer type
new_grouped_by_type = {}

for type in computer_types:
    stern_old_by_type[type] = old_week.loc[(old_week['Location'] == 'Stern') & (old_week['Course: Hardware Tier'] == type)].sort_values(by='Regs')
    stern_new_by_type[type] = new_week.loc[(new_week['Location'] == 'Stern') & (new_week['Course: Hardware Tier'] == type)].sort_values(by='Regs')

for type in computer_types: #sort the classes by the number of students in the class within computer type
    old_grouped_by_type[type] = old_week.loc[(old_week['Course: Hardware Tier'] == type) & (old_week['Location'] != 'Stern')].sort_values(by='Regs')
    new_grouped_by_type[type] = new_week.loc[(new_week['Course: Hardware Tier'] == type) & (new_week['Location'] != 'Stern')].sort_values(by='Regs')

pairings = pd.DataFrame(columns=['Old Class', 'New Class', 'Difference', 'Type'])

pairings = check_perfect_matches(pairings, old_grouped_by_type, new_grouped_by_type)
pairings = check_perfect_matches(pairings, stern_old_by_type, stern_new_by_type)

pairings = check_matches(pairings, old_grouped_by_type, new_grouped_by_type)
pairings = check_matches(pairings, stern_old_by_type, stern_new_by_type)

print(pairings)
pairings.to_csv('pairings.csv', encoding='utf-8', index=False)
print('Pairings written to CSV')
