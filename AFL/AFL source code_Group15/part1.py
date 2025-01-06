import pandas as pd

MAX_BR_PER_GAME = 3
DATASET = 'AFL-2022-totals.csv'

# PRE-PROCESSING

# Some values will be removed since they do not have importance on the brownlow votes
# These include: Player and Team (TM)

# Read the data into a pandas dataframe
print("Reading: ",DATASET)
afl_data = pd.read_csv(DATASET)

# Remove columns 'Player' and 'TM' since these will not be neccesary
afl_data = afl_data.drop(['Player','TM'], axis=1)

# Handle missing values, Most missing values should be 0

afl_data = afl_data.fillna(0)

# Divide all rows values by number of games to find game average

for row in range(afl_data.shape[0]):
    afl_data.iloc[row,:] = afl_data.iloc[row,:].div(afl_data.iloc[row,0])

# Check that values are within an acceptable range

is_any_errors = False
print("Range Checks:")
# Check values are positive and numeric
range_error = False
for row in range(afl_data.shape[0]):
    for column in range(afl_data.shape[1]):
        if((afl_data.iloc[row,column]<0)and(afl_data.iloc[row,column].isnumeric())):
            range_error = True
            is_any_errors = True
            print("\t|ERROR: Negative or non-numeric value found")

if(not range_error):
    print("\t|No negative or non-numeric values were found")

# Brownlow votes can not exceed 3 per game
range_error = False
for row in range(afl_data.shape[0]):
    brownlow_votes = afl_data.iloc[row]['BR']
    if(brownlow_votes>MAX_BR_PER_GAME):
        range_error = True
        is_any_errors = True
        print("\t|ERROR: More than 3 Brownlow votes per game")

if(not range_error):
    print("\t|No range error")

# 'Goals' must be less than 'kicks' + 'free kicks for'

range_error = False
for row in range(afl_data.shape[0]):
    total_kicks = afl_data.iloc[row]['KI'] + afl_data.iloc[row]['FF']
    if(total_kicks<(afl_data.iloc[row]['GL'])):
        range_error = True
        is_any_errors = True
        print("\t|ERROR: Value to large (More goals than kicks + free kicks)")

if(not range_error):
    print("\t|No range error")

# None of these values should be over 1000 per game
range_error = False
for row in range(afl_data.shape[0]):
    for column in range(afl_data.shape[1]):
        if(afl_data.iloc[row][column]>1000):
            range_error = True
            is_any_errors = True
            print("\t|ERROR: Value greater than 1000")
if(not range_error):
    print("\t|No range error")

if(is_any_errors):
    print("ERROR: Range errors were detected in the dataset")
else:
    print("No range errors were detected in the dataset")
    # Export dataset to csv
    afl_data.to_csv('processed_afl_dataset.csv')


""" Currently the processed dataset is stored in a pandas dataframe as
    'afl_data' which contains all of the statistics apart from 
    'player' and 'team'. Missing values were replaced with '0' and an
    average for each stat per game was stored. The dataset has been 
    checked for range errors of which none were found. """
